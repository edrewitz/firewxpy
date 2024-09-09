import pytz
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import metpy.calc as mpcalc
import numpy as np
import firewxpy.parsers as parsers
import firewxpy.data_access as da
import firewxpy.geometry as geometry
import firewxpy.colormaps as colormaps
import pandas as pd
import matplotlib.gridspec as gridspec
import math
import firewxpy.settings as settings
import firewxpy.standard as standard


from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from dateutil import tz
from firewxpy.calc import scaling, Thermodynamics, unit_conversion
from firewxpy.utilities import file_functions

def plot_relative_humidity(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States and Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', alpha=0.5, data=None, time=None, state='us', gacc_region=None, colorbar_pad=0.02, clabel_fontsize=8):

    r'''
        This function does the following:
                                        1) Downloads the latest availiable temperature and dewpoint data arrays. 
                                        2) Downloads the METAR Data that is synced with the latest availiable 2.5km x 2.5km Real Time Mesoscale Analysis Data. 
                                        3) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data arrays. 
                                        4) Plots the relative humidity data overlayed with the METAR reports. 

        

        Inputs:

            1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.

            2) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.

            3) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.

            4) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.

            5) central_longitude (Integer or Float) - The central longitude. Defaults to -96.

            6) central_latitude (Integer or Float) - The central latitude. Defaults to 39.

            7) first_standard_parallel (Integer or Float) - Southern standard parallel. 

            8) second_standard_parallel (Integer or Float) - Northern standard parallel. 
            
            9) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

            10) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

            11) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

            12) decimate (Integer) - Distance in meters to decimate METAR stations apart from eachother so stations don't clutter the plot. The higher the value, the less stations are displayed. 

            13) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            14) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            15) title_font_size (Integer) - The fontsize of the title of the figure. 

            16) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            17) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

            18) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                       Default setting is 0.05.
                                       Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                       Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

            19) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis relative humidity overlayed with the latest METAR reports. 
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = state
    gacc_region = gacc_region

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    contourf = np.arange(0, 101, 1)
    if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
        contours = [0, 10, 20, 30, 40, 60, 80, 100]
        linewidths = 1
        clabel_fontsize = 12
    else:
        contours = np.arange(0, 110, 10)
        linewidths = 0.5

    labels = contourf[::4]

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
        if reference_system == 'States and Counties':
            show_state_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
        if reference_system == 'GACC Only':
            show_gacc_borders = True
        if reference_system == 'GACC and PSA':
            show_gacc_borders = True
            show_psa_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.25
        if reference_system == 'CWA Only':
            show_cwa_borders = True
        if reference_system == 'CWA and Public Zones':
            show_cwa_borders = True
            show_nws_public_zones = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                nws_public_zones_linewidth=0.25
        if reference_system == 'CWA and Fire Weather Zones':
            show_cwa_borders = True
            show_nws_firewx_zones = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                nws_firewx_zones_linewidth=0.25
        if reference_system == 'CWA and Counties':
            show_cwa_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
        if reference_system == 'GACC with PSA and Fire Weather Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_firewx_zones = True
            nws_firewx_zones_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC with PSA and Public Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_public_zones = True
            nws_public_zones_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC with PSA and CWA':
            show_gacc_borders = True
            show_psa_borders = True
            show_cwa_borders = True
            cwa_border_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC with PSA and Counties':
            show_gacc_borders = True
            show_psa_borders = True
            show_county_borders = True
            county_border_linewidth=0.25
        if reference_system == 'GACC and Counties':
            show_gacc_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
    
    if state != None and gacc_region == None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma')

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick


    if state == None and gacc_region != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_gacc_region_data_and_coords(gacc_region, 'rtma')

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick


    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None and gacc_region == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    
    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.relative_humidity_colormap()
    cmap_c = colormaps.thresh_contour_line_relative_humidity_colormap()

    try:
        if data == None:
            test = True
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            
            rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data[0]
            rtma_time = time

            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            
            rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            print("Unpacked the data successfully!")
        except Exception as e:
            pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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
    
    plt.title("RTMA Relative Humidity", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, rtma_data[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha)

    plt.rcParams["font.weight"] = "bold"

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Relative Humidity (%)", size=colorbar_fontsize, fontweight='bold')

    if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
        gaussian = mpcalc.smooth_gaussian(rtma_data[0, :, :], n=20)
    else:
        gaussian = mpcalc.smooth_gaussian(rtma_data[0, :, :], n=8)

    norm_con = ax.contour(lon, lat, gaussian, levels=contours, linewidths=linewidths, line_styles='dotted', cmap=cmap_c,
               transform=ccrs.PlateCarree())
    
    ax.clabel(norm_con, fontsize=clabel_fontsize, fmt="%.2s", rightside_up=True, zorder=3)

    path, gif_path = file_functions.check_file_paths(state, gacc_region, 'RTMA RH', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA RH')

def plot_24_hour_relative_humidity_comparison(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States and Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', alpha=0.5, data=None, data_24=None, time=None, time_24=None, state='us', gacc_region=None, colorbar_pad=0.02, clabel_fontsize=8):

    r'''
        This function does the following:
                                        1) Downloads the latest availiable temperature and dewpoint data arrays. 
                                        2) Downloads the METAR Data that is synced with the latest availiable 2.5km x 2.5km Real Time Mesoscale Analysis Data. 
                                        3) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data arrays. 
                                        4) Plots the relative humidity data overlayed with the METAR reports. 

        

        Inputs:

            1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.

            2) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.

            3) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.

            4) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.

            5) central_longitude (Integer or Float) - The central longitude. Defaults to -96.

            6) central_latitude (Integer or Float) - The central latitude. Defaults to 39.

            7) first_standard_parallel (Integer or Float) - Southern standard parallel. 

            8) second_standard_parallel (Integer or Float) - Northern standard parallel. 
            
            9) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

            10) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

            11) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

            12) decimate (Integer) - Distance in meters to decimate METAR stations apart from eachother so stations don't clutter the plot. The higher the value, the less stations are displayed. 

            13) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            14) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            15) title_font_size (Integer) - The fontsize of the title of the figure. 

            16) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            17) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

            18) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                       Default setting is 0.05.
                                       Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                       Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

            19) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis relative humidity overlayed with the latest METAR reports. 
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = state
    gacc_region = gacc_region

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    contourf = np.arange(-50, 51, 1)

    contours = [-75, -50, -30, -15, 15, 30, 50, 75] 

    linewidths = 1

    labels = contourf[::4]

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
        if reference_system == 'States and Counties':
            show_state_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
        if reference_system == 'GACC Only':
            show_gacc_borders = True
        if reference_system == 'GACC and PSA':
            show_gacc_borders = True
            show_psa_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.25
        if reference_system == 'CWA Only':
            show_cwa_borders = True
        if reference_system == 'CWA and Public Zones':
            show_cwa_borders = True
            show_nws_public_zones = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                nws_public_zones_linewidth=0.25
        if reference_system == 'CWA and Fire Weather Zones':
            show_cwa_borders = True
            show_nws_firewx_zones = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                nws_firewx_zones_linewidth=0.25
        if reference_system == 'CWA and Counties':
            show_cwa_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
        if reference_system == 'GACC with PSA and Fire Weather Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_firewx_zones = True
            nws_firewx_zones_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC with PSA and Public Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_public_zones = True
            nws_public_zones_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC with PSA and CWA':
            show_gacc_borders = True
            show_psa_borders = True
            show_cwa_borders = True
            cwa_border_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC with PSA and Counties':
            show_gacc_borders = True
            show_psa_borders = True
            show_county_borders = True
            county_border_linewidth=0.25
        if reference_system == 'GACC and Counties':
            show_gacc_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
    
    if state != None and gacc_region == None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma')

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick


    if state == None and gacc_region != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_gacc_region_data_and_coords(gacc_region, 'rtma')

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick


    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None and gacc_region == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    
    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.relative_humidity_colormap()
    cmap_c = colormaps.thresh_contour_line_relative_humidity_colormap()

    try:
        if data == None:
            test = True
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, ds_24, rtma_time, rtma_time_24 = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_24_hour_comparison_datasets(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = temp - 273.15
            dwpt = dwpt - 273.15

            temp_24 = ds_24['tmp2m']
            dwpt_24 = ds_24['dpt2m']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']
            temp_24 = temp_24 - 273.15
            dwpt_24 = dwpt_24 - 273.15
            
            rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            rtma_data_24 = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_24, dwpt_24)

            diff = rtma_data[0, :, :] - rtma_data_24[0, :, :]
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data[0]
            rtma_time = time
            ds_24 = data_24[0]
            rtma_time_24 = time_24

            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = temp - 273.15
            dwpt = dwpt - 273.15

            temp_24 = ds_24['tmp2m']
            dwpt_24 = ds_24['dpt2m']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']
            temp_24 = temp_24 - 273.15
            dwpt_24 = dwpt_24 - 273.15
            
            rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            rtma_data_24 = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_24, dwpt_24)

            diff = rtma_data[0, :, :] - rtma_data_24[0, :, :]

            print("Unpacked the data successfully!")
        except Exception as e:
            pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc_24 = rtma_time_24.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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
    
    plt.title("RTMA 24-Hour Relative Humidity Comparison", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Current: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")\n[Current - 24HRS]: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_24.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, diff, 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both')

    plt.rcParams["font.weight"] = "bold"

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Relative Humidity Trend (%)", size=colorbar_fontsize, fontweight='bold')

    if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
        gaussian = mpcalc.smooth_gaussian(diff, n=20)
    else:
        gaussian = mpcalc.smooth_gaussian(diff, n=8)

    norm_con = ax.contour(lon, lat, gaussian, levels=contours, linewidths=linewidths, linestyles='dotted', cmap=cmap_c,
               transform=ccrs.PlateCarree())
    
    ax.clabel(norm_con, fontsize=clabel_fontsize, fmt="%.2s", rightside_up=True, zorder=3)

    path, gif_path = file_functions.check_file_paths(state, gacc_region, '24HR RTMA RH COMPARISON', reference_system)
    file_functions.update_images(fig, path, gif_path, '24HR RTMA RH COMPARISON')
