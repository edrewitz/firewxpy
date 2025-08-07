"""
This class hosts the functions showing the temperature forecast.

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

mpl.rcParams['font.weight'] = 'bold'
local_time, utc_time = standard.plot_creation_time()

datacrs = ccrs.PlateCarree()

provinces = cfeature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale='50m', facecolor='none', edgecolor='k')

props = dict(boxstyle='round', facecolor='wheat', alpha=1)


def plot_2m_temperatures(model, region, start_of_warm_season_month=4, end_of_warm_season_month=10, start_of_cool_season_month=11, end_of_cool_season_month=3, temp_scale_warm_start=10, temp_scale_warm_stop=110, temp_scale_cool_start=-20, temp_scale_cool_stop=80, temp_scale_step=1, temperature_contour_value=32, data=False, ds=None, ds_list=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

    """
    This function plots the 2-Meter Temperature Forecast. 

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
        10) GEFS0p25 ENS MEAN - GEFS 0.25x0.25 degree Ensemble Mean

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                        To look at any state use the 2-letter abbreviation for the state in either all capitals
                        or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                        CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                        North America use either: NA, na, North America or north america. If the user wishes to use custom
                        boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                        the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                        'oscc' for South Ops. 

    Optional Arguments: 
    
    1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

    2) end_of_warm_season_month (Integer) - Default = 10 (October). The numeric value for the month the warm season ends. 

    3) start_of_cool_season_month (Integer) - Default = 11 (November). The numeric value for the month the cool season begins. 

    4) end_of_cool_season_month (Integer) - Default = 3 (March). The numeric value for the month the cool season ends.

    5) temp_scale_warm_start (Integer) - Default = 10. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

    6) temp_scale_warm_stop (Integer) - Default = 110. The top bound temperature value in Fahrenheit of the warm season temperature range.

    7) temp_scale_cool_start (Integer) - Default = -20. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

    8) temp_scale_cool_stop (Integer) - Default = 80. The top bound temperature value in Fahrenheit of the cool season temperature range. 

    9) temp_scale_step (Integer) - Default = 1. The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                                    (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

    10) temperature_contour_value (Integer) - Default = 32. This draws a contour line seperating two groups of temperature values. 
                                                Default is the boundary between below and above freezing temperatures.

    11) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                        and passing the data in or if the function needs to download the data. A value of False means the data
                        is downloaded inside of the function while a value of True means the user is downloading the data outside
                        of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                        things, it is recommended to set this value to True and download the data outside of the function and pass
                        it in so that the amount of data requests on the host servers can be minimized. 

    12) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                    in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                    outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

    13) ds_list (List) - Default = None. This is the list of datasets the user passes in if the user downloads the data outside of the function
                        and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                        needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

    14) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    15) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


    16) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                    

    17) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                    custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

    18) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
        Default setting is True. Users should change this value to False if they wish to hide rivers.

    19) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                            

    20) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide state borders. 

    21) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide county borders. 

    22) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display GACC borders. 

    23) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display PSA borders.

    24) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display CWA borders.

    25) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

    26) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

    27) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

    28) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

    29) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

    30) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

    31) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

    32) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

    33) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

    34) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

    35) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
        To change to a dashed line, users should set state_border_linestyle='--'. 

    36) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
        To change to a dashed line, users should set county_border_linestyle='--'. 

    37) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
        To change to a dashed line, users should set gacc_border_linestyle='--'. 

    38) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    39) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    40) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    41) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'.    

    42) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    43) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    44) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    45) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    46) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    47) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

    48) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                        This is a feature of matplotlib, as per their definition, the shrink is:
                                        "Fraction by which to multiply the size of the colorbar." 
                                        This should only be changed if the user wishes to make a custom plot. 
                                        Preset values are called from the settings module for each region. 

    49) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                when making a custom plot. 

    50) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    51) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    52) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

    53) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

    54) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


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

    temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
    temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step

    temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)

    temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)

    ticks_warm = temp_scale_warm[::5]
    ticks_cool = temp_scale_cool[::5]

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

    path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, '2-Meter Temperature', str_level)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass

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

        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            
            if region == 'conus' or region == 'North America' or region == 'north america' or region == 'NA' or region == 'na':
                decimate = decimate * 2
            else:
                decimate = decimate + 1
                
        elif model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            if region == 'conus' or region == 'North America' or region == 'north america' or region == 'NA' or region == 'na':
                decimate = decimate * 2
            else:
                decimate = decimate + 2
        else:
            decimate = decimate
    
    if data == False and model != 'GEFS0p25 ENS MEAN':
        if model == 'RAP' or model == 'RAP 32':
            ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
        else:
            ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)

    if data == False and model == 'GEFS0p25 ENS MEAN':
        ds_list = model_data.get_nomads_model_data_via_https(model, region, 'heightAboveGround', wb, eb, sb, nb, get_u_and_v_wind_components=False, add_wind_gusts=False)
        
    if data == True and model != 'GEFS0p25 ENS MEAN':
        ds = ds

    if data == True and model == 'GEFS0p25 ENS MEAN':
        ds_list = ds_list

    cmap = colormaps.temperature_colormap()

    if model != 'GEFS0p25 ENS MEAN':

        end1 = (int(round((len(ds['time']) - 1)/6, 0)) - 1)
        end2 = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
        
        for t in range(0, end1, 1):
        
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
            plt.title(f"{model} 2-METER TEMPERATURE [°F]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
            ax.text(x, y, f"Contour Line: T = {temperature_contour_value}[°F]", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
    
            stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
    
            if model == 'CMCENS' or model == 'GEFS0P50':
    
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :])
    
                temp = temp[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                    
                c = ax.contour(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), levels=[temperature_contour_value], colors='purple', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                ax.clabel(c, levels=[temperature_contour_value], inline=True, fontsize=8, rightside_up=True)
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_warm, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_warm)
    
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_cool, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_cool)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
    
            else:
                
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :])
    
                temp = temp[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                    
                c = ax.contour(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), levels=[temperature_contour_value], colors='purple', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                ax.clabel(c, levels=[temperature_contour_value], inline=True, fontsize=8, rightside_up=True)
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_warm, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_warm)
    
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_cool, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_cool)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
        for t in range(end1, end2, step):
        
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
            plt.title(f"{model} 2-METER TEMPERATURE [°F]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
            ax.text(x, y, f"Contour Line: T = {temperature_contour_value}[°F]", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
    
            stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
    
            if model == 'CMCENS' or model == 'GEFS0P50':
    
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :])
    
                temp = temp[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                    
                c = ax.contour(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), levels=[temperature_contour_value], colors='purple', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                ax.clabel(c, levels=[temperature_contour_value], inline=True, fontsize=8, rightside_up=True)
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_warm, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_warm)
    
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_cool, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_cool)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
    
            else:
                
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :])
    
                temp = temp[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                    
                c = ax.contour(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), levels=[temperature_contour_value], colors='purple', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                ax.clabel(c, levels=[temperature_contour_value], inline=True, fontsize=8, rightside_up=True)
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_warm, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_warm)
    
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_cool, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_cool)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
        print(f"Saved forecast graphics to {path_print}.")

    if model == 'GEFS0p25 ENS MEAN':

        for i in range(0, (len(ds_list) - 1)):

            time = ds_list[i]['valid_time']
            init = ds_list[0]['time']
            times = time.to_pandas()
            times = pd.to_datetime(times)
            inits = init.to_pandas()
            inits = pd.to_datetime(inits)
            
            tempK = ds_list[i]['t2m']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(tempK)
            c_temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(tempK)

            fname = f"Image_{i}.png"
        
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
            
            plt.title(f"{model} 2-METER TEMPERATURE [°F]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.strftime('%a %d/%H UTC')+"\nInitialization: "+inits.strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
            ax.text(x, y, f"Contour Line: T = {temperature_contour_value}[°F]", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
        
            lon_2d, lat_2d = np.meshgrid(ds_list[i]['longitude'], ds_list[i]['latitude'])

            numbers = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
            

            temp = temp[::decimate, ::decimate].to_numpy().flatten()
    
            numbers.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

            c = ax.contour(ds_list[i]['longitude'], ds_list[i]['latitude'], c_temp[: , :], levels=[temperature_contour_value], colors='purple', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c, levels=[temperature_contour_value], inline=True, fontsize=8, rightside_up=True)


            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs = ax.contourf(ds_list[i]['longitude'], ds_list[i]['latitude'], c_temp[: , :], cmap=cmap, transform=datacrs, levels=temp_scale_warm, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_warm)

            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs = ax.contourf(ds_list[i]['longitude'], ds_list[i]['latitude'], c_temp[: , :], cmap=cmap, transform=datacrs, levels=temp_scale_cool, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_cool)
    
            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)
        print(f"Saved forecast graphics to {path_print}.")


def plot_freezing_level(model, region, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

    """
    This function plots the Freezing Level Forecast. 

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
                    in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                    outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

    3) ds_list (List) - Default = None. This is the list of datasets the user passes in if the user downloads the data outside of the function
                        and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                        needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

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

    9) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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


    Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/FREEZING LEVEL


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

    levels = np.arange(3000, 10500, 500)
    ticks = levels[::2]

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

    str_level = f"FREEZING LEVEL"

    path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Freezing Level', str_level)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass

    if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
        step = 1
    
    if model == 'GEFS0p50':
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

        if model == 'GFS0p25' or model == 'NAM' or model == 'NAM 1hr' or model == 'GFS0p25_1hr':
            decimate = decimate * 2
        else:
            decimate = decimate
    
    if data == False:
        if model == 'RAP' or model == 'RAP 32':
            ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
        else:
            ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
        
    if data == True:
        ds = ds

    cmap = colormaps.gph_colormap()

    end1 = (int(round((len(ds['time']) - 1)/6, 0)) - 1)
    end2 = len(ds['time']) - 1
    time = ds['time']
    times = time.to_pandas()
    
    for t in range(0, end1, 1):
    
        fname = f"Image_{t}.png"
    
        fig = plt.figure(figsize=(12, 12))
        fig.set_facecolor('aliceblue')
        
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([wb, eb, sb, nb], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
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
        plt.title(f"{model} FREEZING LEVEL [FT]", fontsize=9, fontweight='bold', loc='left')
        plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
        
        lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])

        stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                            transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)

        if model == 'GEFS0P50':

            hgt = ds['hgttop0c'][0, t, :, :] * 3.28084

            hgt = hgt[::decimate, ::decimate].to_numpy().flatten()
    
            stn.plot_parameter('C', hgt, color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

            cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgttop0c'][0, t, :, :] * 3.28084), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)


        else:
            
            hgt = ds['hgttop0c'][t, :, :] * 3.28084

            hgt = hgt[::decimate, ::decimate].to_numpy().flatten()
    
            stn.plot_parameter('C', hgt, color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

            cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgttop0c'][t, :, :] * 3.28084), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)

    for t in range(end1, end2, step):
    
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
        plt.title(f"{model} FREEZING LEVEL [FT]", fontsize=9, fontweight='bold', loc='left')
        plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
        
        lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])

        stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                            transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)

        if model == 'GEFS0P50':

            hgt = ds['hgttop0c'][0, t, :, :] * 3.28084

            hgt = hgt[::decimate, ::decimate].to_numpy().flatten()
    
            stn.plot_parameter('C', hgt, color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

            cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgttop0c'][0, t, :, :] * 3.28084), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)


        else:
            
            hgt = ds['hgttop0c'][t, :, :] * 3.28084

            hgt = hgt[::decimate, ::decimate].to_numpy().flatten()
    
            stn.plot_parameter('C', hgt, color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

            cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgttop0c'][t, :, :] * 3.28084), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)
    print(f"Saved forecast graphics to {path_print}.")


def plot_heights_temperature_wind(model, region, level=850, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8):

    """
    This function plots the Geopotential Height/Temperature/Wind Forecast for a specific level. 

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
    
    1) level (Integer) - Default = 850. This is the level in millibars or hectopascals at which the user wishes to examine. 
                            850 means 850mb or 850hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

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
        hgt_levels = np.arange(96, 180, 4)
        temp_levels = np.arange(-40, 31, 1)
    if level == 700:
        hgt_levels = np.arange(240, 340, 4)
        temp_levels = np.arange(-50, 21, 1)
    if level == 500:
        temp_levels = np.arange(-60, 11, 1)
    if level == 300:
        hgt_levels = np.arange(840, 1020, 10)
        temp_levels = np.arange(-60, -19, 1)
    if level == 250:
        hgt_levels = np.arange(900, 1140, 10)
        temp_levels = np.arange(-70, -29, 1)
    if level == 200:
        hgt_levels = np.arange(1000, 1280, 10)
        temp_levels = np.arange(-70, -29, 1)

    ticks = temp_levels[::5]        

    if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america' or region == 'conus' or region == 'CONUS' or region == 'CONUS & South Canada & North Mexico':

        temp_low_levels = np.arange(-60, 0, 10)
        temp_high_levels = np.arange(10, 50, 10)
        
    else:

        temp_low_levels = np.arange(-60, 0, 5)
        temp_high_levels = np.arange(5, 55, 10)            

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


    cmap = colormaps.temperature_colormap_alt()

    end = len(ds['time']) - 1
    time = ds['time']
    times = time.to_pandas()


    path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Height Temperature Wind', str_level)

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
        plt.title(f"{model} {str_level} GPH [DM]/TEMPERATURE [°C]/WIND [KTS]", fontsize=9, fontweight='bold', loc='left')
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
                c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)

            else:                
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=hgt_levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                ax.clabel(c, levels=hgt_levels, inline=True, fontsize=8, rightside_up=True)

            c_temp_below = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][0, t, level_idx, :, :] - 273.15), colors='purple', transform=datacrs, levels=temp_low_levels, linewidths=0.5, linestyles='--')
            ax.clabel(c_temp_below, levels=temp_low_levels, inline=True, fontsize=8, rightside_up=True)

            c_temp_0 = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][0, t, level_idx, :, :] - 273.15), colors='dimgrey', transform=datacrs, levels=[0], linewidths=0.5, linestyles='--')
            ax.clabel(c_temp_0, levels=[0], inline=True, fontsize=8, rightside_up=True)

            c_temp_above = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][0, t, level_idx, :, :] - 273.15), colors='darkorange', transform=datacrs, levels=temp_high_levels, linewidths=0.5, linestyles='--')
            ax.clabel(c_temp_above, levels=temp_high_levels, inline=True, fontsize=8, rightside_up=True)
                
            cs = ax.contourf(ds['lon'], ds['lat'], (ds['tmpprs'][0, t, level_idx, :, :] - 273.15), cmap=cmap, transform=datacrs, levels=temp_levels, alpha=0.35, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)


        else:
            
            stn.plot_barb((ds['ugrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)

            if level == 500:
                c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)

            else:
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=hgt_levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                ax.clabel(c, levels=hgt_levels, inline=True, fontsize=8, rightside_up=True)

            c_temp_below = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][t, level_idx, :, :] - 273.15), colors='purple', transform=datacrs, levels=temp_low_levels, linewidths=0.5, linestyles='--')
            ax.clabel(c_temp_below, levels=temp_low_levels, inline=True, fontsize=8, rightside_up=True)

            c_temp_0 = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][t, level_idx, :, :] - 273.15), colors='dimgrey', transform=datacrs, levels=[0], linewidths=0.5, linestyles='--')
            ax.clabel(c_temp_0, levels=[0], inline=True, fontsize=8, rightside_up=True)

            c_temp_above = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][t, level_idx, :, :] - 273.15), colors='darkorange', transform=datacrs, levels=temp_high_levels, linewidths=0.5, linestyles='--')
            ax.clabel(c_temp_above, levels=temp_high_levels, inline=True, fontsize=8, rightside_up=True)
            
            cs = ax.contourf(ds['lon'], ds['lat'], (ds['tmpprs'][t, level_idx, :, :] - 273.15), cmap=cmap, transform=datacrs, levels=temp_levels, alpha=0.35, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)
    print(f"Saved forecast graphics to {path_print}.")
