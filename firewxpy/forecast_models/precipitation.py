"""
This class hosts the functions showing the precipitation forecast.

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


def plot_precipitation_rate(model, region, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

    """
    This function plots the Precipitation Rate Forecast. 

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
    sample_point_fontsize=sample_point_fontsize
    x=x 
    y=y
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    levels = [0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.5, 2, 2.5, 3]
    ticks = levels

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
                
        elif model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            if region == 'conus' or region == 'North America' or region == 'north america' or region == 'NA' or region == 'na':
                decimate = decimate * 2
            else:
                decimate = decimate + 2
        else:
            decimate = decimate

    path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Precipitation Rate', str_level)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass
            
    if data == False:
        if model == 'RAP' or model == 'RAP 32':
            ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
        else:
            ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
        
    if data == True:
        ds = ds


    cmap = colormaps.precipitation_colormap()


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
        plt.title(f"{model} SURFACE PRECIPITATION RATE [IN/HR]", fontsize=9, fontweight='bold', loc='left')
        plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
        
        lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])

        stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                            transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)

        if model == 'CMCENS' or model == 'GEFS0P50':

            qpf = ds['pratesfc'][0, t, :, :] * 141.73236

            qpf = qpf[::decimate, ::decimate].to_numpy().flatten()
    
            stn.plot_parameter('C', qpf, color='white', formatter='0.2f', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

            cs = ax.contourf(ds['lon'], ds['lat'], (ds['pratesfc'][0, t, :, :] * 141.73236), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)


        else:
            
            qpf = ds['pratesfc'][t, :, :] * 141.73236

            qpf = qpf[::decimate, ::decimate].to_numpy().flatten()
    
            stn.plot_parameter('C', qpf, color='white', formatter='0.2f', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

            cs = ax.contourf(ds['lon'], ds['lat'], (ds['pratesfc'][t, :, :] * 141.73236), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='max')
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
        plt.title(f"{model} SURFACE PRECIPITATION RATE [IN/HR]", fontsize=9, fontweight='bold', loc='left')
        plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
        
        lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])

        stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                            transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)

        if model == 'CMCENS' or model == 'GEFS0P50':

            qpf = ds['pratesfc'][0, t, :, :] * 141.73236

            qpf = qpf[::decimate, ::decimate].to_numpy().flatten()
    
            stn.plot_parameter('C', qpf, color='white', formatter='0.2f', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

            cs = ax.contourf(ds['lon'], ds['lat'], (ds['pratesfc'][0, t, :, :] * 141.73236), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)


        else:
            
            qpf = ds['pratesfc'][t, :, :] * 141.73236 

            qpf = qpf[::decimate, ::decimate].to_numpy().flatten()
    
            stn.plot_parameter('C', qpf, color='white', formatter='0.2f', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

            cs = ax.contourf(ds['lon'], ds['lat'], (ds['pratesfc'][t, :, :] * 141.73236), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            if mapcrs == datacrs:
                tim.sleep(10)
    print(f"Saved forecast graphics to {path_print}.")
