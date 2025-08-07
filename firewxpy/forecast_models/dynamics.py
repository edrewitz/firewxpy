"""
This file hosts the graphics for the following: 

1) Vorticity/Geopotential Height/Wind
2) Geopotential Height
3) 24-Hour Geopotential Height Change
4) Geopotential Height/Wind
5) 10-Meter Wind/MSLP

(C) Eric J. Drewitz 2025

"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as md
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import metpy.calc as mpcalc
import numpy as np
import firewxpy.utils.parsers as parsers
import firewxpy.utils.geometry as geometry
import firewxpy.utils.colormaps as colormaps
import pandas as pd
import matplotlib.gridspec as gridspec
import firewxpy.utils.settings as settings
import firewxpy.utils.standard as standard
import firewxpy.utils.dims as dims
import os
import time as tim

from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from dateutil import tz
from firewxpy.utils.calc import scaling, Thermodynamics, unit_conversion
from firewxpy.utils.utilities import file_functions
from metpy.units import units
from firewxpy.data.data_access import model_data



def plot_vorticity_geopotential_height_wind(model, region, level=500, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

    """
    This function plots the Geopotential Height/Vorticity/Wind Forecast for a specific level. 

    Required Arguments: 
    
    1) model (String) - This is the model the user must select. 
                            
        Here are the choices: 
        1) GFS0p25 - GFS 0.25x0.25 degree
        2) GFS0p50 - GFS 0.5x0.5 degree
        3) GFS1p00 - GFS 1.0x1.0 degree
        4) GEFS0p50 - GEFS 0.5x0.5 degree
        5) CMCENS - Canadian Ensemble
        6) NAM - North American Model
        7) NA NAM - 32km North American Model - Full North America

    2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                            To look at any state use the 2-letter abbreviation for the state in either all capitals
                            or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                            CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                            North America use either: NA, na, North America or north america. If the user wishes to use custom
                            boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                            the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                            'oscc' for South Ops. 

    Optional Arguments: 
    
    1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                            500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

    2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                        and passing the data in or if the function needs to download the data. A value of False means the data
                        is downloaded inside of the function while a value of True means the user is downloading the data outside
                        of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                        things, it is recommended to set this value to True and download the data outside of the function and pass
                        it in so that the amount of data requests on the host servers can be minimized. 

    3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                    in the dataset. If the user wishes to download the data inside of the function, this value is None. 

    4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                    

    7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

    8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
        Default setting is True. Users should change this value to False if they wish to hide rivers.

    9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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
                            

    10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide state borders. 

    11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide county borders. 

    12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display GACC borders. 

    13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display PSA borders.

    14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display CWA borders.

    15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

    16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

    17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

    18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

    19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

    20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

    21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

    22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

    23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

    24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

    25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
        To change to a dashed line, users should set state_border_linestyle='--'. 

    26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
        To change to a dashed line, users should set county_border_linestyle='--'. 

    27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
        To change to a dashed line, users should set gacc_border_linestyle='--'. 

    28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'.    

    32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

    38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                        This is a feature of matplotlib, as per their definition, the shrink is:
                                        "Fraction by which to multiply the size of the colorbar." 
                                        This should only be changed if the user wishes to make a custom plot. 
                                        Preset values are called from the settings module for each region. 

    39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                when making a custom plot. 

    40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

    43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

    44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


    Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

    """

    data=data
    level=level
    ds=ds
    western_bound=western_bound
    eastern_bound=eastern_bound 
    southern_bound=southern_bound
    northern_bound=northern_bound
    show_rivers=show_rivers
    reference_system=reference_system
    state_border_linewidth=state_border_linewidth
    county_border_linewidth=county_border_linewidth
    gacc_border_linewidth=gacc_border_linewidth
    psa_border_linewidth=psa_border_linewidth 
    cwa_border_linewidth=cwa_border_linewidth
    nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
    nws_public_zones_linewidth=nws_public_zones_linewidth 
    state_border_linestyle=state_border_linestyle
    county_border_linestyle=county_border_linestyle
    gacc_border_linestyle=gacc_border_linestyle
    psa_border_linestyle=psa_border_linestyle 
    cwa_border_linestyle=cwa_border_linestyle
    nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
    nws_public_zones_linestyle=nws_public_zones_linestyle
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
        mapcrs = ccrs.LambertConformal()
    else:
        mapcrs = ccrs.PlateCarree()

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

    str_level = f"{level} MB"

    if level == 850:
        levels = np.arange(96, 180, 4)
    if level == 700:
        levels = np.arange(240, 340, 4)
    if level == 300:
        levels = np.arange(840, 1020, 10)
    if level == 250:
        levels = np.arange(900, 1140, 10)
    if level == 200:
        levels = np.arange(1000, 1280, 10)
    

    if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
        decimate = 20
        step = 1
        
        if level == 850:
            level_idx = 6
        if level == 700:
            level_idx = 12
        if level == 500:
            level_idx = 20
        if level == 300:
            level_idx = 28
        if level == 250:
            level_idx = 30
        if level == 200:
            level_idx = 32
    
    if model == 'CMCENS' or model == 'GEFS0p50':
        decimate = 10
        step = 1

        if level == 850:
            level_idx = 2
        if level == 700:
            level_idx = 3
        if level == 500:
            level_idx = 4
        if level == 300:
            level_idx = 6
        if level == 250:
            level_idx = 7
        if level == 200:
            level_idx = 8
        
    if model == 'GFS0p25' or model == 'GFS0p25_1h':
        decimate = 10
        step = 2
        
        if level == 850:
            level_idx = 5
        if level == 700:
            level_idx = 8
        if level == 500:
            level_idx = 12
        if level == 300:
            level_idx = 16
        if level == 250:
            level_idx = 17
        if level == 200:
            level_idx = 18
        
    if model == 'GFS0p50':
        decimate = 10
        step = 2
        
        if level == 850:
            level_idx = 6
        if level == 700:
            level_idx = 12
        if level == 500:
            level_idx = 20
        if level == 300:
            level_idx = 28
        if level == 250:
            level_idx = 30
        if level == 200:
            level_idx = 32
    
    if model == 'GFS1p00':
        decimate = 10
        step = 2

        if level == 850:
            level_idx = 5
        if level == 700:
            level_idx = 8
        if level == 500:
            level_idx = 12
        if level == 300:
            level_idx = 16
        if level == 250:
            level_idx = 17
        if level == 200:
            level_idx = 18

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
        wb=western_bound
        eb=eastern_bound
        sb=southern_bound
        nb=northern_bound
        x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
    else:
        wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
        sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
    
    if data == False:
        if model == 'RAP' or model == 'RAP 32':
            ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
        else:
            ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
        
    if data == True:
        ds = ds


    if model == 'CMCENS' or model == 'GEFS0p50':
        ds['absvprs'] = mpcalc.vorticity((ds['ugrdprs'][0, :, level_idx, :, :] * units('m/s')), (ds['vgrdprs'][0, :, level_idx, :, :] * units('m/s')))

    if model == 'RAP' or model == 'RAP 32':
        ds['absvprs'] = mpcalc.vorticity((ds['ugrdprs'][:, level_idx, :, :] * units('m/s')), (ds['vgrdprs'][:, level_idx, :, :] * units('m/s')))

    cmap = colormaps.vorticity_colormap()

    end = len(ds['time']) - 1
    time = ds['time']
    times = time.to_pandas()


    path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Height Vorticity Wind', str_level)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass
    
    for t in range(0, end, step):
    
        fname = f"Image_{t}.png"
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
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

        model = model.upper()
        plt.title(f"{model} {str_level} GPH [DM]/ABS VORT [1/S]/WIND [KTS]", fontsize=9, fontweight='bold', loc='left')
        plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
        
        lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
        
        stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                            transform=ccrs.PlateCarree(), zorder=3, fontsize=5, clip_on=True)


        if model == 'CMCENS' or model == 'GEFS0P50':

            stn.plot_barb((ds['ugrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)

            if level == 500:
                c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='darkblue', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='darkred', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)

            else:                
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
                
            cs = ax.contourf(ds['lon'], ds['lat'], abs(ds['absvprs'][t, :, :]), cmap=cmap, transform=datacrs, levels=np.arange(0, 55e-5, 50e-6), alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', format="{x:.0e}")

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)


        else:
            
            stn.plot_barb((ds['ugrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)

            if level == 500:
                c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='darkblue', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='darkred', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)

            else:
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
            try:
                cs = ax.contourf(ds['lon'], ds['lat'], abs(ds['absvprs'][t, level_idx, :, :]), cmap=cmap, transform=datacrs, levels=np.arange(0, 55e-5, 50e-6), alpha=0.35, extend='max')
            except Exception as e:
                cs = ax.contourf(ds['lon'], ds['lat'], abs(ds['absvprs'][t, :, :]), cmap=cmap, transform=datacrs, levels=np.arange(0, 55e-5, 50e-6), alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', format="{x:.0e}")
    
            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
        
            if mapcrs == datacrs:
                tim.sleep(10)
    print(f"Saved forecast graphics to {path_print}.")


def plot_geopotential_height(model, region, level=500, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

    """
    This function plots the Geopotential Height Forecast for a specific level. 

    Required Arguments: 
    
    1) model (String) - This is the model the user must select. 
                            
        Here are the choices: 
        1) GFS0p25 - GFS 0.25x0.25 degree
        2) GFS0p50 - GFS 0.5x0.5 degree
        3) GFS1p00 - GFS 1.0x1.0 degree
        4) GEFS0p50 - GEFS 0.5x0.5 degree
        5) CMCENS - Canadian Ensemble
        6) NAM - North American Model
        7) NA NAM - 32km North American Model - Full North America

    2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                            To look at any state use the 2-letter abbreviation for the state in either all capitals
                            or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                            CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                            North America use either: NA, na, North America or north america. If the user wishes to use custom
                            boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                            the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                            'oscc' for South Ops. 

    Optional Arguments: 
    
    1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                            500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

    2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                        and passing the data in or if the function needs to download the data. A value of False means the data
                        is downloaded inside of the function while a value of True means the user is downloading the data outside
                        of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                        things, it is recommended to set this value to True and download the data outside of the function and pass
                        it in so that the amount of data requests on the host servers can be minimized. 

    3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                    in the dataset. If the user wishes to download the data inside of the function, this value is None. 

    4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                    

    7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

    8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
        Default setting is True. Users should change this value to False if they wish to hide rivers.

    9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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
                            

    10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide state borders. 

    11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide county borders. 

    12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display GACC borders. 

    13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display PSA borders.

    14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display CWA borders.

    15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

    16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

    17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

    18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

    19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

    20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

    21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

    22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

    23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

    24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

    25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
        To change to a dashed line, users should set state_border_linestyle='--'. 

    26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
        To change to a dashed line, users should set county_border_linestyle='--'. 

    27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
        To change to a dashed line, users should set gacc_border_linestyle='--'. 

    28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'.    

    32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

    38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                        This is a feature of matplotlib, as per their definition, the shrink is:
                                        "Fraction by which to multiply the size of the colorbar." 
                                        This should only be changed if the user wishes to make a custom plot. 
                                        Preset values are called from the settings module for each region. 

    39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                when making a custom plot. 

    40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

    43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

    44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


    Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

    """

    data=data
    level=level
    ds=ds
    western_bound=western_bound
    eastern_bound=eastern_bound 
    southern_bound=southern_bound
    northern_bound=northern_bound
    show_rivers=show_rivers
    reference_system=reference_system
    state_border_linewidth=state_border_linewidth
    county_border_linewidth=county_border_linewidth
    gacc_border_linewidth=gacc_border_linewidth
    psa_border_linewidth=psa_border_linewidth 
    cwa_border_linewidth=cwa_border_linewidth
    nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
    nws_public_zones_linewidth=nws_public_zones_linewidth 
    state_border_linestyle=state_border_linestyle
    county_border_linestyle=county_border_linestyle
    gacc_border_linestyle=gacc_border_linestyle
    psa_border_linestyle=psa_border_linestyle 
    cwa_border_linestyle=cwa_border_linestyle
    nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
    nws_public_zones_linestyle=nws_public_zones_linestyle
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
        mapcrs = ccrs.LambertConformal()
    else:
        mapcrs = ccrs.PlateCarree()

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

    str_level = f"{level} MB"

    if level == 850:
        levels = np.arange(96, 180, 4)
        ticks = levels[::2]
    if level == 700:
        levels = np.arange(240, 340, 4)
        ticks = levels[::2]
    if level == 500:
        levels = np.arange(480, 604, 4)
        ticks = levels[::2]
    if level == 300:
        levels = np.arange(840, 1020, 10)
        ticks = levels[::2]
    if level == 250:
        levels = np.arange(900, 1140, 10)
        ticks = levels[::2]
    if level == 200:
        levels = np.arange(1000, 1280, 10)
        ticks = levels[::2]
    

    if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
        decimate = 20
        step = 1
        
        if level == 850:
            level_idx = 6
        if level == 700:
            level_idx = 12
        if level == 500:
            level_idx = 20
        if level == 300:
            level_idx = 28
        if level == 250:
            level_idx = 30
        if level == 200:
            level_idx = 32
    
    if model == 'CMCENS' or model == 'GEFS0p50':
        decimate = 10
        step = 1

        if level == 850:
            level_idx = 2
        if level == 700:
            level_idx = 3
        if level == 500:
            level_idx = 4
        if level == 300:
            level_idx = 6
        if level == 250:
            level_idx = 7
        if level == 200:
            level_idx = 8
        
    if model == 'GFS0p25' or model == 'GFS0p25_1h':
        decimate = 10
        step = 2
        
        if level == 850:
            level_idx = 5
        if level == 700:
            level_idx = 8
        if level == 500:
            level_idx = 12
        if level == 300:
            level_idx = 16
        if level == 250:
            level_idx = 17
        if level == 200:
            level_idx = 18
        
    if model == 'GFS0p50':
        decimate = 10
        step = 2
        
        if level == 850:
            level_idx = 6
        if level == 700:
            level_idx = 12
        if level == 500:
            level_idx = 20
        if level == 300:
            level_idx = 28
        if level == 250:
            level_idx = 30
        if level == 200:
            level_idx = 32
    
    if model == 'GFS1p00':
        decimate = 10
        step = 2

        if level == 850:
            level_idx = 5
        if level == 700:
            level_idx = 8
        if level == 500:
            level_idx = 12
        if level == 300:
            level_idx = 16
        if level == 250:
            level_idx = 17
        if level == 200:
            level_idx = 18

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
        wb=western_bound
        eb=eastern_bound
        sb=southern_bound
        nb=northern_bound
        x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
    else:
        wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
        sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
    
    if data == False:
        if model == 'RAP' or model == 'RAP 32':
            ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
        else:
            ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
        
    if data == True:
        ds = ds

    cmap = colormaps.gph_colormap()

    end = len(ds['time']) - 1
    time = ds['time']
    times = time.to_pandas()


    path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Geopotential Height', str_level)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass
    
    for t in range(0, end, step):
    
        fname = f"Image_{t}.png"
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
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

        model = model.upper()
        plt.title(f"{model} {str_level} GEOPOTENTIAL HEIGHT [DM]", fontsize=9, fontweight='bold', loc='left')
        plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)


        if model == 'CMCENS' or model == 'GEFS0P50':
                
            c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
            ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
                
            cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)

            if mapcrs == datacrs:
                tim.sleep(10)


        else:
            
            c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
            ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
            
            cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)
    print(f"Saved forecast graphics to {path_print}.")

def plot_24hr_geopotential_height_change(model, region, level=500, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

    """
    This function plots the 24-Hour Gepotential Height Change Forecast for a specific level. 

    Required Arguments: 
    
    1) model (String) - This is the model the user must select. 
                            
        Here are the choices: 
        1) GFS0p25 - GFS 0.25x0.25 degree
        2) GFS0p50 - GFS 0.5x0.5 degree
        3) GFS1p00 - GFS 1.0x1.0 degree
        4) GEFS0p50 - GEFS 0.5x0.5 degree
        5) CMCENS - Canadian Ensemble
        6) NAM - North American Model
        7) NA NAM - 32km North American Model - Full North America
        
    2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                            To look at any state use the 2-letter abbreviation for the state in either all capitals
                            or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                            CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                            North America use either: NA, na, North America or north america. If the user wishes to use custom
                            boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                            the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                            'oscc' for South Ops. 

    Optional Arguments: 
    
    1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                            500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

    2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                        and passing the data in or if the function needs to download the data. A value of False means the data
                        is downloaded inside of the function while a value of True means the user is downloading the data outside
                        of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                        things, it is recommended to set this value to True and download the data outside of the function and pass
                        it in so that the amount of data requests on the host servers can be minimized. 

    3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                    in the dataset. If the user wishes to download the data inside of the function, this value is None. 

    4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                    

    7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

    8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
        Default setting is True. Users should change this value to False if they wish to hide rivers.

    9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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
                            

    10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide state borders. 

    11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide county borders. 

    12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display GACC borders. 

    13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display PSA borders.

    14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display CWA borders.

    15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

    16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

    17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

    18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

    19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

    20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

    21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

    22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

    23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

    24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

    25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
        To change to a dashed line, users should set state_border_linestyle='--'. 

    26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
        To change to a dashed line, users should set county_border_linestyle='--'. 

    27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
        To change to a dashed line, users should set gacc_border_linestyle='--'. 

    28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'.    

    32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

    38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                        This is a feature of matplotlib, as per their definition, the shrink is:
                                        "Fraction by which to multiply the size of the colorbar." 
                                        This should only be changed if the user wishes to make a custom plot. 
                                        Preset values are called from the settings module for each region. 

    39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                when making a custom plot. 

    40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

    43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

    44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


    Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

    """

    data=data
    level=level
    ds=ds
    western_bound=western_bound
    eastern_bound=eastern_bound 
    southern_bound=southern_bound
    northern_bound=northern_bound
    show_rivers=show_rivers
    reference_system=reference_system
    state_border_linewidth=state_border_linewidth
    county_border_linewidth=county_border_linewidth
    gacc_border_linewidth=gacc_border_linewidth
    psa_border_linewidth=psa_border_linewidth 
    cwa_border_linewidth=cwa_border_linewidth
    nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
    nws_public_zones_linewidth=nws_public_zones_linewidth 
    state_border_linestyle=state_border_linestyle
    county_border_linestyle=county_border_linestyle
    gacc_border_linestyle=gacc_border_linestyle
    psa_border_linestyle=psa_border_linestyle 
    cwa_border_linestyle=cwa_border_linestyle
    nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
    nws_public_zones_linestyle=nws_public_zones_linestyle
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
        mapcrs = ccrs.LambertConformal()
    else:
        mapcrs = ccrs.PlateCarree()

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

    str_level = f"{level} MB"

    levels = np.arange(-30, 31, 1)
    ticks = levels[::5]

    negative = np.arange(-30, 5, 5)
    positive = np.arange(5, 35, 5)
    
    
    if model == 'CMCENS' or model == 'GEFS0p50':
        increment = 4
        step = 1

        if level == 850:
            level_idx = 2
        if level == 700:
            level_idx = 3
        if level == 500:
            level_idx = 4
        if level == 300:
            level_idx = 6
        if level == 250:
            level_idx = 7
        if level == 200:
            level_idx = 8
        
    if model == 'GFS0p25' or model == 'GFS0p25_1h':
        step = 2
        increment = 8
        
        if level == 850:
            level_idx = 5
        if level == 700:
            level_idx = 8
        if level == 500:
            level_idx = 12
        if level == 300:
            level_idx = 16
        if level == 250:
            level_idx = 17
        if level == 200:
            level_idx = 18
        
    if model == 'GFS0p50':
        step = 2
        increment = 8
        
        if level == 850:
            level_idx = 6
        if level == 700:
            level_idx = 12
        if level == 500:
            level_idx = 20
        if level == 300:
            level_idx = 28
        if level == 250:
            level_idx = 30
        if level == 200:
            level_idx = 32
    
    if model == 'GFS1p00':
        step = 2
        increment = 8
        
        if level == 850:
            level_idx = 5
        if level == 700:
            level_idx = 8
        if level == 500:
            level_idx = 12
        if level == 300:
            level_idx = 16
        if level == 250:
            level_idx = 17
        if level == 200:
            level_idx = 18

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
        wb=western_bound
        eb=eastern_bound
        sb=southern_bound
        nb=northern_bound
        x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
    else:
        wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
        sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
    
    if data == False:
        if model == 'RAP' or model == 'RAP 32':
            ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
        else:
            ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
        
    if data == True:
        ds = ds

    cmap = colormaps.gph_change_colormap()

    end = len(ds['time']) - 1
    time = ds['time']
    times = time.to_pandas()


    path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, '24-Hour Geopotential Height Change', str_level)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass
    
    for t in range(0, end, step):

        t1 = t + increment
    
        fname = f"Image_{t}.png"
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
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

        model = model.upper()
        plt.title(f"{model} {str_level} 24-HR GEOPOTENTIAL HEIGHT CHANGE [ΔDM]", fontsize=9, fontweight='bold', loc='left')
        try:
            plt.title("Forecast Valid: " +times.iloc[t1].strftime('%a %d/%H UTC')+" - "+times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
        except Exception as e:
            pass
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)


        if model == 'CMCENS' or model == 'GEFS0P50':

            try:

                c_low = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][0, t1, level_idx, :, :] - ds['hgtprs'][0, t, level_idx, :, :])/10), levels=negative, colors='blue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                ax.clabel(c_low, levels=negative, inline=True, fontsize=8, rightside_up=True)
    
                c = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][0, t1, level_idx, :, :] - ds['hgtprs'][0, t, level_idx, :, :])/10), levels=[0], colors='black', zorder=2, transform=datacrs, linewidths=1, linestyles='-')
                ax.clabel(c, levels=[0], inline=True, fontsize=8, rightside_up=True)
    
                c_high = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][0, t1, level_idx, :, :] - ds['hgtprs'][0, t, level_idx, :, :])/10), levels=positive, colors='red', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                ax.clabel(c_high, levels=positive, inline=True, fontsize=8, rightside_up=True)
                    
                cs = ax.contourf(ds['lon'], ds['lat'], ((ds['hgtprs'][0, t1, level_idx, :, :] - ds['hgtprs'][0, t, level_idx, :, :])/10), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)

            except Exception as e:
                pass


        else:

            try:
                c_low = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][t1, level_idx, :, :] - ds['hgtprs'][t, level_idx, :, :])/10), levels=negative, colors='blue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                ax.clabel(c_low, levels=negative, inline=True, fontsize=8, rightside_up=True)
    
                c_high = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][t1, level_idx, :, :] - ds['hgtprs'][t, level_idx, :, :])/10), levels=positive, colors='red', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                ax.clabel(c_high, levels=positive, inline=True, fontsize=8, rightside_up=True)
    
                c = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][t1, level_idx, :, :] - ds['hgtprs'][t, level_idx, :, :])/10), levels=[0], colors='black', zorder=2, transform=datacrs, linewidths=1, linestyles='-')
                ax.clabel(c, levels=[0], inline=True, fontsize=8, rightside_up=True)
                
                cs = ax.contourf(ds['lon'], ds['lat'], ((ds['hgtprs'][t1, level_idx, :, :] - ds['hgtprs'][t, level_idx, :, :])/10), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
            except Exception as e:
                pass
    print(f"Saved forecast graphics to {path_print}.")

def plot_geopotential_height_and_wind(model, region, level=250, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

    """
    This function plots the Geopotential Height/Wind Forecast for a specific level. 

    Required Arguments: 
    
    1) model (String) - This is the model the user must select. 
                            
        Here are the choices: 
        1) GFS0p25 - GFS 0.25x0.25 degree
        2) GFS0p50 - GFS 0.5x0.5 degree
        3) GFS1p00 - GFS 1.0x1.0 degree
        4) GEFS0p50 - GEFS 0.5x0.5 degree
        5) CMCENS - Canadian Ensemble
        6) NAM - North American Model
        7) NA NAM - 32km North American Model - Full North America

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                        To look at any state use the 2-letter abbreviation for the state in either all capitals
                        or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                        CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                        North America use either: NA, na, North America or north america. If the user wishes to use custom
                        boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                        the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                        'oscc' for South Ops. 

    Optional Arguments: 
    
    1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                            500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

    2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                        and passing the data in or if the function needs to download the data. A value of False means the data
                        is downloaded inside of the function while a value of True means the user is downloading the data outside
                        of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                        things, it is recommended to set this value to True and download the data outside of the function and pass
                        it in so that the amount of data requests on the host servers can be minimized. 

    3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                    in the dataset. If the user wishes to download the data inside of the function, this value is None. 

    4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                    

    7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

    8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
        Default setting is True. Users should change this value to False if they wish to hide rivers.

    9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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
                            

    10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide state borders. 

    11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide county borders. 

    12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display GACC borders. 

    13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display PSA borders.

    14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display CWA borders.

    15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

    16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

    17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

    18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

    19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

    20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

    21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

    22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

    23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

    24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

    25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
        To change to a dashed line, users should set state_border_linestyle='--'. 

    26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
        To change to a dashed line, users should set county_border_linestyle='--'. 

    27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
        To change to a dashed line, users should set gacc_border_linestyle='--'. 

    28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'.    

    32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

    38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                        This is a feature of matplotlib, as per their definition, the shrink is:
                                        "Fraction by which to multiply the size of the colorbar." 
                                        This should only be changed if the user wishes to make a custom plot. 
                                        Preset values are called from the settings module for each region. 

    39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                when making a custom plot. 

    40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

    43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

    44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


    Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

    """

    data=data
    level=level
    ds=ds
    western_bound=western_bound
    eastern_bound=eastern_bound 
    southern_bound=southern_bound
    northern_bound=northern_bound
    show_rivers=show_rivers
    reference_system=reference_system
    state_border_linewidth=state_border_linewidth
    county_border_linewidth=county_border_linewidth
    gacc_border_linewidth=gacc_border_linewidth
    psa_border_linewidth=psa_border_linewidth 
    cwa_border_linewidth=cwa_border_linewidth
    nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
    nws_public_zones_linewidth=nws_public_zones_linewidth 
    state_border_linestyle=state_border_linestyle
    county_border_linestyle=county_border_linestyle
    gacc_border_linestyle=gacc_border_linestyle
    psa_border_linestyle=psa_border_linestyle 
    cwa_border_linestyle=cwa_border_linestyle
    nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
    nws_public_zones_linestyle=nws_public_zones_linestyle
    x1=x1 
    y1=y1
    x2=x2
    y2=y2 
    x3=x3
    y3=y3 
    shrink=shrink
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
        mapcrs = ccrs.LambertConformal()
    else:
        mapcrs = ccrs.PlateCarree()

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

        str_level = f"{level} MB"
    
        if level == 850:
            levels = np.arange(96, 180, 4)
            speeds = np.arange(20, 101, 1)
            ticks = speeds[::5]
        if level == 700:
            levels = np.arange(240, 340, 4)
            speeds = np.arange(20, 101, 1)
            ticks = speeds[::5]
        if level == 500:
            speeds = np.arange(40, 121, 1)
            ticks = speeds[::5]
        if level == 300:
            levels = np.arange(840, 1020, 10)
            speeds = np.arange(80, 161, 1)
            ticks = speeds[::5]
        if level == 250:
            levels = np.arange(900, 1140, 10)
            speeds = np.arange(80, 161, 1)
            ticks = speeds[::5]
        if level == 200:
            levels = np.arange(1000, 1280, 10)
            speeds = np.arange(80, 161, 1)
            ticks = speeds[::5]
        
    
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            decimate = 20
            step = 1
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 10
            step = 1
    
            if level == 850:
                level_idx = 2
            if level == 700:
                level_idx = 3
            if level == 500:
                level_idx = 4
            if level == 300:
                level_idx = 6
            if level == 250:
                level_idx = 7
            if level == 200:
                level_idx = 8
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
            
        if model == 'GFS0p50':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'GFS1p00':
            decimate = 10
            step = 2
    
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18


    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
        wb=western_bound
        eb=eastern_bound
        sb=southern_bound
        nb=northern_bound
        x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
    else:
        wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
        sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
    
    if data == False:
        if model == 'RAP' or model == 'RAP 32':
            ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
        else:
            ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
        
    if data == True:
        ds = ds

    cmap = colormaps.wind_speed_colormap()

    end = len(ds['time']) - 1
    time = ds['time']
    times = time.to_pandas()


    path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Geopotential Height & Wind', str_level)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass
    
    for t in range(0, end, step):
    
        fname = f"Image_{t}.png"
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
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

        model = model.upper()
        plt.title(f"{model} {str_level} GEOPOTENTIAL HEIGHT [DM] & WIND [KTS]", fontsize=9, fontweight='bold', loc='left')
        plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
        
        lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
        
        stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                            transform=ccrs.PlateCarree(), zorder=3, fontsize=6, clip_on=True)


        if model == 'CMCENS' or model == 'GEFS0P50':
    
            stn.plot_barb((ds['ugrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)

            if level == 500:
                c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='darkblue', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='darkred', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)

            else:                
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
                
            cs = ax.contourf(ds['lon'], ds['lat'], (mpcalc.wind_speed((ds['ugrdprs'][0, t, level_idx, :, :] *units('m/s')), (ds['vgrdprs'][0, t, level_idx, :, :] *units('m/s'))) * 1.94384), cmap=cmap, transform=datacrs, levels=speeds, alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)


        else:
            
            stn.plot_barb((ds['ugrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)

            if level == 500:
                c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='darkblue', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='darkred', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)

            else:
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
            
            cs = ax.contourf(ds['lon'], ds['lat'], (mpcalc.wind_speed((ds['ugrdprs'][t, level_idx, :, :] *units('m/s')), (ds['vgrdprs'][t, level_idx, :, :] *units('m/s'))) * 1.94384), cmap=cmap, transform=datacrs, levels=speeds, alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)
    print(f"Saved forecast graphics to {path_print}.")

def plot_10m_winds_mslp(model, region, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

    """
    This function plots the 10-Meter Wind/MSLP Forecast. 

    Required Arguments: 
    
    1) model (String) - This is the model the user must select. 
                            
        Here are the choices: 
        1) GFS0p25 - GFS 0.25x0.25 degree
        2) GFS0p50 - GFS 0.5x0.5 degree
        3) GFS1p00 - GFS 1.0x1.0 degree
        4) GEFS0p50 - GEFS 0.5x0.5 degree
        5) CMCENS - Canadian Ensemble
        6) NAM - North American Model
        7) NA NAM - 32km North American Model - Full North America
        8) RAP - Rapid Refresh Model
        9) RAP 32 - 32km Rapid Refresh Model - Full North America

    2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                            To look at any state use the 2-letter abbreviation for the state in either all capitals
                            or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                            CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                            North America use either: NA, na, North America or north america. If the user wishes to use custom
                            boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                            the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                            'oscc' for South Ops. 

    Optional Arguments: 
    
    1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                        and passing the data in or if the function needs to download the data. A value of False means the data
                        is downloaded inside of the function while a value of True means the user is downloading the data outside
                        of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                        things, it is recommended to set this value to True and download the data outside of the function and pass
                        it in so that the amount of data requests on the host servers can be minimized. 

    2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                    in the dataset. If the user wishes to download the data inside of the function, this value is None. 

    3) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    4) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    5) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                    

    6) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

    7) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
        Default setting is True. Users should change this value to False if they wish to hide rivers.

    8) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                            

    9) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide state borders. 

    10) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide county borders. 

    11) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display GACC borders. 

    12) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display PSA borders.

    13) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display CWA borders.

    14) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

    15) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

    16) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

    17) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

    18) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

    19) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

    20) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

    21) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

    22) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

    23) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

    24) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
        To change to a dashed line, users should set state_border_linestyle='--'. 

    25) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
        To change to a dashed line, users should set county_border_linestyle='--'. 

    26) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
        To change to a dashed line, users should set gacc_border_linestyle='--'. 

    27) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    28) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    29) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    30) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'.    

    31) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    32) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    33) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    34) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    35) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    36) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

    37) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                        This is a feature of matplotlib, as per their definition, the shrink is:
                                        "Fraction by which to multiply the size of the colorbar." 
                                        This should only be changed if the user wishes to make a custom plot. 
                                        Preset values are called from the settings module for each region. 

    38) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                when making a custom plot. 

    39) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    40) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    41) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

    42) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

    43) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


    Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

    """

    data=data
    ds=ds
    western_bound=western_bound
    eastern_bound=eastern_bound 
    southern_bound=southern_bound
    northern_bound=northern_bound
    show_rivers=show_rivers
    reference_system=reference_system
    state_border_linewidth=state_border_linewidth
    county_border_linewidth=county_border_linewidth
    gacc_border_linewidth=gacc_border_linewidth
    psa_border_linewidth=psa_border_linewidth 
    cwa_border_linewidth=cwa_border_linewidth
    nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
    nws_public_zones_linewidth=nws_public_zones_linewidth 
    state_border_linestyle=state_border_linestyle
    county_border_linestyle=county_border_linestyle
    gacc_border_linestyle=gacc_border_linestyle
    psa_border_linestyle=psa_border_linestyle 
    cwa_border_linestyle=cwa_border_linestyle
    nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
    nws_public_zones_linestyle=nws_public_zones_linestyle
    x1=x1 
    y1=y1
    x2=x2
    y2=y2 
    x3=x3
    y3=y3 
    shrink=shrink
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
        mapcrs = ccrs.LambertConformal()
    else:
        mapcrs = ccrs.PlateCarree()

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

    str_level = f"SURFACE"

    mslp_levels = np.arange(850, 1104, 4)
    speeds = np.arange(10, 81, 1)
    mslp_labels = mslp_levels
    speed_ticks = speeds[::5]

    if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
        step = 1
    
    if model == 'CMCENS' or model == 'GEFS0p50':
        step = 1
        
    if model == 'GFS0p25' or model == 'GFS0p25_1h':
        step = 2
        
    if model == 'GFS0p50':
        step = 2
    
    if model == 'GFS1p00':
        step = 2


    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
        wb=western_bound
        eb=eastern_bound
        sb=southern_bound
        nb=northern_bound
        x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
    else:
        wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
        sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
    
    if data == False:
        if model == 'RAP' or model == 'RAP 32':
            ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
        else:
            ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
        
    if data == True:
        ds = ds

    cmap = colormaps.cross_section_wind_speed()

    end = len(ds['time']) - 1
    time = ds['time']
    times = time.to_pandas()


    path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, '10m Wind & MSLP', str_level)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass
    
    for t in range(0, end, step):
    
        fname = f"Image_{t}.png"
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
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

        model = model.upper()
        plt.title(f"{model} MSLP [MB] & 10M WIND [MPH]", fontsize=9, fontweight='bold', loc='left')
        plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
        
        lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
        
        stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                            transform=ccrs.PlateCarree(), zorder=3, fontsize=6, clip_on=True)


        if model == 'CMCENS' or model == 'GEFS0P50':

            stn.plot_barb((ds['ugrd10m'][0, t, ::decimate, ::decimate] * 2.23694), (ds['vgrd10m'][0, t, ::decimate, ::decimate] * 2.23694), color='black', alpha=1, zorder=3, linewidth=0.5)
                
            c = ax.contour(ds['lon'], ds['lat'], (ds['prmslmsl'][0, t, :, :]/100), levels=mslp_levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
            ax.clabel(c, levels=mslp_levels, inline=True, fontsize=8, rightside_up=True)
                
            cs = ax.contourf(ds['lon'], ds['lat'], (mpcalc.wind_speed((ds['ugrd10m'][0, t, :, :] *units('m/s')), (ds['vgrd10m'][0, t, :, :] *units('m/s'))) * 2.23694), cmap=cmap, transform=datacrs, levels=speeds, alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=speed_ticks)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)


        else:
            
            stn.plot_barb((ds['ugrd10m'][t, ::decimate, ::decimate] * 2.23694), (ds['vgrd10m'][t, ::decimate, ::decimate] * 2.23694), color='black', alpha=1, zorder=3, linewidth=0.5)

            c = ax.contour(ds['lon'], ds['lat'], (ds['prmslmsl'][t, :, :]/100), levels=mslp_levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
            ax.clabel(c, levels=mslp_levels, inline=True, fontsize=8, rightside_up=True)
            
            cs = ax.contourf(ds['lon'], ds['lat'], (mpcalc.wind_speed((ds['ugrd10m'][t, :, :] *units('m/s')), (ds['vgrd10m'][t, :, :] *units('m/s'))) * 2.23694), cmap=cmap, transform=datacrs, levels=speeds, alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=speed_ticks)
    
            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)
    print(f"Saved forecast graphics to {path_print}.")