"""
This file hosts 8-Day stats graphics for forecast ensemble data. 

This includes the following: 

1) Period Mean
2) EOF1
3) EOF2
4) EOF1 Scores

(C) Eric J. Drewitz 2025
"""
import xeofs as xe
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
from cartopy.util import add_cyclic_point

def plot_geopotential_height(model, hemisphere, level=500, data=False, ds=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

    """
    This function plots the following 8-Day Statistics over a period of 16-Days:

    1) Mean 500MB Geopotential Height
    2) EOF1 Geopotential Height
    3) EOF2 Geopotential Height
    4) EOF1 Scores Geopotential Height
    5) EOF2 Scores Geopotential Height

    Required Arguments: 
    
    1) model (String) - This is the model the user must select. 
                            
        Here are the choices: 
        1) GEFS0p50 - GEFS 0.5x0.5 degree
        2) CMCENS - Canadian Ensemble

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
    
    shrink = 0.8

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

    if hemisphere == 'N':
        mapcrs = ccrs.NorthPolarStereo()
        region ='custom'
        region_name = 'NORTHERN HEMISPHERE'
        wb = 360
        eb = 0
        sb = 25
        nb = 90

    if hemisphere == 'S':
        mapcrs = ccrs.SouthPolarStereo()
        region ='custom'
        region_name = 'SOUTHERN HEMISPHERE'
        wb = 360
        eb = 0
        sb = -90
        nb = -25
    
    if data == False:
        ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
        
    if data == True:
        ds = ds

    cmap = colormaps.gph_colormap()

    end = len(ds['time']) - 1
    ds1 = ds.sel(ens=ds['ens'][0], time=ds['time'][0:33])
    ds2 = ds.sel(ens=ds['ens'][0], time=ds['time'][32:65])
    time_1 = ds1['time']
    times_1 = time_1.to_pandas()
    time_2 = ds2['time']
    times_2 = time_2.to_pandas() 

    model_1 = xe.single.EOF(use_coslat=True)
    model_1.fit(ds1['hgtprs'], dim="time")
    model_1.explained_variance_ratio()
    components_1 = model_1.components()
    scores_1 = model_1.scores()
    avg_1 = ds1['hgtprs'].mean(dim='time')

    model_2 = xe.single.EOF(use_coslat=True)
    model_2.fit(ds2['hgtprs'], dim="time")
    model_2.explained_variance_ratio()
    components_2 = model_2.components()
    scores_2 = model_2.scores()
    avg_2 = ds2['hgtprs'].mean(dim='time')

    avg_1_lon = avg_1['lon']
    avg_1_lon_idx = avg_1.dims.index('lon')
    cyclic_avg_1, cyclic_avg_lon_1 = add_cyclic_point(avg_1.values, coord=avg_1_lon, axis=avg_1_lon_idx)

    avg_2_lon = avg_2['lon']
    avg_2_lon_idx = avg_2.dims.index('lon')
    cyclic_avg_2, cyclic_avg_lon_2 = add_cyclic_point(avg_2.values, coord=avg_2_lon, axis=avg_2_lon_idx)

    eofs_1_lon = components_1['lon']
    eofs_1_lon_idx = components_1.dims.index('lon')
    cyclic_eof_1, cyclic_eof_lon_1 = add_cyclic_point(components_1, coord=eofs_1_lon, axis=eofs_1_lon_idx)

    eofs_2_lon = components_2['lon']
    eofs_2_lon_idx = components_2.dims.index('lon')
    cyclic_eof_2, cyclic_eof_lon_2 = add_cyclic_point(components_2, coord=eofs_2_lon, axis=eofs_2_lon_idx)

    eof_levels_1_1 = np.arange(np.nanmin(components_1[0, level_idx, :, :]), (np.nanmax(components_1[0, level_idx, :, :]) + 0.00005), 0.00005)
    eof_levels_1_2 = np.arange(np.nanmin(components_2[0, level_idx, :, :]), (np.nanmax(components_2[0, level_idx, :, :]) + 0.00005), 0.00005)

    eof_levels_2_1 = np.arange(np.nanmin(components_1[1, level_idx, :, :]), (np.nanmax(components_1[1, level_idx, :, :]) + 0.00005), 0.00005)
    eof_levels_2_2 = np.arange(np.nanmin(components_2[1, level_idx, :, :]), (np.nanmax(components_2[1, level_idx, :, :]) + 0.00005), 0.00005)
    
    avg_1_levels = np.arange(int(round((np.nanmin(avg_1[level_idx, :, :])/10),0)), (int(round((np.nanmax(avg_1[level_idx, :, :])/10),0)) + 1), 1)
    ticks_1 = avg_1_levels[::3]
    avg_2_levels = np.arange(int(round(np.nanmin((avg_2[level_idx, :, :])/10),0)), (int(round((np.nanmax(avg_2[level_idx, :, :])/10),0)) + 1), 1)
    ticks_2 = avg_2_levels[::3]

    path1, path2, path3, path4, path5 = file_functions.forecast_model_eofs_paths(model, region_name, reference_system, 'Geopotential Height', str_level)

    for file in os.listdir(f"{path1}"):
        try:
            os.remove(f"{path1}/{file}")
        except Exception as e:
            pass

    for file in os.listdir(f"{path2}"):
        try:
            os.remove(f"{path2}/{file}")
        except Exception as e:
            pass

    for file in os.listdir(f"{path3}"):
        try:
            os.remove(f"{path3}/{file}")
        except Exception as e:
            pass

    for file in os.listdir(f"{path4}"):
        try:
            os.remove(f"{path4}/{file}")
        except Exception as e:
            pass

    for file in os.listdir(f"{path5}"):
        try:
            os.remove(f"{path5}/{file}")
        except Exception as e:
            pass
    
    for i in range(0, 2):
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=2)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=2)
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

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

        if i == 0:
            fname = f"PERIOD 1 AVG.png"
            plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} 8-DAY MEAN {str_level} GEOPOTENTIAL HEIGHT [DM]", fontsize=9, fontweight='bold', loc='left')
            cs = ax.contourf(cyclic_avg_lon_1, avg_1['lat'], (cyclic_avg_1[level_idx, :, :]/10), cmap=colormaps.gph_colormap(), levels=avg_1_levels, transform=datacrs, extend='both')
            c = ax.contour(cyclic_avg_lon_1, avg_1['lat'], (cyclic_avg_1[level_idx, :, :]/10), levels=avg_1_levels[::3], transform=datacrs, colors='black')
            ax.clabel(c, levels=avg_1_levels[::3], inline=True, fontsize=8, rightside_up=True)
            cbar = cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_1)
            fig.savefig(f"{path1}/{fname}", bbox_inches='tight')
            plt.close(fig)
            
        if i == 1:
            fname = f"PERIOD 2 AVG.png"
            plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} 8-DAY MEAN {str_level} GEOPOTENTIAL HEIGHT [DM]", fontsize=9, fontweight='bold', loc='left')
            cs = ax.contourf(cyclic_avg_lon_2, avg_2['lat'], (cyclic_avg_2[level_idx, :, :]/10), cmap=colormaps.gph_colormap(), levels=avg_2_levels, transform=datacrs, extend='both')
            c = ax.contour(cyclic_avg_lon_2, avg_2['lat'], (cyclic_avg_2[level_idx, :, :]/10), levels=avg_2_levels[::3], transform=datacrs, colors='black')
            ax.clabel(c, levels=avg_2_levels[::3], inline=True, fontsize=8, rightside_up=True)
            cbar = cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_2)
            fig.savefig(f"{path1}/{fname}", bbox_inches='tight')
            plt.close(fig)

            print(f"Saved Averages to f:{path1}")
        
        if mapcrs == datacrs:
            tim.sleep(10)


    for i in range(0, 2):
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=2)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=2)
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

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

        if i == 0:
            fname = f"PERIOD 1 EOF1.png"
            plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF1 {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
            ax.contourf(cyclic_eof_lon_1, components_1['lat'], cyclic_eof_1[0, level_idx, :, :], levels=eof_levels_1_1, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
            fig.savefig(f"{path2}/{fname}", bbox_inches='tight')
            plt.close(fig)

        if i == 1:
            fname = f"PERIOD 2 EOF1.png"
            plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF1 {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
            ax.contourf(cyclic_eof_lon_2, components_2['lat'], cyclic_eof_2[0, level_idx, :, :], levels=eof_levels_1_2, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
            fig.savefig(f"{path2}/{fname}", bbox_inches='tight')
            plt.close(fig)

            print(f"Saved Averages to f:{path2}")
        
        if mapcrs == datacrs:
            tim.sleep(10)     

    for i in range(0, 2):
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=2)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=2)
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

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

        if i == 0:
            fname = f"PERIOD 1 EOF2.png"
            plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF2 {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
            ax.contourf(cyclic_eof_lon_1, components_1['lat'], cyclic_eof_1[1, level_idx, :, :], levels=eof_levels_2_1, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
            fig.savefig(f"{path3}/{fname}", bbox_inches='tight')
            plt.close(fig)

        if i == 1:
            fname = f"PERIOD 2 EOF2.png"
            plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF2 {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
            ax.contourf(cyclic_eof_lon_2, components_2['lat'], cyclic_eof_2[1, level_idx, :, :], levels=eof_levels_2_2, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
            fig.savefig(f"{path3}/{fname}", bbox_inches='tight')
            plt.close(fig)

            print(f"Saved Averages to f:{path3}")
        
        if mapcrs == datacrs:
            tim.sleep(10)  


    for i in range(0, 2):
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1)
        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        ax.text(x1, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, -0.05, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

        if i == 0:
            fname = f"PERIOD 1 EOF1 SCORES.png"
            plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF1 SCORES {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
            ax.plot(scores_1['time'], scores_1[0, :], color='black')
            ax.fill_between(scores_1['time'], 0, scores_1[0, :], color='red', where=(scores_1[0, :] > 0), alpha=0.3)
            ax.fill_between(scores_1['time'], scores_1[0, :], 0, color='blue', where=(scores_1[0, :] < 0), alpha=0.3)
            fig.savefig(f"{path4}/{fname}", bbox_inches='tight')
            plt.close(fig)

        if i == 1:
            fname = f"PERIOD 2 EOF1 SCORES.png"
            plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF1 SCORES {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
            ax.plot(scores_2['time'], scores_2[0, :], color='black')
            ax.fill_between(scores_2['time'], 0, scores_2[0, :], color='red', where=(scores_2[0, :] > 0), alpha=0.3)
            ax.fill_between(scores_2['time'], scores_2[0, :], 0, color='blue', where=(scores_2[0, :] < 0), alpha=0.3)
            fig.savefig(f"{path4}/{fname}", bbox_inches='tight')
            plt.close(fig)

            print(f"Saved Averages to f:{path4}")
        
        if mapcrs == datacrs:
            tim.sleep(10)   

    for i in range(0, 2):
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1)
        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        ax.text(x1, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, -0.05, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

        if i == 0:
            fname = f"PERIOD 1 EOF2 SCORES.png"
            plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF2 SCORES {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
            ax.plot(scores_1['time'], scores_1[1, :], color='black')
            ax.fill_between(scores_1['time'], 0, scores_1[1, :], color='red', where=(scores_1[1, :] > 0), alpha=0.3)
            ax.fill_between(scores_1['time'], scores_1[1, :], 0, color='blue', where=(scores_1[1, :] < 0), alpha=0.3)
            fig.savefig(f"{path5}/{fname}", bbox_inches='tight')
            plt.close(fig)

        if i == 1:
            fname = f"PERIOD 2 EOF2 SCORES.png"
            plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF2 SCORES {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
            ax.plot(scores_2['time'], scores_2[1, :], color='black')
            ax.fill_between(scores_2['time'], 0, scores_2[1, :], color='red', where=(scores_2[1, :] > 0), alpha=0.3)
            ax.fill_between(scores_2['time'], scores_2[1, :], 0, color='blue', where=(scores_2[1, :] < 0), alpha=0.3)
            fig.savefig(f"{path5}/{fname}", bbox_inches='tight')
            plt.close(fig)

            print(f"Saved Averages to f:{path5}")
        
        if mapcrs == datacrs:
            tim.sleep(10)   


def plot_mslp(model, hemisphere, data=False, ds=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

    """
    This function plots the following 8-Day Statistics over a period of 16-Days:

    1) Mean MSLP
    2) EOF1 MSLP
    3) EOF2 MSLP
    4) EOF1 Scores MSLP
    5) EOF2 Scores MSLP

    Required Arguments: 
    
    1) model (String) - This is the model the user must select. 
                            
        Here are the choices: 
        1) GEFS0p50 - GEFS 0.5x0.5 degree
        2) CMCENS - Canadian Ensemble

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

    8) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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


    Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/SURFACE

    """

    data=data
    ds=ds
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
    
    shrink = 0.8

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
    
    if hemisphere == 'N':
        mapcrs = ccrs.NorthPolarStereo()
        region ='custom'
        region_name = 'NORTHERN HEMISPHERE'
        wb = 360
        eb = 0
        sb = 25
        nb = 90

    if hemisphere == 'S':
        mapcrs = ccrs.SouthPolarStereo()
        region ='custom'
        region_name = 'SOUTHERN HEMISPHERE'
        wb = 360
        eb = 0
        sb = -90
        nb = -25
    
    if data == False:
        ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
        
    if data == True:
        ds = ds

    cmap = colormaps.gph_colormap()

    end = len(ds['time']) - 1
    ds1 = ds.sel(ens=ds['ens'][0], time=ds['time'][0:33])
    ds2 = ds.sel(ens=ds['ens'][0], time=ds['time'][32:65])
    time_1 = ds1['time']
    times_1 = time_1.to_pandas()
    time_2 = ds2['time']
    times_2 = time_2.to_pandas() 

    model_1 = xe.single.EOF(use_coslat=True)
    model_1.fit(ds1['prmslmsl'], dim="time")
    model_1.explained_variance_ratio()
    components_1 = model_1.components()
    scores_1 = model_1.scores()
    avg_1 = ds1['prmslmsl'].mean(dim='time')

    model_2 = xe.single.EOF(use_coslat=True)
    model_2.fit(ds2['prmslmsl'], dim="time")
    model_2.explained_variance_ratio()
    components_2 = model_2.components()
    scores_2 = model_2.scores()
    avg_2 = ds2['prmslmsl'].mean(dim='time')
    
    avg_1 = avg_1/100
    avg_1_lon = avg_1['lon']
    avg_1_lon_idx = avg_1.dims.index('lon')
    cyclic_avg_1, cyclic_avg_lon_1 = add_cyclic_point(avg_1.values, coord=avg_1_lon, axis=avg_1_lon_idx)

    avg_2 = avg_2/100
    avg_2_lon = avg_2['lon']
    avg_2_lon_idx = avg_2.dims.index('lon')
    cyclic_avg_2, cyclic_avg_lon_2 = add_cyclic_point(avg_2.values, coord=avg_2_lon, axis=avg_2_lon_idx)

    eofs_1_lon = components_1['lon']
    eofs_1_lon_idx = components_1.dims.index('lon')
    cyclic_eof_1, cyclic_eof_lon_1 = add_cyclic_point(components_1, coord=eofs_1_lon, axis=eofs_1_lon_idx)

    eofs_2_lon = components_2['lon']
    eofs_2_lon_idx = components_2.dims.index('lon')
    cyclic_eof_2, cyclic_eof_lon_2 = add_cyclic_point(components_2, coord=eofs_2_lon, axis=eofs_2_lon_idx)

    eof_levels_1_1 = np.arange(np.nanmin(components_1[0, :, :]), (np.nanmax(components_1[0, :, :]) + 0.00005), 0.00005)
    eof_levels_1_2 = np.arange(np.nanmin(components_2[0, :, :]), (np.nanmax(components_2[0, :, :]) + 0.00005), 0.00005)

    eof_levels_2_1 = np.arange(np.nanmin(components_1[1, :, :]), (np.nanmax(components_1[1, :, :]) + 0.00005), 0.00005)
    eof_levels_2_2 = np.arange(np.nanmin(components_2[1, :, :]), (np.nanmax(components_2[1, :, :]) + 0.00005), 0.00005)
    
    avg_1_levels = np.arange(int(round(np.nanmin(avg_1[:, :]),0)), (int(round(np.nanmax(avg_1[:, :]),0)) + 1), 1)
    ticks_1 = avg_1_levels[::4]
    avg_2_levels = np.arange(int(round(np.nanmin(avg_2[:, :]),0)), (int(round(np.nanmax(avg_2[:, :]),0)) + 1), 1)
    ticks_2 = avg_2_levels[::4]

    path1, path2, path3, path4, path5 = file_functions.forecast_model_eofs_paths(model, region_name, reference_system, 'MSLP', str_level)

    for file in os.listdir(f"{path1}"):
        try:
            os.remove(f"{path1}/{file}")
        except Exception as e:
            pass

    for file in os.listdir(f"{path2}"):
        try:
            os.remove(f"{path2}/{file}")
        except Exception as e:
            pass

    for file in os.listdir(f"{path3}"):
        try:
            os.remove(f"{path3}/{file}")
        except Exception as e:
            pass

    for file in os.listdir(f"{path4}"):
        try:
            os.remove(f"{path4}/{file}")
        except Exception as e:
            pass

    for file in os.listdir(f"{path5}"):
        try:
            os.remove(f"{path5}/{file}")
        except Exception as e:
            pass
    
    for i in range(0, 2):
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=2)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=2)
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

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

        if i == 0:
            fname = f"PERIOD 1 AVG.png"
            plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} 8-DAY MEAN MSLP [hPa]", fontsize=9, fontweight='bold', loc='left')
            cs = ax.contourf(cyclic_avg_lon_1, avg_1['lat'], cyclic_avg_1[:, :], cmap=colormaps.gph_colormap(), levels=avg_1_levels, transform=datacrs, extend='both')
            c = ax.contour(cyclic_avg_lon_1, avg_1['lat'], cyclic_avg_1[:, :], levels=avg_1_levels[::3], transform=datacrs, colors='black')
            ax.clabel(c, levels=avg_1_levels[::3], inline=True, fontsize=8, rightside_up=True)
            cbar = cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_1)
            fig.savefig(f"{path1}/{fname}", bbox_inches='tight')
            plt.close(fig)
            
        if i == 1:
            fname = f"PERIOD 2 AVG.png"
            plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} 8-DAY MEAN MSLP [hPa]", fontsize=9, fontweight='bold', loc='left')
            cs = ax.contourf(cyclic_avg_lon_2, avg_2['lat'], cyclic_avg_2[:, :], cmap=colormaps.gph_colormap(), levels=avg_2_levels, transform=datacrs, extend='both')
            c = ax.contour(cyclic_avg_lon_2, avg_2['lat'], cyclic_avg_2[:, :], levels=avg_2_levels[::3], transform=datacrs, colors='black')
            ax.clabel(c, levels=avg_2_levels[::3], inline=True, fontsize=8, rightside_up=True)
            cbar = cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_2)
            fig.savefig(f"{path1}/{fname}", bbox_inches='tight')
            plt.close(fig)

            print(f"Saved Averages to f:{path1}")
        
        if mapcrs == datacrs:
            tim.sleep(10)


    for i in range(0, 2):
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=2)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=2)
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

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

        if i == 0:
            fname = f"PERIOD 1 EOF1.png"
            plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF1 8-DAY MEAN MSLP", fontsize=9, fontweight='bold', loc='left')
            ax.contourf(cyclic_eof_lon_1, components_1['lat'], cyclic_eof_1[0, :, :], levels=eof_levels_1_1, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
            fig.savefig(f"{path2}/{fname}", bbox_inches='tight')
            plt.close(fig)

        if i == 1:
            fname = f"PERIOD 2 EOF1.png"
            plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF1 8-DAY MEAN MSLP", fontsize=9, fontweight='bold', loc='left')
            ax.contourf(cyclic_eof_lon_2, components_2['lat'], cyclic_eof_2[0, :, :], levels=eof_levels_1_2, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
            fig.savefig(f"{path2}/{fname}", bbox_inches='tight')
            plt.close(fig)

            print(f"Saved Averages to f:{path2}")
        
        if mapcrs == datacrs:
            tim.sleep(10)     

    for i in range(0, 2):
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=2)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=2)
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

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

        if i == 0:
            fname = f"PERIOD 1 EOF2.png"
            plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF2 8-DAY MEAN MSLP", fontsize=9, fontweight='bold', loc='left')
            ax.contourf(cyclic_eof_lon_1, components_1['lat'], cyclic_eof_1[1, :, :], levels=eof_levels_2_1, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
            fig.savefig(f"{path3}/{fname}", bbox_inches='tight')
            plt.close(fig)

        if i == 1:
            fname = f"PERIOD 2 EOF2.png"
            plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF2 8-DAY MEAN MSLP", fontsize=9, fontweight='bold', loc='left')
            ax.contourf(cyclic_eof_lon_2, components_2['lat'], cyclic_eof_2[1, :, :], levels=eof_levels_2_2, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
            fig.savefig(f"{path3}/{fname}", bbox_inches='tight')
            plt.close(fig)

            print(f"Saved Averages to f:{path3}")
        
        if mapcrs == datacrs:
            tim.sleep(10)  


    for i in range(0, 2):
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1)
        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        ax.text(x1, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, -0.05, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

        if i == 0:
            fname = f"PERIOD 1 EOF1 SCORES.png"
            plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF1 SCORES 8-DAY MEAN MSLP", fontsize=9, fontweight='bold', loc='left')
            ax.plot(scores_1['time'], scores_1[0, :], color='black')
            ax.fill_between(scores_1['time'], 0, scores_1[0, :], color='red', where=(scores_1[0, :] > 0), alpha=0.3)
            ax.fill_between(scores_1['time'], scores_1[0, :], 0, color='blue', where=(scores_1[0, :] < 0), alpha=0.3)
            fig.savefig(f"{path4}/{fname}", bbox_inches='tight')
            plt.close(fig)

        if i == 1:
            fname = f"PERIOD 2 EOF1 SCORES.png"
            plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF1 SCORES 8-DAY MEAN MSLP", fontsize=9, fontweight='bold', loc='left')
            ax.plot(scores_2['time'], scores_2[0, :], color='black')
            ax.fill_between(scores_2['time'], 0, scores_2[0, :], color='red', where=(scores_2[0, :] > 0), alpha=0.3)
            ax.fill_between(scores_2['time'], scores_2[0, :], 0, color='blue', where=(scores_2[0, :] < 0), alpha=0.3)
            fig.savefig(f"{path4}/{fname}", bbox_inches='tight')
            plt.close(fig)

            print(f"Saved Averages to f:{path4}")
        
        if mapcrs == datacrs:
            tim.sleep(10)   

    for i in range(0, 2):
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1)
        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        ax.text(x1, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax.text(x2, -0.05, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

        if i == 0:
            fname = f"PERIOD 1 EOF2 SCORES.png"
            plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF2 SCORES 8-DAY MEAN MSLP", fontsize=9, fontweight='bold', loc='left')
            ax.plot(scores_1['time'], scores_1[1, :], color='black')
            ax.fill_between(scores_1['time'], 0, scores_1[1, :], color='red', where=(scores_1[1, :] > 0), alpha=0.3)
            ax.fill_between(scores_1['time'], scores_1[1, :], 0, color='blue', where=(scores_1[1, :] < 0), alpha=0.3)
            fig.savefig(f"{path5}/{fname}", bbox_inches='tight')
            plt.close(fig)

        if i == 1:
            fname = f"PERIOD 2 EOF2 SCORES.png"
            plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            plt.title(f"{model.upper()} EOF2 SCORES 8-DAY MEAN MSLP", fontsize=9, fontweight='bold', loc='left')
            ax.plot(scores_2['time'], scores_2[1, :], color='black')
            ax.fill_between(scores_2['time'], 0, scores_2[1, :], color='red', where=(scores_2[1, :] > 0), alpha=0.3)
            ax.fill_between(scores_2['time'], scores_2[1, :], 0, color='blue', where=(scores_2[1, :] < 0), alpha=0.3)
            fig.savefig(f"{path5}/{fname}", bbox_inches='tight')
            plt.close(fig)

            print(f"Saved Averages to f:{path5}")
        
        if mapcrs == datacrs:
            tim.sleep(10)   