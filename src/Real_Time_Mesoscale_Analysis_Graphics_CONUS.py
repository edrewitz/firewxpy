'''
This file hosts all the Real Time Mesoscale Analysis (RTMA) plotting functions in FireWxPy for CONUS aka the "Lower-48". 
The RTMA data consists of gridded data for current conditions with a grid spacing of 2.5km x 2.5km.

There are 2 classes which are used to define the perspective of the plot: 
1) Counties_Perspective - This class uses state and county borders as the geographical reference. 
2) Predictive_Services_Areas_Perspective - This class uses the Geographic Area Coordination Center (GACC) and Predictive Services Area (PSA) boundaries as the geographical reference. 

This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS
'''

import pytz
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import metpy.calc as mpcalc
import numpy as np
import parsers
import data_access as da
import geometry
import calc
import colormaps
import pandas as pd
import matplotlib.gridspec as gridspec
import math

from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from NWS_Generic_Forecast_Graphics import standard
from dateutil import tz



def plot_relative_humidity(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, decimate='default', data=None, time=None):

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

    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate
        
    local_time, utc_time = standard.plot_creation_time()
    
    data = data
    try:
        if data == None:
            test = True
    except Exception as a:
        test = False

    data.append(data_var)
    time = time

    if test == True and time == None:
        
        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)
            NOMADS = False
            print("Unpacked the data successfully!")
        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            
            rtma_data = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            
            lat = ds['lat']
            lon = ds['lon']
            
            NOMADS = True
            print("Unpacked the data successfully!")

    elif test == False and time != None:
        try:
            rtma_data = data[0]
            rtma_time = time
            NOMADS = False
            print("Unpacked the data successfully!")
        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)
                NOMADS = False
                print("Unpacked the data successfully!")
            except Exception as g:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
                dwpt = ds['dpt2m']
                temp = temp - 273.15
                dwpt = dwpt - 273.15
                
                rtma_data = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                
                lat = ds['lat']
                lon = ds['lon']
                
                NOMADS = True
                print("Unpacked the data successfully!")
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")
        
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    cmap = colormaps.relative_humidity_colormap()

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    if NOMADS == False:

        plot_proj = rtma_data.metpy.cartopy_crs
        rtma_df = rtma_data.to_dataframe(name='rtma_rh')

        ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
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

        cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn = mpplots.StationPlot(ax, rtma_df['longitude'][::decimate], rtma_df['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn.plot_parameter('C', rtma_df['rtma_rh'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        plt.title("RTMA Relative Humidity\nAnalysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    if NOMADS == True:

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

        cs = ax.contourf(lon, lat, rtma_data[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA Relative Humidity\nAnalysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_total_cloud_cover(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, contour_step, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, decimate='default', data=None, time=None):

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

    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate
        
    local_time, utc_time = standard.plot_creation_time()
    contour_step = contour_step
    data = data
    try:
        if data == None:
            test = True
    except Exception as a:
        test = False
    time = time

    if test == True and time == None:
        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Total_cloud_cover_Analysis_entire_atmosphere_single_layer')
            NOMADS = False
            print("Unpacked the data successfully!")
        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
            cloud_cover = ds['tcdcclm']
            lon = cloud_cover['lon']
            lat = cloud_cover['lat']
            NOMADS = True
            print("Unpacked the data successfully!")

    elif test == False and time != None:
        try:
            rtma_data = data
            rtma_time = time
            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Total_cloud_cover_Analysis_entire_atmosphere_single_layer')
                NOMADS = False
                print("Unpacked the data successfully!")
            except Exception as e:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
                cloud_cover = ds['tcdcclm']
                lon = cloud_cover['lon']
                lat = cloud_cover['lat']
                NOMADS = True
                print("Unpacked the data successfully!")                

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    cmap = colormaps.cloud_cover_colormap()

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    if NOMADS == False:
        plot_proj = rtma_data.metpy.cartopy_crs
        rtma_df = rtma_data.to_dataframe()

        ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
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

        cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, alpha=alpha)

        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Total Cloud Cover (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn = mpplots.StationPlot(ax, rtma_df['longitude'][::decimate], rtma_df['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn.plot_parameter('C', rtma_df['Total_cloud_cover_Analysis_entire_atmosphere_single_layer'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        plt.title("RTMA Total Cloud Cover\nAnalysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    if NOMADS == True:

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

        cs = ax.contourf(lon, lat, cloud_cover[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, alpha=alpha)

        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Total Cloud Cover (%)", size=colorbar_label_font_size, fontweight='bold')

        plt.title("RTMA Relative Humidity\nAnalysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig

def plot_relative_humidity_with_METARs(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, thredds_decimate=80000, nomads_decimate=5, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, metar_fontsize=8, data=None):

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
    
    data = data
    local_time, utc_time = standard.plot_creation_time()
    nomads_decimate = nomads_decimate
    thredds_decimate = thredds_decimate

    if data == None:
        try:
            data = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, thredds_decimate)
            rtma_data = data[0]
            rtma_time = data[1]
            sfc_data = data[2]
            sfc_data_u_kt = data[3]
            sfc_data_v_kt = data[4]
            sfc_data_rh = data[5]
            sfc_data_decimate = data[6]
            metar_time_revised = data[7]
            plot_proj = data[8]            
            
            NOMADS = False
            print("Unpacked the data successfully!")
        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time_revised = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Dataset_Synced_With_METAR(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            
            rtma_data = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            
            lat = ds['lat']
            lon = ds['lon']
            
            NOMADS = True
            print("Unpacked the data successfully!")

    elif data != None:
        try:
            rtma_data = data[0]
            rtma_time = data[1]
            sfc_data = data[2]
            sfc_data_u_kt = data[3]
            sfc_data_v_kt = data[4]
            sfc_data_rh = data[5]
            sfc_data_decimate = data[6]
            metar_time_revised = data[7]
            plot_proj = data[8]            
            
            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                data = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, thredds_decimate)
                rtma_data = data[0]
                rtma_time = data[1]
                sfc_data = data[2]
                sfc_data_u_kt = data[3]
                sfc_data_v_kt = data[4]
                sfc_data_rh = data[5]
                sfc_data_decimate = data[6]
                metar_time_revised = data[7]
                plot_proj = data[8]            
                
                NOMADS = False
                print("Unpacked the data successfully!")
            except Exception as g:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time_revised = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Dataset_Synced_With_METAR(utc_time)
                temp = ds['tmp2m']
                dwpt = ds['dpt2m']
                temp = temp - 273.15
                dwpt = dwpt - 273.15
                
                rtma_data = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                
                lat = ds['lat']
                lon = ds['lon']
                
                NOMADS = True
                print("Unpacked the data successfully!")                

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    metar_time_revised = metar_time_revised.replace(tzinfo=from_zone)
    metar_time_revised = metar_time_revised.astimezone(to_zone)
    metar_time_revised_utc = metar_time_revised.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    cmap = colormaps.relative_humidity_colormap()

    if NOMADS == False:

        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
        ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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

        cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        # Plots METAR
        stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_decimate].m, sfc_data['latitude'][sfc_data_decimate].m,
                                 transform=ccrs.PlateCarree(), fontsize=metar_fontsize, zorder=10, clip_on=True)
        
        
        stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_decimate], color='red',
                          path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_decimate], color='darkorange',
                          path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_decimate], mpplots.sky_cover)
        
        stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_decimate], color='lime',
                            path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_barb(sfc_data['u'][sfc_data_decimate], sfc_data['v'][sfc_data_decimate])

        plt.title("RTMA Relative Humidity\nValid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %H:00 Local')+" ("+metar_time_revised_utc.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)
   
    if NOMADS == True:
        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=datacrs)
        ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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

        cs = ax.contourf(lon, lat, rtma_data[0, :, :], 
                         transform=datacrs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        # Plots METAR
        stn = mpplots.StationPlot(ax, sfc_data['longitude'][::nomads_decimate].m, sfc_data['latitude'][::nomads_decimate].m,
                                 transform=ccrs.PlateCarree(), fontsize=metar_fontsize, zorder=10, clip_on=True)
        
        
        stn.plot_parameter('NW', sfc_data['air_temperature'][::nomads_decimate].to('degF'), color='red',
                          path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_parameter('SW', sfc_data['dew_point_temperature'][::nomads_decimate].to('degF'), color='darkorange',
                          path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_symbol('C', sfc_data['cloud_coverage'][::nomads_decimate], mpplots.sky_cover)
        
        stn.plot_parameter('E', sfc_data_rh.to('percent')[::nomads_decimate], color='lime',
                            path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_barb(sfc_data['u'][::nomads_decimate], sfc_data['v'][::nomads_decimate])

        plt.title("RTMA Relative Humidity\nValid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %H:00 Local')+" ("+metar_time_revised_utc.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_low_relative_humidity_with_METARs(low_relative_humidity_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, thredds_decimate=80000, nomads_decimate=10, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, metar_fontsize=8, data=None):

    r'''
        This function does the following:
                                        1) Downloads the latest availiable temperature and dewpoint data arrays. 
                                        2) Downloads the METAR Data that is synced with the latest availiable 2.5km x 2.5km Real Time Mesoscale Analysis Data. 
                                        3) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data arrays. 
                                        4) Plots the relative humidity data filtered RH <= red_flag_warning_relative_humidity_threshold (%) overlayed with the latest METAR reports. 

        

        Inputs:

            1) red_flag_warning_relative_humidity_threshold (Integer) - The National Weather Service Red Flag Warning threshold for relative humidity. 

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
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis relative humidity data filtered RH <= red_flag_warning_relative_humidity_threshold (%) overlayed with the latest METAR reports. 
    
    '''

    low_relative_humidity_threshold = low_relative_humidity_threshold
    low_relative_humidity_threshold_numpy = low_relative_humidity_threshold + 1
    local_time, utc_time = standard.plot_creation_time()
    nomads_decimate = nomads_decimate
    thredds_decimate = thredds_decimate
    data = data

    if data == None:
        try:
            data = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, thredds_decimate)
            rtma_data = data[0]
            rtma_time = data[1]
            sfc_data = data[2]
            sfc_data_u_kt = data[3]
            sfc_data_v_kt = data[4]
            sfc_data_rh = data[5]
            sfc_data_decimate = data[6]
            metar_time_revised = data[7]
            plot_proj = data[8]            
            
            NOMADS = False
            print("Unpacked the data successfully!")
        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time_revised = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Dataset_Synced_With_METAR(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            
            rtma_data = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            
            lat = ds['lat']
            lon = ds['lon']
            
            NOMADS = True
            print("Unpacked the data successfully!")

    elif data != None:
        try:
            rtma_data = data[0]
            rtma_time = data[1]
            sfc_data = data[2]
            sfc_data_u_kt = data[3]
            sfc_data_v_kt = data[4]
            sfc_data_rh = data[5]
            sfc_data_decimate = data[6]
            metar_time_revised = data[7]
            plot_proj = data[8]            
            
            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                data = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, thredds_decimate)
                rtma_data = data[0]
                rtma_time = data[1]
                sfc_data = data[2]
                sfc_data_u_kt = data[3]
                sfc_data_v_kt = data[4]
                sfc_data_rh = data[5]
                sfc_data_decimate = data[6]
                metar_time_revised = data[7]
                plot_proj = data[8]            
                
                NOMADS = False
                print("Unpacked the data successfully!")
            except Exception as g:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time_revised = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Dataset_Synced_With_METAR(utc_time)
                temp = ds['tmp2m']
                dwpt = ds['dpt2m']
                temp = temp - 273.15
                dwpt = dwpt - 273.15
                
                rtma_data = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                
                lat = ds['lat']
                lon = ds['lon']
                
                NOMADS = True
                print("Unpacked the data successfully!")                

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")
        

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    metar_time_revised = metar_time_revised.replace(tzinfo=from_zone)
    metar_time_revised = metar_time_revised.astimezone(to_zone)
    metar_time_revised_utc = metar_time_revised.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    cmap = colormaps.low_relative_humidity_colormap()

    if NOMADS == False:

        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
        ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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

        cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, low_relative_humidity_threshold + 1, 1), cmap=cmap, alpha=alpha) 

        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        # Plots METAR
        stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_decimate].m, sfc_data['latitude'][sfc_data_decimate].m,
                                 transform=ccrs.PlateCarree(), fontsize=metar_fontsize, zorder=10, clip_on=True)
        
        
        stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_decimate], color='red',
                          path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_decimate], color='darkorange',
                          path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_decimate], mpplots.sky_cover)
        
        stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_decimate], color='lime',
                            path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_barb(sfc_data['u'][sfc_data_decimate], sfc_data['v'][sfc_data_decimate])

        plt.title("RTMA Low Relative Humidity\nValid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %H:00 Local')+" ("+metar_time_revised_utc.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)
   
    if NOMADS == True:
        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=datacrs)
        ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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

        cs = ax.contourf(lon, lat, rtma_data[0, :, :], 
                         transform=datacrs, levels=np.arange(0, low_relative_humidity_threshold + 1, 1), cmap=cmap, alpha=alpha)

        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        # Plots METAR
        stn = mpplots.StationPlot(ax, sfc_data['longitude'][::nomads_decimate].m, sfc_data['latitude'][::nomads_decimate].m,
                                 transform=ccrs.PlateCarree(), fontsize=metar_fontsize, zorder=10, clip_on=True)
        
        
        stn.plot_parameter('NW', sfc_data['air_temperature'][::nomads_decimate].to('degF'), color='red',
                          path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_parameter('SW', sfc_data['dew_point_temperature'][::nomads_decimate].to('degF'), color='darkorange',
                          path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_symbol('C', sfc_data['cloud_coverage'][::nomads_decimate], mpplots.sky_cover)
        
        stn.plot_parameter('E', sfc_data_rh.to('percent')[::nomads_decimate], color='lime',
                            path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_barb(sfc_data['u'][::nomads_decimate], sfc_data['v'][::nomads_decimate])

        plt.title("RTMA Low Relative Humidity\nValid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %H:00 Local')+" ("+metar_time_revised_utc.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_relative_humidity_6hr_timelapse(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, decimate='default', data=None, time=None):

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
    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate
    
    local_time, utc_time = standard.plot_creation_time()
    rtma_data = data
    rtma_time = time

    if rtma_data == None and rtma_time == None:
        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_relative_humidity_data_past_6hrs()

            rtma_data_0 = rtma_data[0]
            rtma_data_1 = rtma_data[1]
            rtma_data_2 = rtma_data[2]
            rtma_data_3 = rtma_data[3]
            rtma_data_4 = rtma_data[4]
            rtma_data_5 = rtma_data[5]
            rtma_data_6 = rtma_data[6]

            rtma_time_0 = rtma_time[0]
            rtma_time_1 = rtma_time[1]
            rtma_time_2 = rtma_time[2]
            rtma_time_3 = rtma_time[3]
            rtma_time_4 = rtma_time[4]
            rtma_time_5 = rtma_time[5]
            rtma_time_6 = rtma_time[6]

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds_list, rtma_times = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_rtma_data_past_6hrs()
            ds_0 = ds_list[0]
            ds_1 = ds_list[1]
            ds_2 = ds_list[2]
            ds_3 = ds_list[3]
            ds_4 = ds_list[4]
            ds_5 = ds_list[5]
            ds_6 = ds_list[6]

            rtma_time_0 = rtma_times[0]
            rtma_time_1 = rtma_times[1]
            rtma_time_2 = rtma_times[2]
            rtma_time_3 = rtma_times[3]
            rtma_time_4 = rtma_times[4]
            rtma_time_5 = rtma_times[5]
            rtma_time_6 = rtma_times[6]

            temp_0 = ds_0['tmp2m']
            temp_1 = ds_1['tmp2m']
            temp_2 = ds_2['tmp2m']
            temp_3 = ds_3['tmp2m']
            temp_4 = ds_4['tmp2m']
            temp_5 = ds_5['tmp2m']
            temp_6 = ds_6['tmp2m']

            dwpt_0 = ds_0['dpt2m']
            dwpt_1 = ds_1['dpt2m']
            dwpt_2 = ds_2['dpt2m']
            dwpt_3 = ds_3['dpt2m']
            dwpt_4 = ds_4['dpt2m']
            dwpt_5 = ds_5['dpt2m']
            dwpt_6 = ds_6['dpt2m']

            temp_0 = temp_0 - 273.15
            temp_1 = temp_1 - 273.15
            temp_2 = temp_2 - 273.15
            temp_3 = temp_3 - 273.15
            temp_4 = temp_4 - 273.15
            temp_5 = temp_5 - 273.15
            temp_6 = temp_6 - 273.15

            dwpt_0 = dwpt_0 - 273.15
            dwpt_1 = dwpt_1 - 273.15
            dwpt_2 = dwpt_2 - 273.15
            dwpt_3 = dwpt_3 - 273.15
            dwpt_4 = dwpt_4 - 273.15
            dwpt_5 = dwpt_5 - 273.15
            dwpt_6 = dwpt_6 - 273.15

            rh_0 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_0, dwpt_0)
            rh_1 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_1, dwpt_1)
            rh_2 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_2, dwpt_2)
            rh_3 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_3, dwpt_3)
            rh_4 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_4, dwpt_4)
            rh_5 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_5, dwpt_5)
            rh_6 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_6, dwpt_6)

            lat_0 = rh_0['lat']
            lon_0 = rh_0['lon']
            lat_1 = rh_1['lat']
            lon_1 = rh_1['lon']
            lat_2 = rh_2['lat']
            lon_2 = rh_2['lon']
            lat_3 = rh_3['lat']
            lon_3 = rh_3['lon']
            lat_4 = rh_4['lat']
            lon_4 = rh_4['lon']
            lat_5 = rh_5['lat']
            lon_5 = rh_5['lon']
            lat_6 = rh_6['lat']
            lon_6 = rh_6['lon']

            NOMADS = True
            print("Unpacked the data successfully!")

    elif rtma_data != None and rtma_time != None:
        try:
            rtma_data_0 = rtma_data[0]
            rtma_data_1 = rtma_data[1]
            rtma_data_2 = rtma_data[2]
            rtma_data_3 = rtma_data[3]
            rtma_data_4 = rtma_data[4]
            rtma_data_5 = rtma_data[5]
            rtma_data_6 = rtma_data[6]

            rtma_time_0 = rtma_time[0]
            rtma_time_1 = rtma_time[1]
            rtma_time_2 = rtma_time[2]
            rtma_time_3 = rtma_time[3]
            rtma_time_4 = rtma_time[4]
            rtma_time_5 = rtma_time[5]
            rtma_time_6 = rtma_time[6]

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            
            try:
                print("Unable to unpack the data. Downloading the data again...")
                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_relative_humidity_data_past_6hrs()
    
                rtma_data_0 = rtma_data[0]
                rtma_data_1 = rtma_data[1]
                rtma_data_2 = rtma_data[2]
                rtma_data_3 = rtma_data[3]
                rtma_data_4 = rtma_data[4]
                rtma_data_5 = rtma_data[5]
                rtma_data_6 = rtma_data[6]
    
                rtma_time_0 = rtma_time[0]
                rtma_time_1 = rtma_time[1]
                rtma_time_2 = rtma_time[2]
                rtma_time_3 = rtma_time[3]
                rtma_time_4 = rtma_time[4]
                rtma_time_5 = rtma_time[5]
                rtma_time_6 = rtma_time[6]
    
                NOMADS = False
                print("Unpacked the data successfully!")
    
            except Exception as g:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds_list, rtma_times = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_rtma_data_past_6hrs()
                ds_0 = ds_list[0]
                ds_1 = ds_list[1]
                ds_2 = ds_list[2]
                ds_3 = ds_list[3]
                ds_4 = ds_list[4]
                ds_5 = ds_list[5]
                ds_6 = ds_list[6]
    
                rtma_time_0 = rtma_times[0]
                rtma_time_1 = rtma_times[1]
                rtma_time_2 = rtma_times[2]
                rtma_time_3 = rtma_times[3]
                rtma_time_4 = rtma_times[4]
                rtma_time_5 = rtma_times[5]
                rtma_time_6 = rtma_times[6]
    
                temp_0 = ds_0['tmp2m']
                temp_1 = ds_1['tmp2m']
                temp_2 = ds_2['tmp2m']
                temp_3 = ds_3['tmp2m']
                temp_4 = ds_4['tmp2m']
                temp_5 = ds_5['tmp2m']
                temp_6 = ds_6['tmp2m']
    
                dwpt_0 = ds_0['dpt2m']
                dwpt_1 = ds_1['dpt2m']
                dwpt_2 = ds_2['dpt2m']
                dwpt_3 = ds_3['dpt2m']
                dwpt_4 = ds_4['dpt2m']
                dwpt_5 = ds_5['dpt2m']
                dwpt_6 = ds_6['dpt2m']
    
                temp_0 = temp_0 - 273.15
                temp_1 = temp_1 - 273.15
                temp_2 = temp_2 - 273.15
                temp_3 = temp_3 - 273.15
                temp_4 = temp_4 - 273.15
                temp_5 = temp_5 - 273.15
                temp_6 = temp_6 - 273.15
    
                dwpt_0 = dwpt_0 - 273.15
                dwpt_1 = dwpt_1 - 273.15
                dwpt_2 = dwpt_2 - 273.15
                dwpt_3 = dwpt_3 - 273.15
                dwpt_4 = dwpt_4 - 273.15
                dwpt_5 = dwpt_5 - 273.15
                dwpt_6 = dwpt_6 - 273.15
    
                rh_0 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_0, dwpt_0)
                rh_1 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_1, dwpt_1)
                rh_2 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_2, dwpt_2)
                rh_3 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_3, dwpt_3)
                rh_4 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_4, dwpt_4)
                rh_5 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_5, dwpt_5)
                rh_6 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_6, dwpt_6)
    
                lat_0 = rh_0['lat']
                lon_0 = rh_0['lon']
                lat_1 = rh_1['lat']
                lon_1 = rh_1['lon']
                lat_2 = rh_2['lat']
                lon_2 = rh_2['lon']
                lat_3 = rh_3['lat']
                lon_3 = rh_3['lon']
                lat_4 = rh_4['lat']
                lon_4 = rh_4['lon']
                lat_5 = rh_5['lat']
                lon_5 = rh_5['lon']
                lat_6 = rh_6['lat']
                lon_6 = rh_6['lon']
    
                NOMADS = True
                print("Unpacked the data successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    rtma_time_0 = rtma_time_0.replace(tzinfo=from_zone)
    rtma_time_0 = rtma_time_0.astimezone(to_zone)
    rtma_time_utc_0 = rtma_time_0.astimezone(from_zone)

    rtma_time_1 = rtma_time_1.replace(tzinfo=from_zone)
    rtma_time_1 = rtma_time_1.astimezone(to_zone)
    rtma_time_utc_1 = rtma_time_1.astimezone(from_zone)

    rtma_time_2 = rtma_time_2.replace(tzinfo=from_zone)
    rtma_time_2 = rtma_time_2.astimezone(to_zone)
    rtma_time_utc_2 = rtma_time_2.astimezone(from_zone)

    rtma_time_3 = rtma_time_3.replace(tzinfo=from_zone)
    rtma_time_3 = rtma_time_3.astimezone(to_zone)
    rtma_time_utc_3 = rtma_time_3.astimezone(from_zone)
    
    rtma_time_4 = rtma_time_4.replace(tzinfo=from_zone)
    rtma_time_4 = rtma_time_4.astimezone(to_zone)
    rtma_time_utc_4 = rtma_time_4.astimezone(from_zone)

    rtma_time_5 = rtma_time_5.replace(tzinfo=from_zone)
    rtma_time_5 = rtma_time_5.astimezone(to_zone)
    rtma_time_utc_5 = rtma_time_5.astimezone(from_zone)

    rtma_time_6 = rtma_time_6.replace(tzinfo=from_zone)
    rtma_time_6 = rtma_time_6.astimezone(to_zone)
    rtma_time_utc_6 = rtma_time_6.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    cmap = colormaps.relative_humidity_colormap()

    figs = []

    ################
    # FIRST FIGURE #
    ################

    if NOMADS == False:

        plot_proj_0 = rtma_data_0.metpy.cartopy_crs
        plot_proj_1 = rtma_data_1.metpy.cartopy_crs
        plot_proj_2 = rtma_data_2.metpy.cartopy_crs
        plot_proj_3 = rtma_data_3.metpy.cartopy_crs
        plot_proj_4 = rtma_data_4.metpy.cartopy_crs
        plot_proj_5 = rtma_data_5.metpy.cartopy_crs
        plot_proj_6 = rtma_data_6.metpy.cartopy_crs

        rtma_df0 = rtma_data_0.to_dataframe(name='rtma_rh')
        rtma_df1 = rtma_data_1.to_dataframe(name='rtma_rh')
        rtma_df2 = rtma_data_2.to_dataframe(name='rtma_rh')
        rtma_df3 = rtma_data_3.to_dataframe(name='rtma_rh')
        rtma_df4 = rtma_data_4.to_dataframe(name='rtma_rh')
        rtma_df5 = rtma_data_5.to_dataframe(name='rtma_rh')
        rtma_df6 = rtma_data_6.to_dataframe(name='rtma_rh')

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        
        ax1 = fig1.add_subplot(1, 1, 1, projection=plot_proj_0)
        ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs1 = ax1.contourf(rtma_data_0.metpy.x, rtma_data_0.metpy.y, rtma_data_0, 
                         transform=rtma_data_0.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)


        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink, pad=colorbar_pad)
        cbar1.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn1 = mpplots.StationPlot(ax1, rtma_df0['longitude'][::decimate], rtma_df0['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn1.plot_parameter('C', rtma_df0['rtma_rh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig1.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_0.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_0.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax1.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax1.transAxes)

        #################
        # SECOND FIGURE #
        #################

        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')

        ax2 = fig2.add_subplot(1, 1, 1, projection=plot_proj_1)
        ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs2 = ax2.contourf(rtma_data_1.metpy.x, rtma_data_1.metpy.y, rtma_data_1, 
                         transform=rtma_data_1.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink, pad=colorbar_pad)
        cbar2.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn2 = mpplots.StationPlot(ax2, rtma_df1['longitude'][::decimate], rtma_df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn2.plot_parameter('C', rtma_df1['rtma_rh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig2.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_1.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax2.transAxes)

        ################
        # THIRD FIGURE #
        ################

        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')

        ax3 = fig3.add_subplot(1, 1, 1, projection=plot_proj_2)
        ax3.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs3 = ax3.contourf(rtma_data_2.metpy.x, rtma_data_2.metpy.y, rtma_data_2, 
                         transform=rtma_data_2.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink, pad=colorbar_pad)
        cbar3.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn3 = mpplots.StationPlot(ax3, rtma_df2['longitude'][::decimate], rtma_df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn3.plot_parameter('C', rtma_df2['rtma_rh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig3.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_2.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax3.transAxes)


        #################
        # FOURTH FIGURE #
        #################

        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')

        ax4 = fig4.add_subplot(1, 1, 1, projection=plot_proj_3)
        ax4.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs4 = ax4.contourf(rtma_data_3.metpy.x, rtma_data_3.metpy.y, rtma_data_3, 
                         transform=rtma_data_3.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink, pad=colorbar_pad)
        cbar4.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn4 = mpplots.StationPlot(ax4, rtma_df3['longitude'][::decimate], rtma_df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn4.plot_parameter('C', rtma_df3['rtma_rh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig4.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_3.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax4.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax4.transAxes)


        ################
        # FIFTH FIGURE #
        ################

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')

        ax5 = fig5.add_subplot(1, 1, 1, projection=plot_proj_4)
        ax5.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax5.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs5 = ax5.contourf(rtma_data_4.metpy.x, rtma_data_4.metpy.y, rtma_data_4, 
                         transform=rtma_data_4.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink, pad=colorbar_pad)
        cbar5.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn5 = mpplots.StationPlot(ax5, rtma_df4['longitude'][::decimate], rtma_df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn5.plot_parameter('C', rtma_df4['rtma_rh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig5.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_4.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)

        ################
        # SIXTH FIGURE #
        ################

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')

        ax6 = fig6.add_subplot(1, 1, 1, projection=plot_proj_5)
        ax6.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax6.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs6 = ax6.contourf(rtma_data_5.metpy.x, rtma_data_5.metpy.y, rtma_data_5, 
                         transform=rtma_data_5.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink, pad=colorbar_pad)
        cbar6.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn6 = mpplots.StationPlot(ax6, rtma_df5['longitude'][::decimate], rtma_df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn6.plot_parameter('C', rtma_df5['rtma_rh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig6.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_5.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax6.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax6.transAxes)

        ##################
        # SEVENTH FIGURE #
        ##################

        fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig7.set_facecolor('aliceblue')

        ax7 = fig7.add_subplot(1, 1, 1, projection=plot_proj_6)
        ax7.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax7.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs7 = ax7.contourf(rtma_data_6.metpy.x, rtma_data_6.metpy.y, rtma_data_6, 
                         transform=rtma_data_6.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink, pad=colorbar_pad)
        cbar7.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn7 = mpplots.StationPlot(ax7, rtma_df6['longitude'][::decimate], rtma_df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn7.plot_parameter('C', rtma_df6['rtma_rh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig7.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_6.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax7.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax7.transAxes)

    if NOMADS == True:

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')

        ax1 = fig1.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs1 = ax1.contourf(lon_0, lat_0, rh_0[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink, pad=colorbar_pad)
        cbar1.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        fig1.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_0.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_0.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax1.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax1.transAxes)

        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')

        ax2 = fig2.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs2 = ax2.contourf(lon_1, lat_1, rh_1[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink, pad=colorbar_pad)
        cbar2.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        fig2.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_1.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax2.transAxes)


        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')

        ax3 = fig3.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax3.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs3 = ax3.contourf(lon_2, lat_2, rh_2[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink, pad=colorbar_pad)
        cbar3.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        fig3.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_2.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax3.transAxes)

        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')

        ax4 = fig4.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax4.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs4 = ax4.contourf(lon_3, lat_3, rh_3[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink, pad=colorbar_pad)
        cbar4.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        fig4.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_3.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax4.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax4.transAxes)

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')

        ax5 = fig5.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax5.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax5.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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

        cs5 = ax5.contourf(lon_4, lat_4, rh_4[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink, pad=colorbar_pad)
        cbar5.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        fig5.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_4.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')

        ax6 = fig6.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax6.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax6.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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

        cs6 = ax6.contourf(lon_5, lat_5, rh_5[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink, pad=colorbar_pad)
        cbar6.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        fig6.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_5.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax6.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax6.transAxes)

        fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig7.set_facecolor('aliceblue')

        ax7 = fig7.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax7.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax7.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs7 = ax7.contourf(lon_6, lat_6, rh_6[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(0, 105, 5), cmap=cmap, alpha=alpha)

        cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink, pad=colorbar_pad)
        cbar7.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

        fig7.suptitle("Real Time Mesoscale Analysis Relative Humidity\nAnalysis Valid: " + rtma_time_6.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax7.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax7.transAxes)

    figs.append(fig7)
    figs.append(fig6)
    figs.append(fig5)
    figs.append(fig4)
    figs.append(fig3)
    figs.append(fig2)
    figs.append(fig1)

    return figs


def plot_relative_humidity_trend_6hr_timelapse(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, decimate='default', data=None, time=None):

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
    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate

    local_time, utc_time = standard.plot_creation_time()
    rtma_data = data
    rtma_time = time

    if rtma_data == None and rtma_time == None:
    
        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_relative_humidity_data_past_6hrs()

            rtma_data_0 = rtma_data[0]
            rtma_data_1 = rtma_data[1]
            rtma_data_2 = rtma_data[2]
            rtma_data_3 = rtma_data[3]
            rtma_data_4 = rtma_data[4]
            rtma_data_5 = rtma_data[5]
            rtma_data_6 = rtma_data[6]
            rtma_data_7 = rtma_data[7]

            rtma_time_0 = rtma_time[0]
            rtma_time_1 = rtma_time[1]
            rtma_time_2 = rtma_time[2]
            rtma_time_3 = rtma_time[3]
            rtma_time_4 = rtma_time[4]
            rtma_time_5 = rtma_time[5]
            rtma_time_6 = rtma_time[6]
            rtma_time_7 = rtma_time[7]

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds_list, rtma_times = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_rtma_data_past_6hrs()
            ds_0 = ds_list[0]
            ds_1 = ds_list[1]
            ds_2 = ds_list[2]
            ds_3 = ds_list[3]
            ds_4 = ds_list[4]
            ds_5 = ds_list[5]
            ds_6 = ds_list[6]
            ds_7 = ds_list[7]

            rtma_time_0 = rtma_times[0]
            rtma_time_1 = rtma_times[1]
            rtma_time_2 = rtma_times[2]
            rtma_time_3 = rtma_times[3]
            rtma_time_4 = rtma_times[4]
            rtma_time_5 = rtma_times[5]
            rtma_time_6 = rtma_times[6]
            rtma_time_7 = rtma_times[7]

            temp_0 = ds_0['tmp2m']
            temp_1 = ds_1['tmp2m']
            temp_2 = ds_2['tmp2m']
            temp_3 = ds_3['tmp2m']
            temp_4 = ds_4['tmp2m']
            temp_5 = ds_5['tmp2m']
            temp_6 = ds_6['tmp2m']
            temp_7 = ds_7['tmp2m']

            dwpt_0 = ds_0['dpt2m']
            dwpt_1 = ds_1['dpt2m']
            dwpt_2 = ds_2['dpt2m']
            dwpt_3 = ds_3['dpt2m']
            dwpt_4 = ds_4['dpt2m']
            dwpt_5 = ds_5['dpt2m']
            dwpt_6 = ds_6['dpt2m']
            dwpt_7 = ds_7['dpt2m']

            temp_0 = temp_0 - 273.15
            temp_1 = temp_1 - 273.15
            temp_2 = temp_2 - 273.15
            temp_3 = temp_3 - 273.15
            temp_4 = temp_4 - 273.15
            temp_5 = temp_5 - 273.15
            temp_6 = temp_6 - 273.15
            temp_7 = temp_7 - 273.15

            dwpt_0 = dwpt_0 - 273.15
            dwpt_1 = dwpt_1 - 273.15
            dwpt_2 = dwpt_2 - 273.15
            dwpt_3 = dwpt_3 - 273.15
            dwpt_4 = dwpt_4 - 273.15
            dwpt_5 = dwpt_5 - 273.15
            dwpt_6 = dwpt_6 - 273.15
            dwpt_7 = dwpt_7 - 273.15

            rh_0 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_0, dwpt_0)
            rh_1 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_1, dwpt_1)
            rh_2 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_2, dwpt_2)
            rh_3 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_3, dwpt_3)
            rh_4 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_4, dwpt_4)
            rh_5 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_5, dwpt_5)
            rh_6 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_6, dwpt_6)
            rh_7 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_7, dwpt_7)

            diff1 = rh_0[0, :, :] - rh_1[0, :, :]
            diff2 = rh_1[0, :, :] - rh_2[0, :, :]
            diff3 = rh_2[0, :, :] - rh_3[0, :, :]
            diff4 = rh_3[0, :, :] - rh_4[0, :, :]
            diff5 = rh_4[0, :, :] - rh_5[0, :, :]
            diff6 = rh_5[0, :, :] - rh_6[0, :, :]
            diff7 = rh_6[0, :, :] - rh_7[0, :, :]

            lat_0 = rh_0['lat']
            lon_0 = rh_0['lon']
            lat_1 = rh_1['lat']
            lon_1 = rh_1['lon']
            lat_2 = rh_2['lat']
            lon_2 = rh_2['lon']
            lat_3 = rh_3['lat']
            lon_3 = rh_3['lon']
            lat_4 = rh_4['lat']
            lon_4 = rh_4['lon']
            lat_5 = rh_5['lat']
            lon_5 = rh_5['lon']
            lat_6 = rh_6['lat']
            lon_6 = rh_6['lon']
            lat_7 = rh_7['lat']
            lon_7 = rh_7['lon']

            NOMADS = True
            print("Unpacked the data successfully!")

    elif rtma_data != None and rtma_time != None:
        try:
            rtma_data_0 = rtma_data[0]
            rtma_data_1 = rtma_data[1]
            rtma_data_2 = rtma_data[2]
            rtma_data_3 = rtma_data[3]
            rtma_data_4 = rtma_data[4]
            rtma_data_5 = rtma_data[5]
            rtma_data_6 = rtma_data[6]
            rtma_data_7 = rtma_data[7]

            rtma_time_0 = rtma_time[0]
            rtma_time_1 = rtma_time[1]
            rtma_time_2 = rtma_time[2]
            rtma_time_3 = rtma_time[3]
            rtma_time_4 = rtma_time[4]
            rtma_time_5 = rtma_time[5]
            rtma_time_6 = rtma_time[6]
            rtma_time_7 = rtma_time[7]

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_relative_humidity_data_past_6hrs()
    
                rtma_data_0 = rtma_data[0]
                rtma_data_1 = rtma_data[1]
                rtma_data_2 = rtma_data[2]
                rtma_data_3 = rtma_data[3]
                rtma_data_4 = rtma_data[4]
                rtma_data_5 = rtma_data[5]
                rtma_data_6 = rtma_data[6]
                rtma_data_7 = rtma_data[7]
    
                rtma_time_0 = rtma_time[0]
                rtma_time_1 = rtma_time[1]
                rtma_time_2 = rtma_time[2]
                rtma_time_3 = rtma_time[3]
                rtma_time_4 = rtma_time[4]
                rtma_time_5 = rtma_time[5]
                rtma_time_6 = rtma_time[6]
                rtma_time_7 = rtma_time[7]
    
                NOMADS = False
                print("Unpacked the data successfully!")
    
            except Exception as e:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds_list, rtma_times = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_rtma_data_past_6hrs()
                ds_0 = ds_list[0]
                ds_1 = ds_list[1]
                ds_2 = ds_list[2]
                ds_3 = ds_list[3]
                ds_4 = ds_list[4]
                ds_5 = ds_list[5]
                ds_6 = ds_list[6]
                ds_7 = ds_list[7]
    
                rtma_time_0 = rtma_times[0]
                rtma_time_1 = rtma_times[1]
                rtma_time_2 = rtma_times[2]
                rtma_time_3 = rtma_times[3]
                rtma_time_4 = rtma_times[4]
                rtma_time_5 = rtma_times[5]
                rtma_time_6 = rtma_times[6]
                rtma_time_7 = rtma_times[7]
    
                temp_0 = ds_0['tmp2m']
                temp_1 = ds_1['tmp2m']
                temp_2 = ds_2['tmp2m']
                temp_3 = ds_3['tmp2m']
                temp_4 = ds_4['tmp2m']
                temp_5 = ds_5['tmp2m']
                temp_6 = ds_6['tmp2m']
                temp_7 = ds_7['tmp2m']
    
                dwpt_0 = ds_0['dpt2m']
                dwpt_1 = ds_1['dpt2m']
                dwpt_2 = ds_2['dpt2m']
                dwpt_3 = ds_3['dpt2m']
                dwpt_4 = ds_4['dpt2m']
                dwpt_5 = ds_5['dpt2m']
                dwpt_6 = ds_6['dpt2m']
                dwpt_7 = ds_7['dpt2m']
    
                temp_0 = temp_0 - 273.15
                temp_1 = temp_1 - 273.15
                temp_2 = temp_2 - 273.15
                temp_3 = temp_3 - 273.15
                temp_4 = temp_4 - 273.15
                temp_5 = temp_5 - 273.15
                temp_6 = temp_6 - 273.15
                temp_7 = temp_7 - 273.15
    
                dwpt_0 = dwpt_0 - 273.15
                dwpt_1 = dwpt_1 - 273.15
                dwpt_2 = dwpt_2 - 273.15
                dwpt_3 = dwpt_3 - 273.15
                dwpt_4 = dwpt_4 - 273.15
                dwpt_5 = dwpt_5 - 273.15
                dwpt_6 = dwpt_6 - 273.15
                dwpt_7 = dwpt_7 - 273.15
    
                rh_0 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_0, dwpt_0)
                rh_1 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_1, dwpt_1)
                rh_2 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_2, dwpt_2)
                rh_3 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_3, dwpt_3)
                rh_4 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_4, dwpt_4)
                rh_5 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_5, dwpt_5)
                rh_6 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_6, dwpt_6)
                rh_7 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_7, dwpt_7)
    
                diff1 = rh_0[0, :, :] - rh_1[0, :, :]
                diff2 = rh_1[0, :, :] - rh_2[0, :, :]
                diff3 = rh_2[0, :, :] - rh_3[0, :, :]
                diff4 = rh_3[0, :, :] - rh_4[0, :, :]
                diff5 = rh_4[0, :, :] - rh_5[0, :, :]
                diff6 = rh_5[0, :, :] - rh_6[0, :, :]
                diff7 = rh_6[0, :, :] - rh_7[0, :, :]
    
                lat_0 = rh_0['lat']
                lon_0 = rh_0['lon']
                lat_1 = rh_1['lat']
                lon_1 = rh_1['lon']
                lat_2 = rh_2['lat']
                lon_2 = rh_2['lon']
                lat_3 = rh_3['lat']
                lon_3 = rh_3['lon']
                lat_4 = rh_4['lat']
                lon_4 = rh_4['lon']
                lat_5 = rh_5['lat']
                lon_5 = rh_5['lon']
                lat_6 = rh_6['lat']
                lon_6 = rh_6['lon']
                lat_7 = rh_7['lat']
                lon_7 = rh_7['lon']
    
                NOMADS = True
                print("Unpacked the data successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")        

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    rtma_time_0 = rtma_time_0.replace(tzinfo=from_zone)
    rtma_time_0 = rtma_time_0.astimezone(to_zone)
    rtma_time_utc_0 = rtma_time_0.astimezone(from_zone)

    rtma_time_1 = rtma_time_1.replace(tzinfo=from_zone)
    rtma_time_1 = rtma_time_1.astimezone(to_zone)
    rtma_time_utc_1 = rtma_time_1.astimezone(from_zone)

    rtma_time_2 = rtma_time_2.replace(tzinfo=from_zone)
    rtma_time_2 = rtma_time_2.astimezone(to_zone)
    rtma_time_utc_2 = rtma_time_2.astimezone(from_zone)

    rtma_time_3 = rtma_time_3.replace(tzinfo=from_zone)
    rtma_time_3 = rtma_time_3.astimezone(to_zone)
    rtma_time_utc_3 = rtma_time_3.astimezone(from_zone)

    rtma_time_4 = rtma_time_4.replace(tzinfo=from_zone)
    rtma_time_4 = rtma_time_4.astimezone(to_zone)
    rtma_time_utc_4 = rtma_time_4.astimezone(from_zone)

    rtma_time_5 = rtma_time_5.replace(tzinfo=from_zone)
    rtma_time_5 = rtma_time_5.astimezone(to_zone)
    rtma_time_utc_5 = rtma_time_5.astimezone(from_zone)
    
    rtma_time_6 = rtma_time_6.replace(tzinfo=from_zone)
    rtma_time_6 = rtma_time_6.astimezone(to_zone)
    rtma_time_utc_6 = rtma_time_6.astimezone(from_zone)

    rtma_time_7 = rtma_time_7.replace(tzinfo=from_zone)
    rtma_time_7 = rtma_time_7.astimezone(to_zone)
    rtma_time_utc_7 = rtma_time_7.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
    cmap_trend = colormaps.relative_humidity_change_colormap()

    figs = []

    ################
    # FIRST FIGURE #
    ################

    if NOMADS == False:

        diff1 = rtma_data_0 - rtma_data_1
        diff2 = rtma_data_1 - rtma_data_2
        diff3 = rtma_data_2 - rtma_data_3
        diff4 = rtma_data_3 - rtma_data_4
        diff5 = rtma_data_4 - rtma_data_5
        diff6 = rtma_data_5 - rtma_data_6
        diff7 = rtma_data_6 - rtma_data_7

        rtma_df1 = diff1.to_dataframe(name='rtma_rh_change')
        rtma_df2 = diff2.to_dataframe(name='rtma_rh_change')
        rtma_df3 = diff3.to_dataframe(name='rtma_rh_change')
        rtma_df4 = diff4.to_dataframe(name='rtma_rh_change')
        rtma_df5 = diff5.to_dataframe(name='rtma_rh_change')
        rtma_df6 = diff6.to_dataframe(name='rtma_rh_change')
        rtma_df7 = diff7.to_dataframe(name='rtma_rh_change')

        plot_proj_8 = diff1.metpy.cartopy_crs
        plot_proj_9 = diff2.metpy.cartopy_crs
        plot_proj_10 = diff3.metpy.cartopy_crs
        plot_proj_11 = diff4.metpy.cartopy_crs
        plot_proj_12 = diff5.metpy.cartopy_crs
        plot_proj_13 = diff6.metpy.cartopy_crs
        plot_proj_14 = diff7.metpy.cartopy_crs

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')

        fig1.suptitle("RTMA Hourly RH Trend (Shaded)\nValid: "+rtma_time_0.strftime('%H:00 Local') + " (" + rtma_time_utc_0.strftime('%H:00 UTC')+")" + " - " + rtma_time_1.strftime('%H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax1 = fig1.add_subplot(1, 1, 1, projection=plot_proj_8)
        ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs1 = ax1.contourf(diff1.metpy.x, diff1.metpy.y, diff1, 
                         transform=diff1.metpy.cartopy_crs, levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha, extend='both')

        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink, pad=colorbar_pad)
        cbar1.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn1 = mpplots.StationPlot(ax1, rtma_df1['longitude'][::decimate], rtma_df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn1.plot_parameter('C', rtma_df1['rtma_rh_change'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass
        

        ax1.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax1.transAxes)


        #################
        # SECOND FIGURE #
        #################

        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')

        fig2.suptitle("RTMA Hourly RH Trend (Shaded)\nValid: "+rtma_time_1.strftime('%H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")" + " - " + rtma_time_2.strftime('%H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax2 = fig2.add_subplot(1, 1, 1, projection=plot_proj_9)
        ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs2 = ax2.contourf(diff2.metpy.x, diff2.metpy.y, diff2, 
                         transform=diff2.metpy.cartopy_crs, levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha, extend='both')

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink, pad=colorbar_pad)
        cbar2.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn2 = mpplots.StationPlot(ax2, rtma_df2['longitude'][::decimate], rtma_df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn2.plot_parameter('C', rtma_df2['rtma_rh_change'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass


        ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax2.transAxes)


        ################
        # THIRD FIGURE #
        ################

        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')

        fig3.suptitle("RTMA Hourly RH Trend (Shaded)\nValid: "+rtma_time_2.strftime('%H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")" + " - " + rtma_time_3.strftime('%H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax3 = fig3.add_subplot(1, 1, 1, projection=plot_proj_10)
        ax3.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs3 = ax3.contourf(diff3.metpy.x, diff3.metpy.y, diff3, 
                         transform=diff3.metpy.cartopy_crs, levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha, extend='both')

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink, pad=colorbar_pad)
        cbar3.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn3 = mpplots.StationPlot(ax3, rtma_df3['longitude'][::decimate], rtma_df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn3.plot_parameter('C', rtma_df3['rtma_rh_change'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass
        

        ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax3.transAxes)


        #################
        # FOURTH FIGURE #
        #################

        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')

        fig4.suptitle("RTMA Hourly RH Trend (Shaded)\nValid: "+rtma_time_3.strftime('%H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")" + " - " + rtma_time_4.strftime('%H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax4 = fig4.add_subplot(1, 1, 1, projection=plot_proj_11)
        ax4.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs4 = ax4.contourf(diff4.metpy.x, diff4.metpy.y, diff4, 
                         transform=diff4.metpy.cartopy_crs, levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha, extend='both')

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink, pad=colorbar_pad)
        cbar4.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn4 = mpplots.StationPlot(ax4, rtma_df4['longitude'][::decimate], rtma_df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn4.plot_parameter('C', rtma_df4['rtma_rh_change'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        ax4.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax4.transAxes)


        ################
        # FIFTH FIGURE #
        ################

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')

        fig5.suptitle("RTMA Hourly RH Trend (Shaded)\nValid: "+rtma_time_4.strftime('%H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")" + " - " + rtma_time_5.strftime('%H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax5 = fig5.add_subplot(1, 1, 1, projection=plot_proj_12)
        ax5.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax5.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs5 = ax5.contourf(diff5.metpy.x, diff5.metpy.y, diff5, 
                         transform=diff5.metpy.cartopy_crs, levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha, extend='both')

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink, pad=colorbar_pad)
        cbar5.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn5 = mpplots.StationPlot(ax5, rtma_df5['longitude'][::decimate], rtma_df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn5.plot_parameter('C', rtma_df5['rtma_rh_change'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass


        ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)

        ################
        # SIXTH FIGURE #
        ################

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')

        fig6.suptitle("RTMA Hourly RH Trend (Shaded)\nValid: "+rtma_time_5.strftime('%H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")" + " - " + rtma_time_6.strftime('%H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax6 = fig6.add_subplot(1, 1, 1, projection=plot_proj_13)
        ax6.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax6.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs6 = ax6.contourf(diff6.metpy.x, diff6.metpy.y, diff6, 
                         transform=diff6.metpy.cartopy_crs, levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha, extend='both')

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink, pad=colorbar_pad)
        cbar6.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn6 = mpplots.StationPlot(ax6, rtma_df6['longitude'][::decimate], rtma_df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn6.plot_parameter('C', rtma_df6['rtma_rh_change'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass
        
        ax6.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax6.transAxes)

        ##################
        # SEVENTH FIGURE #
        ##################

        fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig7.set_facecolor('aliceblue')

        fig7.suptitle("RTMA Hourly RH Trend (Shaded)\nValid: "+rtma_time_6.strftime('%H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")" + " - " + rtma_time_7.strftime('%H:00 Local') + " (" + rtma_time_utc_7.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax7 = fig7.add_subplot(1, 1, 1, projection=plot_proj_14)
        ax7.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax7.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs7 = ax7.contourf(diff7.metpy.x, diff7.metpy.y, diff7, 
                         transform=diff7.metpy.cartopy_crs, levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha, extend='both')

        cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink, pad=colorbar_pad)
        cbar7.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn7 = mpplots.StationPlot(ax7, rtma_df7['longitude'][::decimate], rtma_df7['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn7.plot_parameter('C', rtma_df7['rtma_rh_change'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass
        
        ax7.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax7.transAxes)

    if NOMADS == True:

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')

        ax1 = fig1.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs1 = ax1.contourf(lon_0, lat_0, diff1, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha)

        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink, pad=colorbar_pad)
        cbar1.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        fig1.suptitle("RTMA Hourly RH Trend\nValid: "+rtma_time_0.strftime('%H:00 Local') + " (" + rtma_time_utc_0.strftime('%H:00 UTC')+")" + " - " + rtma_time_1.strftime('%H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax1.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax1.transAxes)

        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')

        ax2 = fig2.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs2 = ax2.contourf(lon_1, lat_1, diff2, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha)

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink, pad=colorbar_pad)
        cbar2.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        fig2.suptitle("RTMA Hourly RH Trend\nValid: "+rtma_time_1.strftime('%H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")" + " - " + rtma_time_2.strftime('%H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax2.transAxes)


        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')

        ax3 = fig3.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax3.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs3 = ax3.contourf(lon_2, lat_2, diff3, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha)

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink, pad=colorbar_pad)
        cbar3.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        fig3.suptitle("RTMA Hourly RH Trend\nValid: "+rtma_time_2.strftime('%H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")" + " - " + rtma_time_3.strftime('%H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax3.transAxes)

        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')

        ax4 = fig4.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax4.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs4 = ax4.contourf(lon_3, lat_3, diff4, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha)

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink, pad=colorbar_pad)
        cbar4.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        fig4.suptitle("RTMA Hourly RH Trend\nValid: "+rtma_time_3.strftime('%H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")" + " - " + rtma_time_4.strftime('%H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax4.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax4.transAxes)

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')

        ax5 = fig5.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax5.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax5.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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

        cs5 = ax5.contourf(lon_4, lat_4, diff5, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha)

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink, pad=colorbar_pad)
        cbar5.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        fig5.suptitle("RTMA Hourly RH Trend\nValid: "+rtma_time_4.strftime('%H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")" + " - " + rtma_time_5.strftime('%H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')

        ax6 = fig6.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax6.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax6.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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

        cs6 = ax6.contourf(lon_5, lat_5, diff6, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha)

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink, pad=colorbar_pad)
        cbar6.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        fig6.suptitle("RTMA Hourly RH Trend\nValid: "+rtma_time_5.strftime('%H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")" + " - " + rtma_time_6.strftime('%H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax6.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax6.transAxes)

        fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig7.set_facecolor('aliceblue')

        ax7 = fig7.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax7.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax7.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs7 = ax7.contourf(lon_6, lat_6, diff7,
                         transform=ccrs.PlateCarree(), levels=np.arange(-25, 26, 1), cmap=cmap_trend, alpha=alpha)

        cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink, pad=colorbar_pad)
        cbar7.set_label(label="Hourly Relative Humidity Trend (%)", size=colorbar_label_font_size, fontweight='bold')

        fig7.suptitle("RTMA Hourly RH Trend\nValid: "+rtma_time_6.strftime('%H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")" + " - " + rtma_time_7.strftime('%H:00 Local') + " (" + rtma_time_utc_7.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax7.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax7.transAxes)

    figs.append(fig7)
    figs.append(fig6)
    figs.append(fig5)
    figs.append(fig4)
    figs.append(fig3)
    figs.append(fig2)
    figs.append(fig1)

    return figs


def plot_temperature_6hr_timelapse(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, temperature_bottom_bound, temperature_top_bound, temperature_step, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, decimate='default', data=None, time=None):

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
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis Temperature overlayed with the latest METAR reports. 
    
    '''

    temperature_bottom_bound = temperature_bottom_bound
    temperature_top_bound = temperature_top_bound
    temperature_step = temperature_step
    local_time, utc_time = standard.plot_creation_time()
    rtma_data = data
    rtma_time = time

    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate

    if rtma_data == None and rtma_time == None:
        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_past_6hrs('Temperature_Analysis_height_above_ground')

            rtma_data_0 = rtma_data[0]
            rtma_data_1 = rtma_data[1]
            rtma_data_2 = rtma_data[2]
            rtma_data_3 = rtma_data[3]
            rtma_data_4 = rtma_data[4]
            rtma_data_5 = rtma_data[5]
            rtma_data_6 = rtma_data[6]

            rtma_time_0 = rtma_time[0]
            rtma_time_1 = rtma_time[1]
            rtma_time_2 = rtma_time[2]
            rtma_time_3 = rtma_time[3]
            rtma_time_4 = rtma_time[4]
            rtma_time_5 = rtma_time[5]
            rtma_time_6 = rtma_time[6]
            
            NOMADS = False
            print("Unpacked the data successfully!")
                
        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds_list, rtma_times = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_rtma_data_past_6hrs()
            ds_0 = ds_list[0]
            ds_1 = ds_list[1]
            ds_2 = ds_list[2]
            ds_3 = ds_list[3]
            ds_4 = ds_list[4]
            ds_5 = ds_list[5]
            ds_6 = ds_list[6]

            rtma_time_0 = rtma_times[0]
            rtma_time_1 = rtma_times[1]
            rtma_time_2 = rtma_times[2]
            rtma_time_3 = rtma_times[3]
            rtma_time_4 = rtma_times[4]
            rtma_time_5 = rtma_times[5]
            rtma_time_6 = rtma_times[6]

            temp_0 = ds_0['tmp2m']
            temp_1 = ds_1['tmp2m']
            temp_2 = ds_2['tmp2m']
            temp_3 = ds_3['tmp2m']
            temp_4 = ds_4['tmp2m']
            temp_5 = ds_5['tmp2m']
            temp_6 = ds_6['tmp2m']

            lat_0 = temp_0['lat']
            lon_0 = temp_0['lon']
            lat_1 = temp_1['lat']
            lon_1 = temp_1['lon']
            lat_2 = temp_2['lat']
            lon_2 = temp_2['lon']
            lat_3 = temp_3['lat']
            lon_3 = temp_3['lon']
            lat_4 = temp_4['lat']
            lon_4 = temp_4['lon']
            lat_5 = temp_5['lat']
            lon_5 = temp_5['lon']
            lat_6 = temp_6['lat']
            lon_6 = temp_6['lon']

            temp_0 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_0)
            temp_1 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_1)
            temp_2 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_2)
            temp_3 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_3)
            temp_4 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_4)
            temp_5 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_5)
            temp_6 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_6)

            NOMADS = True
            print("Unpacked the data successfully!")

    elif rtma_data != None and rtma_time != None:
        try:
            rtma_data_0 = rtma_data[0]
            rtma_data_1 = rtma_data[1]
            rtma_data_2 = rtma_data[2]
            rtma_data_3 = rtma_data[3]
            rtma_data_4 = rtma_data[4]
            rtma_data_5 = rtma_data[5]
            rtma_data_6 = rtma_data[6]

            rtma_time_0 = rtma_time[0]
            rtma_time_1 = rtma_time[1]
            rtma_time_2 = rtma_time[2]
            rtma_time_3 = rtma_time[3]
            rtma_time_4 = rtma_time[4]
            rtma_time_5 = rtma_time[5]
            rtma_time_6 = rtma_time[6]
            
            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_past_6hrs('Temperature_Analysis_height_above_ground')
    
                rtma_data_0 = rtma_data[0]
                rtma_data_1 = rtma_data[1]
                rtma_data_2 = rtma_data[2]
                rtma_data_3 = rtma_data[3]
                rtma_data_4 = rtma_data[4]
                rtma_data_5 = rtma_data[5]
                rtma_data_6 = rtma_data[6]
    
                rtma_time_0 = rtma_time[0]
                rtma_time_1 = rtma_time[1]
                rtma_time_2 = rtma_time[2]
                rtma_time_3 = rtma_time[3]
                rtma_time_4 = rtma_time[4]
                rtma_time_5 = rtma_time[5]
                rtma_time_6 = rtma_time[6]
                
                NOMADS = False
                print("Unpacked the data successfully!")
                    
            except Exception as e:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds_list, rtma_times = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_rtma_data_past_6hrs()
                ds_0 = ds_list[0]
                ds_1 = ds_list[1]
                ds_2 = ds_list[2]
                ds_3 = ds_list[3]
                ds_4 = ds_list[4]
                ds_5 = ds_list[5]
                ds_6 = ds_list[6]
    
                rtma_time_0 = rtma_times[0]
                rtma_time_1 = rtma_times[1]
                rtma_time_2 = rtma_times[2]
                rtma_time_3 = rtma_times[3]
                rtma_time_4 = rtma_times[4]
                rtma_time_5 = rtma_times[5]
                rtma_time_6 = rtma_times[6]
    
                temp_0 = ds_0['tmp2m']
                temp_1 = ds_1['tmp2m']
                temp_2 = ds_2['tmp2m']
                temp_3 = ds_3['tmp2m']
                temp_4 = ds_4['tmp2m']
                temp_5 = ds_5['tmp2m']
                temp_6 = ds_6['tmp2m']
    
                lat_0 = temp_0['lat']
                lon_0 = temp_0['lon']
                lat_1 = temp_1['lat']
                lon_1 = temp_1['lon']
                lat_2 = temp_2['lat']
                lon_2 = temp_2['lon']
                lat_3 = temp_3['lat']
                lon_3 = temp_3['lon']
                lat_4 = temp_4['lat']
                lon_4 = temp_4['lon']
                lat_5 = temp_5['lat']
                lon_5 = temp_5['lon']
                lat_6 = temp_6['lat']
                lon_6 = temp_6['lon']
    
                temp_0 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_0)
                temp_1 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_1)
                temp_2 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_2)
                temp_3 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_3)
                temp_4 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_4)
                temp_5 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_5)
                temp_6 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_6)
    
                NOMADS = True
                print("Unpacked the data successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    rtma_time_0 = rtma_time_0.replace(tzinfo=from_zone)
    rtma_time_0 = rtma_time_0.astimezone(to_zone)
    rtma_time_utc_0 = rtma_time_0.astimezone(from_zone)

    rtma_time_1 = rtma_time_1.replace(tzinfo=from_zone)
    rtma_time_1 = rtma_time_1.astimezone(to_zone)
    rtma_time_utc_1 = rtma_time_1.astimezone(from_zone)

    rtma_time_2 = rtma_time_2.replace(tzinfo=from_zone)
    rtma_time_2 = rtma_time_2.astimezone(to_zone)
    rtma_time_utc_2 = rtma_time_2.astimezone(from_zone)

    rtma_time_3 = rtma_time_3.replace(tzinfo=from_zone)
    rtma_time_3 = rtma_time_3.astimezone(to_zone)
    rtma_time_utc_3 = rtma_time_3.astimezone(from_zone)
    
    rtma_time_4 = rtma_time_4.replace(tzinfo=from_zone)
    rtma_time_4 = rtma_time_4.astimezone(to_zone)
    rtma_time_utc_4 = rtma_time_4.astimezone(from_zone)

    rtma_time_5 = rtma_time_5.replace(tzinfo=from_zone)
    rtma_time_5 = rtma_time_5.astimezone(to_zone)
    rtma_time_utc_5 = rtma_time_5.astimezone(from_zone)

    rtma_time_6 = rtma_time_6.replace(tzinfo=from_zone)
    rtma_time_6 = rtma_time_6.astimezone(to_zone)
    rtma_time_utc_6 = rtma_time_6.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    cmap = colormaps.temperature_colormap()

    figs = []

    ################
    # FIRST FIGURE #
    ################

    if NOMADS == False:

        rtma_data_0 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_0)
        rtma_data_1 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_1)
        rtma_data_2 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_2)
        rtma_data_3 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_3)
        rtma_data_4 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_4)
        rtma_data_5 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_5)
        rtma_data_6 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_6)

        plot_proj_0 = rtma_data_0.metpy.cartopy_crs
        plot_proj_1 = rtma_data_1.metpy.cartopy_crs
        plot_proj_2 = rtma_data_2.metpy.cartopy_crs
        plot_proj_3 = rtma_data_3.metpy.cartopy_crs
        plot_proj_4 = rtma_data_4.metpy.cartopy_crs
        plot_proj_5 = rtma_data_5.metpy.cartopy_crs
        plot_proj_6 = rtma_data_6.metpy.cartopy_crs

        rtma_df0 = rtma_data_0.to_dataframe()
        rtma_df1 = rtma_data_1.to_dataframe()
        rtma_df2 = rtma_data_2.to_dataframe()
        rtma_df3 = rtma_data_3.to_dataframe()
        rtma_df4 = rtma_data_4.to_dataframe()
        rtma_df5 = rtma_data_5.to_dataframe()
        rtma_df6 = rtma_data_6.to_dataframe()

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')

        ax1 = fig1.add_subplot(1, 1, 1, projection=plot_proj_0)
        ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs1 = ax1.contourf(rtma_data_0.metpy.x, rtma_data_0.metpy.y, rtma_data_0, 
                         transform=rtma_data_0.metpy.cartopy_crs, levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha, extend='both')


        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink, pad=colorbar_pad)
        cbar1.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn1 = mpplots.StationPlot(ax1, rtma_df0['longitude'][::decimate], rtma_df0['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn1.plot_parameter('C', rtma_df0['Temperature_Analysis_height_above_ground'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig1.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_0.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_0.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax1.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax1.transAxes)

        #################
        # SECOND FIGURE #
        #################

        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')

        ax2 = fig2.add_subplot(1, 1, 1, projection=plot_proj_1)
        ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs2 = ax2.contourf(rtma_data_1.metpy.x, rtma_data_1.metpy.y, rtma_data_1, 
                         transform=rtma_data_1.metpy.cartopy_crs, levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha, extend='both')

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink, pad=colorbar_pad)
        cbar2.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn2 = mpplots.StationPlot(ax2, rtma_df1['longitude'][::decimate], rtma_df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn2.plot_parameter('C', rtma_df1['Temperature_Analysis_height_above_ground'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig2.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_1.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax2.transAxes)

        ################
        # THIRD FIGURE #
        ################

        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')

        ax3 = fig3.add_subplot(1, 1, 1, projection=plot_proj_2)
        ax3.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs3 = ax3.contourf(rtma_data_2.metpy.x, rtma_data_2.metpy.y, rtma_data_2, 
                         transform=rtma_data_2.metpy.cartopy_crs, levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha, extend='both')

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink, pad=colorbar_pad)
        cbar3.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn3 = mpplots.StationPlot(ax3, rtma_df2['longitude'][::decimate], rtma_df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn3.plot_parameter('C', rtma_df2['Temperature_Analysis_height_above_ground'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig3.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_2.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax3.transAxes)


        #################
        # FOURTH FIGURE #
        #################

        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')

        ax4 = fig4.add_subplot(1, 1, 1, projection=plot_proj_3)
        ax4.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs4 = ax4.contourf(rtma_data_3.metpy.x, rtma_data_3.metpy.y, rtma_data_3, 
                         transform=rtma_data_3.metpy.cartopy_crs, levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha, extend='both')

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink, pad=colorbar_pad)
        cbar4.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn4 = mpplots.StationPlot(ax4, rtma_df3['longitude'][::decimate], rtma_df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn4.plot_parameter('C', rtma_df3['Temperature_Analysis_height_above_ground'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig4.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_3.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax4.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax4.transAxes)


        ################
        # FIFTH FIGURE #
        ################

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')

        ax5 = fig5.add_subplot(1, 1, 1, projection=plot_proj_4)
        ax5.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax5.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs5 = ax5.contourf(rtma_data_4.metpy.x, rtma_data_4.metpy.y, rtma_data_4, 
                         transform=rtma_data_4.metpy.cartopy_crs, levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha, extend='both')

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink, pad=colorbar_pad)
        cbar5.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn5 = mpplots.StationPlot(ax5, rtma_df4['longitude'][::decimate], rtma_df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn5.plot_parameter('C', rtma_df4['Temperature_Analysis_height_above_ground'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig5.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_4.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)

        ################
        # SIXTH FIGURE #
        ################

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')

        ax6 = fig6.add_subplot(1, 1, 1, projection=plot_proj_5)
        ax6.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax6.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs6 = ax6.contourf(rtma_data_5.metpy.x, rtma_data_5.metpy.y, rtma_data_5, 
                         transform=rtma_data_5.metpy.cartopy_crs, levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha, extend='both')

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink, pad=colorbar_pad)
        cbar6.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn6 = mpplots.StationPlot(ax6, rtma_df5['longitude'][::decimate], rtma_df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn6.plot_parameter('C', rtma_df5['Temperature_Analysis_height_above_ground'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig6.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_5.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax6.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax6.transAxes)

        ##################
        # SEVENTH FIGURE #
        ##################

        fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig7.set_facecolor('aliceblue')

        ax7 = fig7.add_subplot(1, 1, 1, projection=plot_proj_6)
        ax7.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax7.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs7 = ax7.contourf(rtma_data_6.metpy.x, rtma_data_6.metpy.y, rtma_data_6, 
                         transform=rtma_data_6.metpy.cartopy_crs, levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha, extend='both')

        cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink, pad=colorbar_pad)
        cbar7.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn7 = mpplots.StationPlot(ax7, rtma_df6['longitude'][::decimate], rtma_df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn7.plot_parameter('C', rtma_df6['Temperature_Analysis_height_above_ground'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        fig7.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_6.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax7.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax7.transAxes)

    if NOMADS == True:

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')

        ax1 = fig1.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs1 = ax1.contourf(lon_0, lat_0, temp_0[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha)

        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink, pad=colorbar_pad)
        cbar1.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig1.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_0.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_0.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax1.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax1.transAxes)

        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')

        ax2 = fig2.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs2 = ax2.contourf(lon_1, lat_1, temp_1[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha)

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink, pad=colorbar_pad)
        cbar2.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig2.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_1.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax2.transAxes)


        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')

        ax3 = fig3.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax3.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs3 = ax3.contourf(lon_2, lat_2, temp_2[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha)

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink, pad=colorbar_pad)
        cbar3.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig3.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_2.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax3.transAxes)

        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')

        ax4 = fig4.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax4.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs4 = ax4.contourf(lon_3, lat_3, temp_3[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha)

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink, pad=colorbar_pad)
        cbar4.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig4.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_3.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax4.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax4.transAxes)

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')

        ax5 = fig5.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax5.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax5.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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

        cs5 = ax5.contourf(lon_4, lat_4, temp_4[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha)

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink, pad=colorbar_pad)
        cbar5.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig5.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_4.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')

        ax6 = fig6.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax6.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax6.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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

        cs6 = ax6.contourf(lon_5, lat_5, temp_5[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha)

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink, pad=colorbar_pad)
        cbar6.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig6.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_5.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax6.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax6.transAxes)

        fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig7.set_facecolor('aliceblue')

        ax7 = fig7.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax7.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax7.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs7 = ax7.contourf(lon_6, lat_6, temp_6[0, :, :], 
                         transform=ccrs.PlateCarree(), levels=np.arange(temperature_bottom_bound, temperature_top_bound + temperature_step, temperature_step), cmap=cmap, alpha=alpha)

        cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink, pad=colorbar_pad)
        cbar7.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig7.suptitle("Real Time Mesoscale Analysis Temperature\nAnalysis Valid: " + rtma_time_6.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax7.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax7.transAxes)

    figs.append(fig7)
    figs.append(fig6)
    figs.append(fig5)
    figs.append(fig4)
    figs.append(fig3)
    figs.append(fig2)
    figs.append(fig1)

    return figs



def plot_temperature_trend_6hr_timelapse(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, decimate='default', data=None, time=None):

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

    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate

    local_time, utc_time = standard.plot_creation_time()
    rtma_data = data
    rtma_time = time

    if rtma_data == None and rtma_time == None:

        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_past_6hrs('Temperature_Analysis_height_above_ground')

            rtma_data_0 = rtma_data[0]
            rtma_data_1 = rtma_data[1]
            rtma_data_2 = rtma_data[2]
            rtma_data_3 = rtma_data[3]
            rtma_data_4 = rtma_data[4]
            rtma_data_5 = rtma_data[5]
            rtma_data_6 = rtma_data[6]
            rtma_data_7 = rtma_data[7]

            rtma_time_0 = rtma_time[0]
            rtma_time_1 = rtma_time[1]
            rtma_time_2 = rtma_time[2]
            rtma_time_3 = rtma_time[3]
            rtma_time_4 = rtma_time[4]
            rtma_time_5 = rtma_time[5]
            rtma_time_6 = rtma_time[6]
            rtma_time_7 = rtma_time[7]
            
            NOMADS = False
            print("Unpacked the data successfully!")
                
        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds_list, rtma_times = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_rtma_data_past_6hrs()
            ds_0 = ds_list[0]
            ds_1 = ds_list[1]
            ds_2 = ds_list[2]
            ds_3 = ds_list[3]
            ds_4 = ds_list[4]
            ds_5 = ds_list[5]
            ds_6 = ds_list[6]
            ds_7 = ds_list[7]

            rtma_time_0 = rtma_times[0]
            rtma_time_1 = rtma_times[1]
            rtma_time_2 = rtma_times[2]
            rtma_time_3 = rtma_times[3]
            rtma_time_4 = rtma_times[4]
            rtma_time_5 = rtma_times[5]
            rtma_time_6 = rtma_times[6]
            rtma_time_7 = rtma_times[7]

            temp_0 = ds_0['tmp2m']
            temp_1 = ds_1['tmp2m']
            temp_2 = ds_2['tmp2m']
            temp_3 = ds_3['tmp2m']
            temp_4 = ds_4['tmp2m']
            temp_5 = ds_5['tmp2m']
            temp_6 = ds_6['tmp2m']
            temp_7 = ds_7['tmp2m']

            lat_0 = temp_0['lat']
            lon_0 = temp_0['lon']
            lat_1 = temp_1['lat']
            lon_1 = temp_1['lon']
            lat_2 = temp_2['lat']
            lon_2 = temp_2['lon']
            lat_3 = temp_3['lat']
            lon_3 = temp_3['lon']
            lat_4 = temp_4['lat']
            lon_4 = temp_4['lon']
            lat_5 = temp_5['lat']
            lon_5 = temp_5['lon']
            lat_6 = temp_6['lat']
            lon_6 = temp_6['lon']
            lat_7 = temp_7['lat']
            lon_7 = temp_7['lon']

            temp_0 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_0)
            temp_1 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_1)
            temp_2 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_2)
            temp_3 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_3)
            temp_4 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_4)
            temp_5 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_5)
            temp_6 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_6)
            temp_7 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_7)

            diff1 = temp_0[0, :, :] - temp_1[0, :, :]
            diff2 = temp_1[0, :, :] - temp_2[0, :, :]
            diff3 = temp_2[0, :, :] - temp_3[0, :, :]
            diff4 = temp_3[0, :, :] - temp_4[0, :, :]
            diff5 = temp_4[0, :, :] - temp_5[0, :, :]
            diff6 = temp_5[0, :, :] - temp_6[0, :, :]
            diff7 = temp_6[0, :, :] - temp_7[0, :, :]

            NOMADS = True 
            print("Unpacked the data successfully!")

    elif rtma_data != None and rtma_time != None:
        try:
            rtma_data_0 = rtma_data[0]
            rtma_data_1 = rtma_data[1]
            rtma_data_2 = rtma_data[2]
            rtma_data_3 = rtma_data[3]
            rtma_data_4 = rtma_data[4]
            rtma_data_5 = rtma_data[5]
            rtma_data_6 = rtma_data[6]
            rtma_data_7 = rtma_data[7]

            rtma_time_0 = rtma_time[0]
            rtma_time_1 = rtma_time[1]
            rtma_time_2 = rtma_time[2]
            rtma_time_3 = rtma_time[3]
            rtma_time_4 = rtma_time[4]
            rtma_time_5 = rtma_time[5]
            rtma_time_6 = rtma_time[6]
            rtma_time_7 = rtma_time[7]
            
            NOMADS = False
            print("Unpacked the data successfully!")
        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_past_6hrs('Temperature_Analysis_height_above_ground')
    
                rtma_data_0 = rtma_data[0]
                rtma_data_1 = rtma_data[1]
                rtma_data_2 = rtma_data[2]
                rtma_data_3 = rtma_data[3]
                rtma_data_4 = rtma_data[4]
                rtma_data_5 = rtma_data[5]
                rtma_data_6 = rtma_data[6]
                rtma_data_7 = rtma_data[7]
    
                rtma_time_0 = rtma_time[0]
                rtma_time_1 = rtma_time[1]
                rtma_time_2 = rtma_time[2]
                rtma_time_3 = rtma_time[3]
                rtma_time_4 = rtma_time[4]
                rtma_time_5 = rtma_time[5]
                rtma_time_6 = rtma_time[6]
                rtma_time_7 = rtma_time[7]
                
                NOMADS = False
                print("Unpacked the data successfully!")
                    
            except Exception as e:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds_list, rtma_times = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_rtma_data_past_6hrs()
                ds_0 = ds_list[0]
                ds_1 = ds_list[1]
                ds_2 = ds_list[2]
                ds_3 = ds_list[3]
                ds_4 = ds_list[4]
                ds_5 = ds_list[5]
                ds_6 = ds_list[6]
                ds_7 = ds_list[7]
    
                rtma_time_0 = rtma_times[0]
                rtma_time_1 = rtma_times[1]
                rtma_time_2 = rtma_times[2]
                rtma_time_3 = rtma_times[3]
                rtma_time_4 = rtma_times[4]
                rtma_time_5 = rtma_times[5]
                rtma_time_6 = rtma_times[6]
                rtma_time_7 = rtma_times[7]
    
                temp_0 = ds_0['tmp2m']
                temp_1 = ds_1['tmp2m']
                temp_2 = ds_2['tmp2m']
                temp_3 = ds_3['tmp2m']
                temp_4 = ds_4['tmp2m']
                temp_5 = ds_5['tmp2m']
                temp_6 = ds_6['tmp2m']
                temp_7 = ds_7['tmp2m']
    
                lat_0 = temp_0['lat']
                lon_0 = temp_0['lon']
                lat_1 = temp_1['lat']
                lon_1 = temp_1['lon']
                lat_2 = temp_2['lat']
                lon_2 = temp_2['lon']
                lat_3 = temp_3['lat']
                lon_3 = temp_3['lon']
                lat_4 = temp_4['lat']
                lon_4 = temp_4['lon']
                lat_5 = temp_5['lat']
                lon_5 = temp_5['lon']
                lat_6 = temp_6['lat']
                lon_6 = temp_6['lon']
                lat_7 = temp_7['lat']
                lon_7 = temp_7['lon']
    
                temp_0 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_0)
                temp_1 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_1)
                temp_2 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_2)
                temp_3 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_3)
                temp_4 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_4)
                temp_5 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_5)
                temp_6 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_6)
                temp_7 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_7)
    
                diff1 = temp_0[0, :, :] - temp_1[0, :, :]
                diff2 = temp_1[0, :, :] - temp_2[0, :, :]
                diff3 = temp_2[0, :, :] - temp_3[0, :, :]
                diff4 = temp_3[0, :, :] - temp_4[0, :, :]
                diff5 = temp_4[0, :, :] - temp_5[0, :, :]
                diff6 = temp_5[0, :, :] - temp_6[0, :, :]
                diff7 = temp_6[0, :, :] - temp_7[0, :, :]
    
                NOMADS = True 
                print("Unpacked the data successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")        

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    rtma_time_0 = rtma_time_0.replace(tzinfo=from_zone)
    rtma_time_0 = rtma_time_0.astimezone(to_zone)
    rtma_time_utc_0 = rtma_time_0.astimezone(from_zone)

    rtma_time_1 = rtma_time_1.replace(tzinfo=from_zone)
    rtma_time_1 = rtma_time_1.astimezone(to_zone)
    rtma_time_utc_1 = rtma_time_1.astimezone(from_zone)

    rtma_time_2 = rtma_time_2.replace(tzinfo=from_zone)
    rtma_time_2 = rtma_time_2.astimezone(to_zone)
    rtma_time_utc_2 = rtma_time_2.astimezone(from_zone)

    rtma_time_3 = rtma_time_3.replace(tzinfo=from_zone)
    rtma_time_3 = rtma_time_3.astimezone(to_zone)
    rtma_time_utc_3 = rtma_time_3.astimezone(from_zone)

    rtma_time_4 = rtma_time_4.replace(tzinfo=from_zone)
    rtma_time_4 = rtma_time_4.astimezone(to_zone)
    rtma_time_utc_4 = rtma_time_4.astimezone(from_zone)

    rtma_time_5 = rtma_time_5.replace(tzinfo=from_zone)
    rtma_time_5 = rtma_time_5.astimezone(to_zone)
    rtma_time_utc_5 = rtma_time_5.astimezone(from_zone)

    rtma_time_6 = rtma_time_6.replace(tzinfo=from_zone)
    rtma_time_6 = rtma_time_6.astimezone(to_zone)
    rtma_time_utc_6 = rtma_time_6.astimezone(from_zone)

    rtma_time_7 = rtma_time_7.replace(tzinfo=from_zone)
    rtma_time_7 = rtma_time_7.astimezone(to_zone)
    rtma_time_utc_7 = rtma_time_7.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    figs = []

    ################
    # FIRST FIGURE #
    ################

    if NOMADS == False:

        rtma_data_0 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_0)
        rtma_data_1 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_1)
        rtma_data_2 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_2)
        rtma_data_3 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_3)
        rtma_data_4 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_4)
        rtma_data_5 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_5)
        rtma_data_6 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_6)
        rtma_data_7 = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data_7)

        diff1 = rtma_data_0 - rtma_data_1
        diff2 = rtma_data_1 - rtma_data_2
        diff3 = rtma_data_2 - rtma_data_3
        diff4 = rtma_data_3 - rtma_data_4
        diff5 = rtma_data_4 - rtma_data_5
        diff6 = rtma_data_5 - rtma_data_6
        diff7 = rtma_data_6 - rtma_data_7

        rtma_df1 = diff1.to_dataframe()
        rtma_df2 = diff2.to_dataframe()
        rtma_df3 = diff3.to_dataframe()
        rtma_df4 = diff4.to_dataframe()
        rtma_df5 = diff5.to_dataframe()
        rtma_df6 = diff6.to_dataframe()
        rtma_df7 = diff7.to_dataframe()

        plot_proj_8 = diff1.metpy.cartopy_crs
        plot_proj_9 = diff2.metpy.cartopy_crs
        plot_proj_10 = diff3.metpy.cartopy_crs
        plot_proj_11 = diff4.metpy.cartopy_crs
        plot_proj_12 = diff5.metpy.cartopy_crs
        plot_proj_13 = diff6.metpy.cartopy_crs
        plot_proj_14 = diff7.metpy.cartopy_crs

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')

        fig1.suptitle("RTMA Hourly Temperature Trend (Shaded)\nValid: "+rtma_time_0.strftime('%H:00 Local') + " (" + rtma_time_utc_0.strftime('%H:00 UTC')+")" + " - " + rtma_time_1.strftime('%H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax1 = fig1.add_subplot(1, 1, 1, projection=plot_proj_8)
        ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs1 = ax1.contourf(diff1.metpy.x, diff1.metpy.y, diff1, 
                         transform=diff1.metpy.cartopy_crs, levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha, extend='both')

        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink, pad=colorbar_pad)
        cbar1.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn1 = mpplots.StationPlot(ax1, rtma_df1['longitude'][::decimate], rtma_df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn1.plot_parameter('C', rtma_df1['Temperature_Analysis_height_above_ground'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass
        

        ax1.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax1.transAxes)


        #################
        # SECOND FIGURE #
        #################

        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')

        fig2.suptitle("RTMA Hourly Temperature Trend (Shaded)\nValid: "+rtma_time_1.strftime('%H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")" + " - " + rtma_time_2.strftime('%H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax2 = fig2.add_subplot(1, 1, 1, projection=plot_proj_9)
        ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs2 = ax2.contourf(diff2.metpy.x, diff2.metpy.y, diff2, 
                         transform=diff2.metpy.cartopy_crs, levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha, extend='both')

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink, pad=colorbar_pad)
        cbar2.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn2 = mpplots.StationPlot(ax2, rtma_df2['longitude'][::decimate], rtma_df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn2.plot_parameter('C', rtma_df2['Temperature_Analysis_height_above_ground'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass


        ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax2.transAxes)


        ################
        # THIRD FIGURE #
        ################

        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')

        fig3.suptitle("RTMA Hourly Temperature Trend (Shaded)\nValid: "+rtma_time_2.strftime('%H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")" + " - " + rtma_time_3.strftime('%H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax3 = fig3.add_subplot(1, 1, 1, projection=plot_proj_10)
        ax3.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass
            
        cs3 = ax3.contourf(diff3.metpy.x, diff3.metpy.y, diff3, 
                         transform=diff3.metpy.cartopy_crs, levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha, extend='both')

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink, pad=colorbar_pad)
        cbar3.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn3 = mpplots.StationPlot(ax3, rtma_df3['longitude'][::decimate], rtma_df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn3.plot_parameter('C', rtma_df3['Temperature_Analysis_height_above_ground'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass
        

        ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax3.transAxes)


        #################
        # FOURTH FIGURE #
        #################

        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')

        fig4.suptitle("RTMA Hourly Temperature Trend (Shaded)\nValid: "+rtma_time_3.strftime('%H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")" + " - " + rtma_time_4.strftime('%H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax4 = fig4.add_subplot(1, 1, 1, projection=plot_proj_11)
        ax4.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass    
        cs4 = ax4.contourf(diff4.metpy.x, diff4.metpy.y, diff4, 
                         transform=diff4.metpy.cartopy_crs, levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha, extend='both')

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink, pad=colorbar_pad)
        cbar4.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn4 = mpplots.StationPlot(ax4, rtma_df4['longitude'][::decimate], rtma_df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn4.plot_parameter('C', rtma_df4['Temperature_Analysis_height_above_ground'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        ax4.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax4.transAxes)


        ################
        # FIFTH FIGURE #
        ################

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')

        fig5.suptitle("RTMA Hourly Temperature Trend (Shaded)\nValid: "+rtma_time_4.strftime('%H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")" + " - " + rtma_time_5.strftime('%H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax5 = fig5.add_subplot(1, 1, 1, projection=plot_proj_12)
        ax5.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax5.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass    
        cs5 = ax5.contourf(diff5.metpy.x, diff5.metpy.y, diff5, 
                         transform=diff5.metpy.cartopy_crs, levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha, extend='both')

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink, pad=colorbar_pad)
        cbar5.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn5 = mpplots.StationPlot(ax5, rtma_df5['longitude'][::decimate], rtma_df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn5.plot_parameter('C', rtma_df5['Temperature_Analysis_height_above_ground'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass


        ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)

        ################
        # SIXTH FIGURE #
        ################

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')

        fig6.suptitle("RTMA Hourly Temperature Trend (Shaded)\nValid: "+rtma_time_5.strftime('%H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")" + " - " + rtma_time_6.strftime('%H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax6 = fig6.add_subplot(1, 1, 1, projection=plot_proj_13)
        ax6.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax6.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass    
        cs6 = ax6.contourf(diff6.metpy.x, diff6.metpy.y, diff6, 
                         transform=diff6.metpy.cartopy_crs, levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha, extend='both')

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink, pad=colorbar_pad)
        cbar6.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn6 = mpplots.StationPlot(ax6, rtma_df6['longitude'][::decimate], rtma_df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn6.plot_parameter('C', rtma_df6['Temperature_Analysis_height_above_ground'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass
        
        ax6.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax6.transAxes)

        ##################
        # SEVENTH FIGURE #
        ##################

        fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig7.set_facecolor('aliceblue')

        fig7.suptitle("RTMA Hourly Temperature Trend (Shaded)\nValid: "+rtma_time_6.strftime('%H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")" + " - " + rtma_time_7.strftime('%H:00 Local') + " (" + rtma_time_utc_7.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')

        ax7 = fig7.add_subplot(1, 1, 1, projection=plot_proj_14)
        ax7.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax7.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        else:
            pass
        if show_gacc_borders == True:
            ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass
            
        cs7 = ax7.contourf(diff7.metpy.x, diff7.metpy.y, diff7, 
                         transform=diff7.metpy.cartopy_crs, levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha, extend='both')

        cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink, pad=colorbar_pad)
        cbar7.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        if show_sample_points == True:

            stn7 = mpplots.StationPlot(ax7, rtma_df7['longitude'][::decimate], rtma_df7['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn7.plot_parameter('C', rtma_df7['Temperature_Analysis_height_above_ground'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass
        
        ax7.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax7.transAxes)

    if NOMADS == True:

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')

        ax1 = fig1.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs1 = ax1.contourf(lon_0, lat_0, diff1, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha)

        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink, pad=colorbar_pad)
        cbar1.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig1.suptitle("RTMA Hourly Temperature Trend\nValid: "+rtma_time_0.strftime('%H:00 Local') + " (" + rtma_time_utc_0.strftime('%H:00 UTC')+")" + " - " + rtma_time_1.strftime('%H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax1.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax1.transAxes)

        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')

        ax2 = fig2.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs2 = ax2.contourf(lon_1, lat_1, diff2, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha)

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink, pad=colorbar_pad)
        cbar2.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig2.suptitle("RTMA Hourly Temperature Trend\nValid: "+rtma_time_1.strftime('%H:00 Local') + " (" + rtma_time_utc_1.strftime('%H:00 UTC')+")" + " - " + rtma_time_2.strftime('%H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax2.transAxes)


        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')

        ax3 = fig3.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax3.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs3 = ax3.contourf(lon_2, lat_2, diff3, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha)

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink, pad=colorbar_pad)
        cbar3.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig3.suptitle("RTMA Hourly Temperature Trend\nValid: "+rtma_time_2.strftime('%H:00 Local') + " (" + rtma_time_utc_2.strftime('%H:00 UTC')+")" + " - " + rtma_time_3.strftime('%H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax3.transAxes)

        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')

        ax4 = fig4.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax4.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs4 = ax4.contourf(lon_3, lat_3, diff4, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha)

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink, pad=colorbar_pad)
        cbar4.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig4.suptitle("RTMA Hourly Temperature Trend\nValid: "+rtma_time_3.strftime('%H:00 Local') + " (" + rtma_time_utc_3.strftime('%H:00 UTC')+")" + " - " + rtma_time_4.strftime('%H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax4.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax4.transAxes)

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')

        ax5 = fig5.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax5.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax5.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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

        cs5 = ax5.contourf(lon_4, lat_4, diff5, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha)

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink, pad=colorbar_pad)
        cbar5.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig5.suptitle("RTMA Hourly Temperature Trend\nValid: "+rtma_time_4.strftime('%H:00 Local') + " (" + rtma_time_utc_4.strftime('%H:00 UTC')+")" + " - " + rtma_time_5.strftime('%H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')

        ax6 = fig6.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax6.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax6.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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

        cs6 = ax6.contourf(lon_5, lat_5, diff6, 
                         transform=ccrs.PlateCarree(), levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha)

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink, pad=colorbar_pad)
        cbar6.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig6.suptitle("RTMA Hourly Temperature Trend\nValid: "+rtma_time_5.strftime('%H:00 Local') + " (" + rtma_time_utc_5.strftime('%H:00 UTC')+")" + " - " + rtma_time_6.strftime('%H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax6.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax6.transAxes)

        fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig7.set_facecolor('aliceblue')

        ax7 = fig7.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax7.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax7.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
        if show_gacc_borders == True:
            ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        cs7 = ax7.contourf(lon_6, lat_6, diff7,
                         transform=ccrs.PlateCarree(), levels=np.arange(-15, 16, 1), cmap='seismic', alpha=alpha)

        cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink, pad=colorbar_pad)
        cbar7.set_label(label="Hourly Temperature Trend (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')

        fig7.suptitle("RTMA Hourly Temperature Trend\nValid: "+rtma_time_6.strftime('%H:00 Local') + " (" + rtma_time_utc_6.strftime('%H:00 UTC')+")" + " - " + rtma_time_7.strftime('%H:00 Local') + " (" + rtma_time_utc_7.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax7.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax7.transAxes)

    figs.append(fig7)
    figs.append(fig6)
    figs.append(fig5)
    figs.append(fig4)
    figs.append(fig3)
    figs.append(fig2)
    figs.append(fig1)

    return figs
    

def plot_low_and_high_relative_humidity(low_relative_humidity_threshold, high_relative_humidity_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, decimate='default', data=None, time=None):

    r'''
        This function does the following:
                                        1) Downloads the latest availiable temperature and dewpoint data arrays. 
                                        2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data arrays. 
                                        4) Plots the relative humidity data filtered RH <= low_relative_humidity_threshold (%) and RH >= high_relative_humidity_threshold (%)

        

        Inputs:

            1) low_relative_humidity_threshold (Integer) - The user defines the threshold for what is considered low relative humidity for the respective geographic area.  

            2) high_relative_humidity_threshold (Integer) - The user defines the threshold for what is considered high relative humidity for the respective geographic area.  

            3) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.

            4) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.

            5) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.

            6) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.

            7) central_longitude (Integer or Float) - The central longitude. Defaults to -96.

            8) central_latitude (Integer or Float) - The central latitude. Defaults to 39.

            9) first_standard_parallel (Integer or Float) - Southern standard parallel. 

            10) second_standard_parallel (Integer or Float) - Northern standard parallel. 
            
            11) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

            12) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

            13) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

            14) decimate (Integer) - Distance in meters to decimate METAR stations apart from eachother so stations don't clutter the plot. The higher the value, the less stations are displayed. 

            15) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            16) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            17) title_font_size (Integer) - The fontsize of the title of the figure. 

            18) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            19) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

            20) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                       Default setting is 0.05.
                                       Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                       Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

            21) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis relative humidity data filtered RH <= red_flag_warning_relative_humidity_threshold (%) overlayed with the latest METAR reports. 
    
    '''
    colorbar_label_font_size = colorbar_label_font_size

    colorbar_pad = colorbar_pad
    show_sample_points = show_sample_points
    sample_point_fontsize = sample_point_fontsize
    data = data
    try:
        if data == None:
            test = True
    except Exception as a:
        test = False
    time = time
    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate

    low_relative_humidity_threshold = low_relative_humidity_threshold
    low_relative_humidity_threshold_scale = low_relative_humidity_threshold + 1

    high_relative_humidity_threshold = high_relative_humidity_threshold
    high_relative_humidity_threshold_scale = high_relative_humidity_threshold

    local_time, utc_time = standard.plot_creation_time()

    if test == True and time == None:
        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)
            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            
            rtma_data = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            
            lat = ds['lat']
            lon = ds['lon']
            
            NOMADS = True
            print("Unpacked the data successfully!")

    elif test == False and time != None:
        try:
            rtma_data = data
            rtma_time = time
            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time1)
                NOMADS = False
                print("Unpacked the data successfully!")
    
            except Exception as e:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
                dwpt = ds['dpt2m']
                temp = temp - 273.15
                dwpt = dwpt - 273.15
                
                rtma_data = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                
                lat = ds['lat']
                lon = ds['lon']
                
                NOMADS = True
                print("Unpacked the data successfully!")                

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    cmap_high = colormaps.excellent_recovery_colormap()
    cmap_low = colormaps.low_relative_humidity_colormap()

    if NOMADS == False:
        plot_proj = rtma_data.metpy.cartopy_crs
        rtma_df = rtma_data.to_dataframe(name='rtma_rh')
        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
        ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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

        cs_low = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, low_relative_humidity_threshold_scale, 1), cmap=cmap_low, alpha=alpha)

        if show_sample_points == True:

            stn = mpplots.StationPlot(ax, rtma_df['longitude'][::decimate], rtma_df['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn.plot_parameter('C', rtma_df['rtma_rh'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        cs_high = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(high_relative_humidity_threshold_scale, 101, 1), cmap=cmap_high, alpha=alpha)


        cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
        cbar_low.set_label(label="Low Relative Humidity (RH <=" + str(low_relative_humidity_threshold) +"%)", size=colorbar_label_font_size, fontweight='bold')


        cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
        cbar_high.set_label(label="High Relative Humidity (RH >= " + str(high_relative_humidity_threshold) +"%)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA nLow RH (<=" + str(low_relative_humidity_threshold) +"%) & High RH (RH >= " + str(high_relative_humidity_threshold) +"%)\nAnalysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC')+")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    if NOMADS == True:
        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=datacrs)
        ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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

        cs_low = ax.contourf(lon, lat, rtma_data[0, :, :], 
                         transform=datacrs, levels=np.arange(0, low_relative_humidity_threshold_scale, 1), cmap=cmap_low, alpha=alpha)

        cs_high = ax.contourf(lon, lat, rtma_data[0, :, :], 
                         transform=datacrs, levels=np.arange(high_relative_humidity_threshold_scale, 101, 1), cmap=cmap_high, alpha=alpha)


        cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
        cbar_low.set_label(label="Low Relative Humidity (RH <=" + str(low_relative_humidity_threshold) +"%)", size=colorbar_label_font_size, fontweight='bold')


        cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
        cbar_high.set_label(label="High Relative Humidity (RH >= " + str(high_relative_humidity_threshold) +"%)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA Low RH (<=" + str(low_relative_humidity_threshold) +"%) & High RH (RH >= " + str(high_relative_humidity_threshold) +"%)\nAnalysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC')+")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_24_hour_relative_humidity_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, decimate='default', data=None, time=None):

    r'''
        This function does the following:
                                        1) Downloads the temperature and dewpoint data arrays for the current time and the data arrays for 24 hours ago from the data arrays for the current time.
                                        2) Uses MetPy to calculate the relative humidity from the temperature and dewpoint data arrays for both times (current time and current time - 24 hours).
                                        3) Subtracts the relative humidity data array from 24 hours ago from the relative humidity data array of the current time (Current RH - RH from 24 hours ago).
                                        4) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis of the difference between the current relative humidity data array from the relative humidity data array from 24 hours ago.
        

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

            12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            14) title_font_size (Integer) - The fontsize of the title of the figure. 

            15) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            16) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

            17) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                       Default setting is 0.05.
                                       Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                       Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

            18) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to relative humidity (%)
    
    '''

    western_bound = western_bound
    eastern_bound = eastern_bound
    southern_bound = southern_bound
    northern_bound = northern_bound
    
    data = data
    try:
        if data == None:
            test = True
    except Exception as a:
        test = False
            
    time = time
    
    local_time, utc_time = standard.plot_creation_time()
    
    cmap = colormaps.relative_humidity_change_colormap()

    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate

    if test == True and time == None:
        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_relative_humidity_24_hour_difference_data(utc_time)
            
            rtma_time_24 = rtma_time - timedelta(hours=24)

            rtma_df = rtma_data.to_dataframe(name='rtma_rh_change')

            plot_proj = rtma_data.metpy.cartopy_crs

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds, ds_24, rtma_time, rtma_time_24 = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_24_hour_comparison_datasets(utc_time)
            
            rtma_time_24 = rtma_time - timedelta(hours=24)

            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15

            temp_24 = ds_24['tmp2m']
            dwpt_24 = ds_24['dpt2m']
            temp_24 = temp_24 - 273.15
            dwpt_24 = dwpt_24 - 273.15

            rtma_data = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            
            rtma_data_24 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_24, dwpt_24)
            lat = ds['lat']
            lon = ds['lon']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']

            diff = rtma_data[0, :, :] - rtma_data_24[0, :, :]

            NOMADS = True
            print("Unpacked the data successfully!")

    elif test == False and time != None:
        try:
            rtma_data = data[0]
            rtma_time = time
            
            rtma_time_24 = rtma_time - timedelta(hours=24)
            
            rtma_df = rtma_data.to_dataframe(name='rtma_rh_change')

            plot_proj = rtma_data.metpy.cartopy_crs

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")

                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_relative_humidity_24_hour_difference_data(utc_time)
    
                rtma_df = rtma_data.to_dataframe(name='rtma_rh_change')
    
                plot_proj = rtma_data.metpy.cartopy_crs
                
                rtma_time_24 = rtma_time - timedelta(hours=24)
    
                NOMADS = False
                print("Unpacked the data successfully!")
    
            except Exception as e:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds, ds_24, rtma_time, rtma_time_24 = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_24_hour_comparison_datasets(utc_time)
    
                temp = ds['tmp2m']
                dwpt = ds['dpt2m']
                temp = temp - 273.15
                dwpt = dwpt - 273.15
    
                temp_24 = ds_24['tmp2m']
                dwpt_24 = ds_24['dpt2m']
                temp_24 = temp_24 - 273.15
                dwpt_24 = dwpt_24 - 273.15
    
                rtma_data = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                
                rtma_data_24 = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_24, dwpt_24)
                lat = ds['lat']
                lon = ds['lon']
                lat_24 = ds_24['lat']
                lon_24 = ds_24['lon']
    
                diff = rtma_data[0, :, :] - rtma_data_24[0, :, :]
    
                NOMADS = True
                rtma_time_24 = rtma_time - timedelta(hours=24)
                print("Unpacked the data successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")        

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    rtma_time_24_utc = rtma_time_24.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    if NOMADS == False:
        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
        ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        else:
            pass
        if show_gacc_borders == True:
            ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-50, 55, 5), cmap=cmap, alpha=alpha, extend='both')

        if show_sample_points == True:

            stn = mpplots.StationPlot(ax, rtma_df['longitude'][::decimate], rtma_df['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn.plot_parameter('C', rtma_df['rtma_rh_change'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass


        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Relative Humidity Change (%)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA 24-Hour Relative Humidity Change (%)\nAnalysis Start: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_24_utc.strftime('%H:00 UTC')+ ")\nAnalysis End:" + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    if NOMADS == True:
        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=datacrs)
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

        cs = ax.contourf(lon, lat, diff, 
                         transform=datacrs, levels=np.arange(-50, 55, 5), cmap=cmap, alpha=alpha, extend='both')

        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Relative Humidity Change (%)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA 24-Hour Relative Humidity Change (%)\nAnalysis Start: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_24_utc.strftime('%H:00 UTC')+ ")\nAnalysis End:" + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_24_hour_temperature_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, decimate='default', data=None, time=None):

    r'''
        This function does the following:
                                        1) Downloads the temperature data arrays for the current time and the data arrays for 24 hours ago from the data arrays for the current time.
                                        2) Converts the temperature values from Kelvin to Fahrenheit. 
                                        3) Subtracts the temperature data array from 24 hours ago from the temperature data array of the current time (Current Temperature - Temperature from 24 hours ago).
                                        4) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis of the difference between the current temperature data array from the temperature data array from 24 hours ago.
        

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

            12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            14) title_font_size (Integer) - The fontsize of the title of the figure. 

            15) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            16) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

            17) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                       Default setting is 0.05.
                                       Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                       Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

            18) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to temperature (degrees Fahrenheit)
    
    '''

    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate

    data = data
    try:
        if data == None:
            test = True
    except Exception as a:
        test = False
    time = time
        
    local_time, utc_time = standard.plot_creation_time()

    if test == True and time == None:
        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Temperature_Analysis_height_above_ground')

            rtma_df = rtma_data.to_dataframe()

            plot_proj = rtma_data.metpy.cartopy_crs

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds, ds_24, rtma_time, rtma_time_24 = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_24_hour_comparison_datasets(utc_time)
            
            temp = ds['tmp2m']
            temp_24 = ds_24['tmp2m']

            lat = ds['lat']
            lon = ds['lon']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']

            rtma_data = temp[0, :, :] - temp_24[0, :, :]
            NOMADS = True
            print("Unpacked the data successfully!")

    elif test == False and time != None:
        try:
            rtma_data = data
            rtma_time = time
            
            rtma_df = rtma_data.to_dataframe()

            plot_proj = rtma_data.metpy.cartopy_crs

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Temperature_Analysis_height_above_ground')
    
                rtma_df = rtma_data.to_dataframe()
    
                plot_proj = rtma_data.metpy.cartopy_crs
    
                NOMADS = False
                print("Unpacked the data successfully!")
    
            except Exception as e:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds, ds_24, rtma_time, rtma_time_24 = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_24_hour_comparison_datasets(utc_time)
                
                temp = ds['tmp2m']
                temp_24 = ds_24['tmp2m']
    
                lat = ds['lat']
                lon = ds['lon']
                lat_24 = ds_24['lat']
                lon_24 = ds_24['lon']
    
                rtma_data = temp[0, :, :] - temp_24[0, :, :]
                NOMADS = True
                print("Unpacked the data successfully!")                    

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")
    
    rtma_time_24 = rtma_time - timedelta(hours=24)

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    rtma_time_24_utc = rtma_time_24.astimezone(from_zone)

    rtma_data = calc.unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(rtma_data)

    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    if NOMADS == False:
        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
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

        cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-25, 26, 1), cmap='seismic', alpha=alpha, extend='both', zorder=2)

        if show_sample_points == True:

            stn = mpplots.StationPlot(ax, rtma_df['longitude'][::decimate], rtma_df['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn.plot_parameter('C', rtma_df['Temperature_Analysis_height_above_ground'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass


        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Temperature Change (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA 24-Hour Temperature Change (\N{DEGREE SIGN}F)\nAnalysis Start: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_24_utc.strftime('%H:00 UTC')+ ")\nAnalysis End:" + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    if NOMADS == True:

        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=datacrs)
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

        cs = ax.contourf(lon, lat, rtma_data, 
                         transform=datacrs, levels=np.arange(-25, 26, 1), cmap='seismic', alpha=alpha, extend='both', zorder=2)


        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Temperature Change (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA 24-Hour Temperature Change (\N{DEGREE SIGN}F)\nAnalysis Start: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_24_utc.strftime('%H:00 UTC')+ ")\nAnalysis End:" + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_24_hour_wind_speed_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, colorblind=False, decimate='default', data=None, time=None):

    r'''
        This function does the following:
                                        1) Downloads the wind speed data arrays for the current time and the data arrays for 24 hours ago from the data arrays for the current time.
                                        2) Converts wind speed values from m/s to MPH. 
                                        3) Subtracts the wind speed data array from 24 hours ago from the wind speed data array of the current time (Current Wind Speed - Wind Speed from 24 hours ago).
                                        4) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis of the difference between the current wind speed data array from the wind speed data array from 24 hours ago.
        

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

            12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            14) title_font_size (Integer) - The fontsize of the title of the figure. 

            15) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            16) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

            17) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                       Default setting is 0.05.
                                       Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                       Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

            18) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
    
    '''


    local_time, utc_time = standard.plot_creation_time()

    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate

    colorblind = colorblind
    data = data
    try:
        if data == None:
            test = True
    except Exception as a:
        test = False
    time = time

    if test == True and time == None:
        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Wind_speed_Analysis_height_above_ground')

            rtma_df = rtma_data.to_dataframe()
            plot_proj = rtma_data.metpy.cartopy_crs

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds, ds_24, rtma_time, rtma_time_24 = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_24_hour_comparison_datasets(utc_time)

            ws = ds['wind10m']
            ws_24 = ds_24['wind10m']

            lat = ds['lat']
            lon = ds['lon']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']

            rtma_data = ws[0, :, :] - ws_24[0, :, :]
            
            NOMADS = True
            print("Unpacked the data successfully!")

    elif test == False and time != None:
        try:
            rtma_data = data
            rtma_time = time

            rtma_df = rtma_data.to_dataframe()
            plot_proj = rtma_data.metpy.cartopy_crs

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Wind_speed_Analysis_height_above_ground')
    
                rtma_df = rtma_data.to_dataframe()
                plot_proj = rtma_data.metpy.cartopy_crs
    
                NOMADS = False
                print("Unpacked the data successfully!")
    
            except Exception as e:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds, ds_24, rtma_time, rtma_time_24 = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_24_hour_comparison_datasets(utc_time)
    
                ws = ds['wind10m']
                ws_24 = ds_24['wind10m']
    
                lat = ds['lat']
                lon = ds['lon']
                lat_24 = ds_24['lat']
                lon_24 = ds_24['lon']
    
                rtma_data = ws[0, :, :] - ws_24[0, :, :]
                
                NOMADS = True
                print("Unpacked the data successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    rtma_time_24 = rtma_time - timedelta(hours=24)

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    rtma_time_24_utc = rtma_time_24.astimezone(from_zone)

    rtma_data = rtma_data * 2.23694
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    if colorblind == False:
        cmap = colormaps.wind_speed_change_colormap()
    if colorblind == True:
        cmap = colormaps.colorblind_mode_divergent_colormap()

    if NOMADS == False:
        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
        ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        else:
            pass
        if show_gacc_borders == True:
            ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=2)
        else:
            pass
        if show_psa_borders == True:
            ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=2)
        else:
            pass
        if show_county_borders == True:
            ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=2)
        else:
            pass
        if show_state_borders == True:
            ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=2)
        else:
            pass

        cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-20, 21, 1), cmap=cmap, alpha=alpha, extend='both')

        if show_sample_points == True:

            stn = mpplots.StationPlot(ax, rtma_df['longitude'][::decimate], rtma_df['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn.plot_parameter('C', rtma_df['Wind_speed_Analysis_height_above_ground'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass

        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Wind Speed Change (MPH)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA 24-Hour Wind Speed Change (MPH)\nAnalysis Start: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_24_utc.strftime('%H:00 UTC')+ ")\nAnalysis End:" + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    if NOMADS == True:

        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=datacrs)
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

        cs = ax.contourf(lon, lat, rtma_data, 
                         transform=datacrs, levels=np.arange(-20, 21, 1), cmap=cmap, alpha=alpha, extend='both')

        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Wind Speed Change (MPH)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA 24-Hour Wind Speed Change (MPH)\nAnalysis Start: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_24_utc.strftime('%H:00 UTC')+ ")\nAnalysis End:" + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_24_hour_wind_speed_and_direction_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, barbs_or_quivers='barbs', first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.6, colorbar_label_font_size=7, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, shaded_alpha=0.5, barb_quiver_alpha=1, minshaft=0.000005, headlength=10, headwidth=15, colorblind=False, barb_quiver_fontsize=8, data=None):

    r'''
        This function does the following:
                                        1) Downloads the wind speed data arrays for the current time and the data arrays for 24 hours ago from the data arrays for the current time.
                                        2) Converts wind speed values from m/s to MPH. 
                                        3) Subtracts the wind speed data array from 24 hours ago from the wind speed data array of the current time (Current Wind Speed - Wind Speed from 24 hours ago).
                                        4) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis of the difference between the current wind speed data array from the wind speed data array from 24 hours ago.
        

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

            12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            14) title_font_size (Integer) - The fontsize of the title of the figure. 

            15) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            16) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

            17) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                       Default setting is 0.05.
                                       Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                       Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

            18) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
    
    '''


    local_time, utc_time = standard.plot_creation_time()
    shaded_alpha = shaded_alpha
    barb_quiver_alpha = barb_quiver_alpha
    barbs_or_quivers = barbs_or_quivers
    western_bound = western_bound
    eastern_bound = eastern_bound
    southern_bound = southern_bound
    northern_bound = northern_bound
    minshaft = minshaft 
    headlength = headlength 
    headwidth = headwidth
    colorblind = colorblind
    data = data
    
    if barbs_or_quivers == 'barbs' or barbs_or_quivers == 'Barbs' or barbs_or_quivers == 'BARBS' or barbs_or_quivers == 'B' or barbs_or_quivers == 'b':
        
        barbs = True

    if barbs_or_quivers == 'quivers' or barbs_or_quivers == 'Quivers' or barbs_or_quivers == 'QUIVERS' or barbs_or_quivers == 'Q' or barbs_or_quivers == 'q':

        barbs = False
    
    nomads_decimate = calc.scaling.get_nomads_decimation(western_bound, eastern_bound, southern_bound, northern_bound, barbs)

    thredds_decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, barbs)

    if data == None:
        try:
            ds = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_24_hour_comparison_data_with_u_and_v_components(utc_time)

            rtma_data = ds[0]
            rtma_time = ds[1]
            rtma_time_24 = ds[2]
            u = ds[3]
            u_time = ds[4]
            u_24 = ds[5]
            u_24_time = ds[6]
            v = ds[7]
            v_time = ds[8]
            v_24 = ds[9]
            v_24_time = ds[10]

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds, ds_24, rtma_time, rtma_time_24 = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_24_hour_comparison_datasets(utc_time)

            u = ds['ugrd10m']
            v = ds['vgrd10m']
            u_24 = ds_24['ugrd10m']
            v_24 = ds_24['vgrd10m']
            ws = ds['wind10m']
            ws_24 = ds_24['wind10m']
            rtma_data = ws[0, :, :] - ws_24[0, :, :]
            lon = ds['lon']
            lat = ds['lat']
            lon_24 = ds_24['lon']
            lat_24 = ds_24['lat']
            lon_2d, lat_2d = np.meshgrid(lon, lat)
            lon_24_2d, lat_24_2d = np.meshgrid(lon_24, lat_24)

            NOMADS = True
            print("Unpacked the data successfully!")

    elif data != None:
        try:
            rtma_data = data[0]
            rtma_time = data[1]
            rtma_time_24 = data[2]
            u = data[3]
            u_time = data[4]
            u_24 = data[5]
            u_24_time = data[6]
            v = data[7]
            v_time = data[8]
            v_24 = data[9]
            v_24_time = data[10]

            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")

                ds = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_24_hour_comparison_data_with_u_and_v_components(utc_time)
    
                rtma_data = ds[0]
                rtma_time = ds[1]
                rtma_time_24 = ds[2]
                u = ds[3]
                u_time = ds[4]
                u_24 = ds[5]
                u_24_time = ds[6]
                v = ds[7]
                v_time = ds[8]
                v_24 = ds[9]
                v_24_time = ds[10]
    
                NOMADS = False
                print("Unpacked the data successfully!")
    
            except Exception as e:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds, ds_24, rtma_time, rtma_time_24 = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_24_hour_comparison_datasets(utc_time)
    
                u = ds['ugrd10m']
                v = ds['vgrd10m']
                u_24 = ds_24['ugrd10m']
                v_24 = ds_24['vgrd10m']
                ws = ds['wind10m']
                ws_24 = ds_24['wind10m']
                rtma_data = ws[0, :, :] - ws_24[0, :, :]
                lon = ds['lon']
                lat = ds['lat']
                lon_24 = ds_24['lon']
                lat_24 = ds_24['lat']
                lon_2d, lat_2d = np.meshgrid(lon, lat)
                lon_24_2d, lat_24_2d = np.meshgrid(lon_24, lat_24)
    
                NOMADS = True
                print("Unpacked the data successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    u = u * 2.23694
    v = v * 2.23694
    u_24 = u_24 * 2.23694
    v_24 = v_24 * 2.23694

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    rtma_time_24_utc = rtma_time_24.astimezone(from_zone)

    rtma_data = rtma_data * 2.23694
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
    if colorblind == False:
        cmap = colormaps.wind_speed_change_colormap()
    if colorblind == True:
        cmap = colormaps.colorblind_mode_divergent_colormap()

    if NOMADS == False:

        df_u = u.to_dataframe()
        df_u24 = u_24.to_dataframe()
        df_v = v.to_dataframe()
        df_v24 = v_24.to_dataframe()

        df_u['wind'] = df_u['u-component_of_wind_Analysis_height_above_ground'] 
        df_v['wind'] = df_v['v-component_of_wind_Analysis_height_above_ground'] 
        df_u24['wind'] = df_u24['u-component_of_wind_Analysis_height_above_ground'] 
        df_v24['wind'] = df_v24['v-component_of_wind_Analysis_height_above_ground'] 

        plot_proj = rtma_data.metpy.cartopy_crs

        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
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

        cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-20, 21, 1), cmap=cmap, alpha=shaded_alpha, extend='both')

        if barbs_or_quivers == 'barbs' or barbs_or_quivers == 'Barbs' or barbs_or_quivers == 'BARBS' or barbs_or_quivers == 'B' or barbs_or_quivers == 'b':

            stn = mpplots.StationPlot(ax, df_u['longitude'][::thredds_decimate], df_u['latitude'][::thredds_decimate],
                                             transform=ccrs.PlateCarree(), zorder=5, fontsize=barb_quiver_fontsize, clip_on=True)
            stn1 = mpplots.StationPlot(ax, df_u24['longitude'][::thredds_decimate], df_u24['latitude'][::thredds_decimate],
                                             transform=ccrs.PlateCarree(), zorder=5, fontsize=barb_quiver_fontsize, clip_on=True)
            if colorblind == False:
                stn.plot_barb(df_u['u-component_of_wind_Analysis_height_above_ground'][::thredds_decimate], df_v['v-component_of_wind_Analysis_height_above_ground'][::thredds_decimate], color='black', label=rtma_time.strftime('%m/%d %H:00'), alpha=barb_quiver_alpha, zorder=5)
    
                stn1.plot_barb(df_u24['u-component_of_wind_Analysis_height_above_ground'][::thredds_decimate], df_v24['v-component_of_wind_Analysis_height_above_ground'][::thredds_decimate], color='blue', label=rtma_time_24.strftime('%m/%d %H:00'), alpha=barb_quiver_alpha, zorder=5)

            if colorblind == True:

                stn.plot_barb(df_u['u-component_of_wind_Analysis_height_above_ground'][::thredds_decimate], df_v['v-component_of_wind_Analysis_height_above_ground'][::thredds_decimate], color='crimson', label=rtma_time.strftime('%m/%d %H:00'), alpha=barb_quiver_alpha, zorder=5)
    
                stn1.plot_barb(df_u24['u-component_of_wind_Analysis_height_above_ground'][::thredds_decimate], df_v24['v-component_of_wind_Analysis_height_above_ground'][::thredds_decimate], color='dodgerblue', label=rtma_time_24.strftime('%m/%d %H:00'), alpha=barb_quiver_alpha, zorder=5)

        if barbs_or_quivers == 'quivers' or barbs_or_quivers == 'Quivers' or barbs_or_quivers == 'QUIVERS' or barbs_or_quivers == 'Q' or barbs_or_quivers == 'q':

            if colorblind == False:
            
                ax.quiver(df_u['longitude'][::thredds_decimate], df_u['latitude'][::thredds_decimate], df_u['wind'][::thredds_decimate], df_v['wind'][::thredds_decimate], color='black', minshaft=minshaft, headlength=headlength, headwidth=headwidth, alpha=barb_quiver_alpha, label=rtma_time.strftime('%m/%d %H:00'), zorder=5, transform=ccrs.PlateCarree())

                ax.quiver(df_u24['longitude'][::thredds_decimate], df_u24['latitude'][::thredds_decimate], df_u24['wind'][::thredds_decimate], df_v24['wind'][::thredds_decimate], color='blue', minshaft=minshaft, headlength=headlength, headwidth=headwidth, alpha=barb_quiver_alpha, label=rtma_time_24.strftime('%m/%d %H:00'), zorder=5, transform=ccrs.PlateCarree())

            if colorblind == True:

                ax.quiver(df_u['longitude'][::thredds_decimate], df_u['latitude'][::thredds_decimate], df_u['wind'][::thredds_decimate], df_v['wind'][::thredds_decimate], color='crimson', minshaft=minshaft, headlength=headlength, headwidth=headwidth, alpha=barb_quiver_alpha, label=rtma_time.strftime('%m/%d %H:00'), zorder=5, transform=ccrs.PlateCarree())

                ax.quiver(df_u24['longitude'][::thredds_decimate], df_u24['latitude'][::thredds_decimate], df_u24['wind'][::thredds_decimate], df_v24['wind'][::thredds_decimate], color='dodgerblue', minshaft=minshaft, headlength=headlength, headwidth=headwidth, alpha=barb_quiver_alpha, label=rtma_time_24.strftime('%m/%d %H:00'), zorder=5, transform=ccrs.PlateCarree())

        
        ax.legend(loc=(1, 0.9))
        
        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Wind Speed Change (MPH)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA 24-Hour Wind Speed & Direction Change (MPH)\nAnalysis Start: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_24_utc.strftime('%H:00 UTC')+ ")\nAnalysis End:" + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    if NOMADS == True:
        
        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=datacrs)
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

        cs = ax.contourf(lon, lat, rtma_data, 
                         transform=datacrs, levels=np.arange(-20, 21, 1), cmap=cmap, alpha=shaded_alpha, extend='both')

        if barbs_or_quivers == 'barbs' or barbs_or_quivers == 'Barbs' or barbs_or_quivers == 'BARBS' or barbs_or_quivers == 'B' or barbs_or_quivers == 'b':

            stn = mpplots.StationPlot(ax, lon_2d[::nomads_decimate, ::nomads_decimate], lat_2d[::nomads_decimate, ::nomads_decimate],
                             transform=ccrs.PlateCarree(), zorder=5, fontsize=barb_quiver_fontsize, clip_on=True)
            
            stn1 = mpplots.StationPlot(ax, lon_24_2d[::nomads_decimate, ::nomads_decimate], lat_24_2d[::nomads_decimate, ::nomads_decimate],
                             transform=ccrs.PlateCarree(), zorder=5, fontsize=barb_quiver_fontsize, clip_on=True)
            
            if colorblind == False:
                stn.plot_barb(u[0, :, :][::nomads_decimate, ::nomads_decimate], v[0, :, :][::nomads_decimate, ::nomads_decimate], color='black', label=rtma_time.strftime('%m/%d %H:00'), alpha=barb_quiver_alpha, zorder=5)
    
                stn1.plot_barb(u_24[0, :, :][::nomads_decimate, ::nomads_decimate], v_24[0, :, :][::nomads_decimate, ::nomads_decimate], color='blue', label=rtma_time_24.strftime('%m/%d %H:00'), alpha=barb_quiver_alpha, zorder=5)

            if colorblind == True:

                stn.plot_barb(u[0, :, :][::nomads_decimate, ::nomads_decimate], v[0, :, :][::nomads_decimate, ::nomads_decimate], color='crimson', label=rtma_time.strftime('%m/%d %H:00'), alpha=barb_quiver_alpha, zorder=5)
    
                stn1.plot_barb(u_24[0, :, :][::nomads_decimate, ::nomads_decimate], v_24[0, :, :][::nomads_decimate, ::nomads_decimate], color='dodgerblue', label=rtma_time_24.strftime('%m/%d %H:00'), alpha=barb_quiver_alpha, zorder=5)

        if barbs_or_quivers == 'quivers' or barbs_or_quivers == 'Quivers' or barbs_or_quivers == 'QUIVERS' or barbs_or_quivers == 'Q' or barbs_or_quivers == 'q':

            if colorblind == False:
            
                ax.quiver(lon_2d[::nomads_decimate, ::nomads_decimate], lat_2d[::nomads_decimate, ::nomads_decimate], u[0, :, :][::nomads_decimate, ::nomads_decimate], v[0, :, :][::nomads_decimate, ::nomads_decimate], color='black', minshaft=minshaft, headlength=headlength, headwidth=headwidth, alpha=barb_quiver_alpha, label=rtma_time.strftime('%m/%d %H:00'), zorder=5, transform=ccrs.PlateCarree())

                ax.quiver(lon_24_2d[::nomads_decimate, ::nomads_decimate], lat_24_2d[::nomads_decimate, ::nomads_decimate], u_24[0, :, :][::nomads_decimate, ::nomads_decimate], v_24[0, :, :][::nomads_decimate, ::nomads_decimate], color='blue', minshaft=minshaft, headlength=headlength, headwidth=headwidth, alpha=barb_quiver_alpha, label=rtma_time_24.strftime('%m/%d %H:00'), zorder=5, transform=ccrs.PlateCarree())

            if colorblind == True:

                ax.quiver(lon_2d[::nomads_decimate, ::nomads_decimate], lat_2d[::nomads_decimate, ::nomads_decimate], u[0, :, :][::nomads_decimate, ::nomads_decimate], v[0, :, :][::nomads_decimate, ::nomads_decimate], color='crimson', minshaft=minshaft, headlength=headlength, headwidth=headwidth, alpha=barb_quiver_alpha, label=rtma_time.strftime('%m/%d %H:00'), zorder=5, transform=ccrs.PlateCarree())

                ax.quiver(lon_24_2d[::nomads_decimate, ::nomads_decimate], lat_24_2d[::nomads_decimate, ::nomads_decimate], u_24[0, :, :][::nomads_decimate, ::nomads_decimate], v_24[0, :, :][::nomads_decimate, ::nomads_decimate], color='dodgerblue', minshaft=minshaft, headlength=headlength, headwidth=headwidth, alpha=barb_quiver_alpha, label=rtma_time_24.strftime('%m/%d %H:00'), zorder=5, transform=ccrs.PlateCarree())

        
        ax.legend(loc=(1, 0.9))
        
        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Wind Speed Change (MPH)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA 24-Hour Wind Speed & Direction Change (MPH)\nAnalysis Start: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_24_utc.strftime('%H:00 UTC')+ ")\nAnalysis End:" + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_24_hour_total_cloud_cover_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, colorblind=False, decimate='default', data=None, time=None):

    r'''
        This function does the following:
                                        1) Downloads the temperature data arrays for the current time and the data arrays for 24 hours ago from the data arrays for the current time.
                                        2) Converts the temperature values from Kelvin to Fahrenheit. 
                                        3) Subtracts the temperature data array from 24 hours ago from the temperature data array of the current time (Current Temperature - Temperature from 24 hours ago).
                                        4) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis of the difference between the current temperature data array from the temperature data array from 24 hours ago.
        

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

            12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            14) title_font_size (Integer) - The fontsize of the title of the figure. 

            15) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            16) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

            17) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                       Default setting is 0.05.
                                       Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                       Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

            18) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to temperature (degrees Fahrenheit)
    
    '''

    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate
        
    local_time, utc_time = standard.plot_creation_time()

    data = data
    try:
        if data == None:
            test = True
    except Exception as a:
        test = False
    time = time

    if test == True and time == None:
        
        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Total_cloud_cover_Analysis_entire_atmosphere_single_layer')

            rtma_df = rtma_data.to_dataframe()
            plot_proj = rtma_data.metpy.cartopy_crs
            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds, ds_24, rtma_time, rtma_time_24 = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_24_hour_comparison_datasets(utc_time)

            cloud = ds['tcdcclm']
            cloud_24 = ds_24['tcdcclm']

            lat = ds['lat']
            lon = ds['lon']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']

            rtma_data = cloud[0, :, :] - cloud_24[0, :, :]
            
            NOMADS = True
            print("Unpacked the data successfully!")

    elif test == False and time != None:
        try:
            rtma_data = data
            rtma_time = time
            rtma_df = rtma_data.to_dataframe()
            plot_proj = rtma_data.metpy.cartopy_crs
            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Total_cloud_cover_Analysis_entire_atmosphere_single_layer')
    
                rtma_df = rtma_data.to_dataframe()
                plot_proj = rtma_data.metpy.cartopy_crs
                NOMADS = False
                print("Unpacked the data successfully!")
    
            except Exception as e:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds, ds_24, rtma_time, rtma_time_24 = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_24_hour_comparison_datasets(utc_time)
    
                cloud = ds['tcdcclm']
                cloud_24 = ds_24['tcdcclm']
    
                lat = ds['lat']
                lon = ds['lon']
                lat_24 = ds_24['lat']
                lon_24 = ds_24['lon']
    
                rtma_data = cloud[0, :, :] - cloud_24[0, :, :]
                
                NOMADS = True
                print("Unpacked the data successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    rtma_time_24 = rtma_time - timedelta(hours=24)

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    rtma_time_24_utc = rtma_time_24.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
    cmap = colormaps.cloud_cover_change_colormap()

    if NOMADS == False:
        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
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

        cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-50, 51, 1), cmap=cmap, alpha=alpha, extend='both', zorder=2)

        if show_sample_points == True:

            stn = mpplots.StationPlot(ax, rtma_df['longitude'][::decimate], rtma_df['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn.plot_parameter('C', rtma_df['Total_cloud_cover_Analysis_entire_atmosphere_single_layer'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass


        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Total Cloud Cover Change (%)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA 24-Hour Total Cloud Cover Change\nAnalysis Start: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_24_utc.strftime('%H:00 UTC')+ ")\nAnalysis End:" + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    if NOMADS == True:
        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=datacrs)
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

        cs = ax.contourf(lon, lat, rtma_data, 
                         transform=datacrs, levels=np.arange(-50, 51, 1), cmap=cmap, alpha=alpha, extend='both', zorder=2)


        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Total Cloud Cover Change (%)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA 24-Hour Total Cloud Cover Change\nAnalysis Start: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_24_utc.strftime('%H:00 UTC')+ ")\nAnalysis End:" + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_current_frost_freeze_areas(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, decimate='default', data=None, time=None):

    r'''
        This function does the following:
                                        1) Downloads the latest available temperature data array.
                                        2) Converts temperature from Kelvin to Fahrenheit
                                        3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis of temperature filtered to only areas where T <= 32F. 
        

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

            12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            14) title_font_size (Integer) - The fontsize of the title of the figure. 

            15) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            16) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

            17) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                       Default setting is 0.05.
                                       Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                       Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

            18) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis of temperature filtered to only areas where T <= 32F. 
    
    '''

    if decimate == 'default':
        decimate = calc.scaling.get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, None)
    else:
        decimate = decimate

    local_time, utc_time = standard.plot_creation_time()
    data = data
    try:
        if data == None:
            test = True
    except Exception as a:
        test = False
    time = time

    if test == True and time == None:

        try:
            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Temperature_Analysis_height_above_ground')
            rtma_data = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
    
            rtma_df = rtma_data.to_dataframe(name='f')
    
            plot_proj = rtma_data.metpy.cartopy_crs
    
            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as e:
            print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
            ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']

            rtma_data = temp[0, :, :]
            rtma_data = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)

            lat = ds['lat']
            lon = ds['lon']
            
            NOMADS = True
            print("Unpacked the data successfully!")

    elif test == False and time != None:
        try:
            rtma_data = data
            rtma_time = time
            
            rtma_data = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
    
            rtma_df = rtma_data.to_dataframe(name='f')
    
            plot_proj = rtma_data.metpy.cartopy_crs
    
            NOMADS = False
            print("Unpacked the data successfully!")

        except Exception as f:
            try:
                print("Unable to unpack the data. Downloading the data again...")
                rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Temperature_Analysis_height_above_ground')
                rtma_data = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
        
                rtma_df = rtma_data.to_dataframe(name='f')
        
                plot_proj = rtma_data.metpy.cartopy_crs
        
                NOMADS = False
                print("Unpacked the data successfully!")
    
            except Exception as e:
                print("UCAR THREDDS Server is having issues. Now trying data access from NCEP NOMADS Server.")
                ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
    
                rtma_data = temp[0, :, :]
                rtma_data = calc.unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
    
                lat = ds['lat']
                lon = ds['lon']
                
                NOMADS = True
                print("Unpacked the data successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    cmap = colormaps.cool_temperatures_colormap()

    if NOMADS == False:

        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
        ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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

        cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                         transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-10, 33, 1), cmap=cmap, alpha=alpha, extend='min')

        if show_sample_points == True:

            stn = mpplots.StationPlot(ax, rtma_df['longitude'][::decimate], rtma_df['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn.plot_parameter('C', rtma_df['f'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        else:
            pass


        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\n   Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC') + ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC')+")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    if NOMADS == True:

        fig = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig.set_facecolor('aliceblue')

        ax = fig.add_subplot(1, 1, 1, projection=datacrs)
        ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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

        cs = ax.contourf(lon, lat, rtma_data, 
                         transform=datacrs, levels=np.arange(-10, 33, 1), cmap=cmap, alpha=alpha, extend='min')


        cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')


        plt.title("RTMA Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\n   Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC') + ")", fontsize=title_font_size, fontweight='bold')
        
        ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC')+")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_dry_and_windy_areas_based_on_sustained_winds(low_relative_humidity_threshold, high_wind_speed_threshold, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', alpha=0.5, data=None, time=None):

    r'''
        This function does the following:
                                        1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                        2) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                        3) Converts the wind speed data array from m/s to MPH. 
                                        4) decimates all areas where the following criteria is not met: RH <= red_flag_warning_relative_humidity_threshold (%) and Wind Speed >= red_flag_warning_wind_speed_threshold (MPH). 
                                        5) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Dry and Windy" criteria are met. 
        

        Inputs:

            1) low_relative_humidity_threshold (Integer) - The National Weather Service Red Flag Warning threshold for relative humidity. 
            
            2) high_wind_speed_threshold (Integer) - The National Weather Service Red Flag Warning threshold for wind speed. 

            3) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.

            4) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.

            5) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.

            6) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.

            7) central_longitude (Integer or Float) - The central longitude. Defaults to -96.

            8) central_latitude (Integer or Float) - The central latitude. Defaults to 39.

            9) first_standard_parallel (Integer or Float) - Southern standard parallel. 

            10) second_standard_parallel (Integer or Float) - Northern standard parallel. 

            11) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

            12) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

            13) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            14) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            15) title_font_size (Integer) - The fontsize of the title of the figure. 

            16) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            17) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of dry and windy conditions. 
    
    '''

    data = data
    time = time

    local_time, utc_time = standard.plot_creation_time()

    cmap = colormaps.red_flag_warning_criteria_colormap()

    low_relative_humidity_threshold = low_relative_humidity_threshold

    high_wind_speed_threshold = high_wind_speed_threshold

    if data == None and time == None:
        ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
        temp = ds['tmp2m']
        dwpt = ds['dpt2m']
        temp = temp - 273.15
        dwpt = dwpt - 273.15
        rtma_wind = ds['wind10m']
        rtma_wind = rtma_wind * 2.23694
        rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)

        rtma_rh = rtma_rh[0, :, :]
        rtma_wind = rtma_wind[0, :, :] 

    elif data != None and time != None:
        try:
            ds = data
            rtma_time = time
            
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['wind10m']
            rtma_wind = rtma_wind * 2.23694
            rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :]

            print ("Unpacked the data successfully!")
        except Exception as e:
            print("Unable to unpack the data. Downloading the data again!")

            ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['wind10m']
            rtma_wind = rtma_wind * 2.23694
            rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :] 

            print("Data retrieved and unpacked successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    mask = (rtma_rh <= low_relative_humidity_threshold) & (rtma_wind >= high_wind_speed_threshold)
    lon = mask['lon']
    lat = mask['lat']
    
    plot_proj = ccrs.PlateCarree()


    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
    ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
    if show_rivers == True:
        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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

    # Plot the mask
    try:
        ax.pcolormesh(lon,lat,mask,transform=ccrs.PlateCarree(),cmap=cmap, zorder=2, alpha=alpha)

    except Exception as e:
        pass
        

    plt.title("RTMA Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(low_relative_humidity_threshold) + "% & Wind Speed >= " + str(high_wind_speed_threshold) + " MPH\nAnalysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC')+")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_dry_and_windy_areas_based_on_wind_gusts(low_relative_humidity_threshold, high_wind_gust_threshold, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, first_standard_parallel=30, second_standard_parallel=60, title_font_size=12, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=8, colorbar_pad=0.02, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', alpha=0.5, data=None, time=None):

    r'''
        This function does the following:
                                        1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                        2) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                        3) Converts the wind gust data array from m/s to MPH. 
                                        4) decimates all areas where the following criteria is not met: RH <= red_flag_warning_relative_humidity_threshold (%) and Wind Gust >= red_flag_warning_wind_gust_threshold (MPH). 
                                        5) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Dry and Windy" criteria are met. 
        

        Inputs:

            1) red_flag_warning_relative_humidity_threshold (Integer) - The National Weather Service Red Flag Warning threshold for relative humidity. 
            
            2) red_flag_warning_wind_gust_threshold (Integer) - The National Weather Service Red Flag Warning threshold for wind speed using wind gusts. 

            3) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.

            4) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.

            5) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.

            6) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.

            7) central_longitude (Integer or Float) - The central longitude. Defaults to -96.

            8) central_latitude (Integer or Float) - The central latitude. Defaults to 39.

            9) first_standard_parallel (Integer or Float) - Southern standard parallel. 

            10) second_standard_parallel (Integer or Float) - Northern standard parallel. 

            11) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

            12) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

            13) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            14) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            15) title_font_size (Integer) - The fontsize of the title of the figure. 

            16) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            17) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of dry and windy conditions. 
    
    '''

    data = data
    time = time

    local_time, utc_time = standard.plot_creation_time()

    signature_x_position = signature_x_position
    signature_y_position = signature_y_position

    cmap = colormaps.red_flag_warning_criteria_colormap()

    low_relative_humidity_threshold = low_relative_humidity_threshold

    high_wind_gust_threshold = high_wind_gust_threshold
    
    if data == None and time == None:
        ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
        temp = ds['tmp2m']
        dwpt = ds['dpt2m']
        temp = temp - 273.15
        dwpt = dwpt - 273.15
        rtma_wind = ds['gust10m']
        rtma_wind = rtma_wind * 2.23694
        rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)

        rtma_rh = rtma_rh[0, :, :]
        rtma_wind = rtma_wind[0, :, :] 

    elif data != None and time != None:
        try:
            ds = data
            rtma_time = time
            
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['gust10m']
            rtma_wind = rtma_wind * 2.23694
            rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :]

            print ("Unpacked the data successfully!")
        except Exception as e:
            print("Unable to unpack the data. Downloading the data again!")

            ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['gust10m']
            rtma_wind = rtma_wind * 2.23694
            rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :] 

            print("Data retrieved and unpacked successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    mask = (rtma_rh <= low_relative_humidity_threshold) & (rtma_wind >= high_wind_gust_threshold)
    lon = mask['lon']
    lat = mask['lat']

    plot_proj = ccrs.PlateCarree()

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
    ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
    if show_rivers == True:
        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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

    # Plot the mask
    try:
        ax.pcolormesh(lon,lat,mask,transform=ccrs.PlateCarree(),cmap=cmap, zorder=2, alpha=alpha)

    except Exception as e:
        pass
        

    plt.title("RTMA Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(low_relative_humidity_threshold) + "% & Wind Gust >= " + str(high_wind_gust_threshold) + " MPH\nAnalysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC')+")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax.transAxes)

    return fig


def plot_dry_and_windy_areas_based_on_sustained_winds_3_panel(low_relative_humidity_threshold, high_wind_speed_threshold, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size=12, subplot_title_font_size=10, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=6, colorbar_pad=0.05, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', alpha=0.5, data=None, time=None):

    r'''
        This function does the following:
                                        1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                        2) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                        3) Converts the wind speed data array from m/s to MPH. 
                                        4) decimates all areas where the following criteria is not met: RH <= red_flag_warning_relative_humidity_threshold (%) and Wind Speed >= red_flag_warning_wind_speed_threshold (MPH). 
                                        5) Plots a figure that consists of 3 subplots.
                                        List of subplots:
                                                    1) Plot where the dry and windy conditions are located. 
                                                    2) Plot the relative humidity filtered only showing areas where the RH <= red_flag_warning_relative_humidity_threshold (%)
                                                    3) Plot the wind speed filtered only showing areas where Wind Speed >= red_flag_warning_wind_speed_threshold (MPH)
                                         
        

        Inputs:


            1) red_flag_warning_relative_humidity_threshold (Integer) - The National Weather Service Red Flag Warning threshold for relative humidity. 
            
            2) red_flag_warning_wind_speed_threshold (Integer) - The National Weather Service Red Flag Warning threshold for wind speed.

            3) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.

            4) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.

            5) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.

            6) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.

            7) central_longitude (Integer or Float) - The central longitude. Defaults to -96.

            8) central_latitude (Integer or Float) - The central latitude. Defaults to 39.

            9) first_standard_parallel (Integer or Float) - Southern standard parallel. 

            10) second_standard_parallel (Integer or Float) - Northern standard parallel. 

            11) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

            12) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

            13) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            14) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            15) title_font_size (Integer) - The fontsize of the title of the figure. 

            16) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            17) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

            18) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

            19) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
            
            20) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
            
            21) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.

            22) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                       Default setting is 0.05.
                                       Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                       Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

            23) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure showing the four aforementioned subplots:                                                             
                                                    1) Plot where the hot, dry and windy conditions are located. 
                                                    2) Plot the relative humidity filtered only showing areas where the RH <= red_flag_warning_relative_humidity_threshold (%)
                                                    3) Plot the wind speed filtered only showing areas where Wind Speed >= red_flag_warning_wind_speed_threshold (MPH)
    
    '''

    data = data
    time = time

    local_time, utc_time = standard.plot_creation_time()

    cmap_rfw = colormaps.red_flag_warning_criteria_colormap()
    cmap_rh = colormaps.low_relative_humidity_colormap()
    cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()

    low_relative_humidity_threshold = low_relative_humidity_threshold

    high_wind_speed_threshold = high_wind_speed_threshold


    if data == None and time == None:
        ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
        temp = ds['tmp2m']
        dwpt = ds['dpt2m']
        temp = temp - 273.15
        dwpt = dwpt - 273.15
        rtma_wind = ds['wind10m']
        rtma_wind = rtma_wind * 2.23694
        rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)

        rtma_rh = rtma_rh[0, :, :]
        rtma_wind = rtma_wind[0, :, :] 

    elif data != None and time != None:
        try:
            ds = data
            rtma_time = time
            
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['wind10m']
            rtma_wind = rtma_wind * 2.23694
            rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :]

            print ("Unpacked the data successfully!")
        except Exception as e:
            print("Unable to unpack the data. Downloading the data again!")

            ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['wind10m']
            rtma_wind = rtma_wind * 2.23694
            rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :] 

            print("Data retrieved and unpacked successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    mask = (rtma_rh <= low_relative_humidity_threshold) & (rtma_wind >= high_wind_speed_threshold)
    lon = mask['lon']
    lat = mask['lat']

    lons = ds['lon']
    lats = ds['lat']

    plot_proj_1 = ccrs.PlateCarree()
    plot_proj_2 = ccrs.PlateCarree()
    plot_proj_3 = ccrs.PlateCarree()

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')
    gs = gridspec.GridSpec(15, 15)
    ax0 = fig.add_subplot(gs[0:15, 0:14], projection=plot_proj_1)
    ax0.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax0.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax0.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
    ax0.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
    if show_rivers == True:
        ax0.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
    else:
        pass
    if show_gacc_borders == True:
        ax0.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
    else:
        pass
    if show_psa_borders == True:
        ax0.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
    else:
        pass
    if show_county_borders == True:
        ax0.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
    else:
        pass
    if show_state_borders == True:
        ax0.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
    else:
        pass

    ax0.set_title("Exceptionally Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')

    # Plot the decimate
    try:
        ax0.pcolormesh(lon,lat,mask, transform=ccrs.PlateCarree(),cmap=cmap_rfw, zorder=2, alpha=alpha)

    except Exception as e:
        pass


    ax1 = fig.add_subplot(gs[1:6, 10:15], projection=plot_proj_2)
    ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
    ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
    if show_rivers == True:
        ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
    else:
        pass
    ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, zorder=4)
    if show_gacc_borders == True:
        ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
    else:
        pass
    if show_psa_borders == True:
        ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
    else:
        pass
    if show_county_borders == True:
        ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
    else:
        pass
    if show_state_borders == True:
        ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
    else:
        pass

    cs_rh = ax1.contourf(lons, lats, rtma_rh, 
                     transform=plot_proj_2, levels=np.arange(0, low_relative_humidity_threshold + 1, 1), cmap=cmap_rh, alpha=alpha)

    cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='right', pad=colorbar_pad)
    cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')


    ax2 = fig.add_subplot(gs[9:14, 10:15], projection=plot_proj_3)
    ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
    ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
    if show_rivers == True:
        ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
    else:
        pass
    ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, zorder=4)
    if show_gacc_borders == True:
        ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
    else:
        pass
    if show_psa_borders == True:
        ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
    else:
        pass
    if show_county_borders == True:
        ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
    else:
        pass
    if show_state_borders == True:
        ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
    else:
        pass

    cs_wind = ax2.contourf(lons, lats, rtma_wind, 
                     transform=plot_proj_3, levels=np.arange(high_wind_speed_threshold, high_wind_speed_threshold + 55, 5), cmap=cmap_wind, alpha=alpha)

    cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='right', pad=colorbar_pad)
    cbar_wind.set_label(label="Sustained Wind Speed (MPH)", size=colorbar_label_font_size, fontweight='bold')   
    

    fig.suptitle("RTMA Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(low_relative_humidity_threshold) + "% & Sustained Wind Speed >= " + str(high_wind_speed_threshold) + " MPH\nAnalysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')

    ax0.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC')+")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
   verticalalignment='bottom', transform=ax0.transAxes)

    return fig        


def plot_dry_and_windy_areas_based_on_wind_gusts_3_panel(low_relative_humidity_threshold, high_wind_gust_threshold, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size=12, subplot_title_font_size=10, signature_font_size=10, color_table_shrink=0.7, colorbar_label_font_size=6, colorbar_pad=0.05, show_rivers=True, show_gacc_borders=False, show_psa_borders=False, show_county_borders=True, show_state_borders=True, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, gacc_border_linestyle='-', psa_border_linestyle='-', state_border_linestyle='-', county_border_linestyle='-', alpha=0.5, data=None, time=None):

    r'''
        This function does the following:
                                        1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                        2) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                        3) Converts the wind speed data array from m/s to MPH. 
                                        4) decimates all areas where the following criteria is not met: RH <= red_flag_warning_relative_humidity_threshold (%) and Wind Speed >= red_flag_warning_wind_speed_threshold (MPH). 
                                        5) Plots a figure that consists of 3 subplots.
                                        List of subplots:
                                                    1) Plot where the dry and windy conditions are located. 
                                                    2) Plot the relative humidity filtered only showing areas where the RH <= red_flag_warning_relative_humidity_threshold (%)
                                                    3) Plot the wind speed filtered only showing areas where Wind Speed >= red_flag_warning_wind_speed_threshold (MPH)
                                         
        

        Inputs:


            1) red_flag_warning_relative_humidity_threshold (Integer) - The National Weather Service Red Flag Warning threshold for relative humidity. 
            
            2) red_flag_warning_wind_speed_threshold (Integer) - The National Weather Service Red Flag Warning threshold for wind speed.

            3) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.

            4) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.

            5) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.

            6) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.

            7) central_longitude (Integer or Float) - The central longitude. Defaults to -96.

            8) central_latitude (Integer or Float) - The central latitude. Defaults to 39.

            9) first_standard_parallel (Integer or Float) - Southern standard parallel. 

            10) second_standard_parallel (Integer or Float) - Northern standard parallel. 

            11) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

            12) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

            13) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

            14) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

            15) title_font_size (Integer) - The fontsize of the title of the figure. 

            16) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            17) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

            18) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

            19) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
            
            20) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
            
            21) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.

            22) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                       Default setting is 0.05.
                                       Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                       Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

            23) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                        will not display on the map. 


        Returns:
                1) A figure showing the four aforementioned subplots:                                                             
                                                    1) Plot where the hot, dry and windy conditions are located. 
                                                    2) Plot the relative humidity filtered only showing areas where the RH <= red_flag_warning_relative_humidity_threshold (%)
                                                    3) Plot the wind speed filtered only showing areas where Wind Speed >= red_flag_warning_wind_speed_threshold (MPH)
    
    '''

    data = data
    time = time

    local_time, utc_time = standard.plot_creation_time()

    cmap_rfw = colormaps.red_flag_warning_criteria_colormap()
    cmap_rh = colormaps.low_relative_humidity_colormap()
    cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()

    low_relative_humidity_threshold = low_relative_humidity_threshold

    high_wind_gust_threshold = high_wind_gust_threshold

    if data == None and time == None:
        ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
        temp = ds['tmp2m']
        dwpt = ds['dpt2m']
        temp = temp - 273.15
        dwpt = dwpt - 273.15
        rtma_wind = ds['gust10m']
        rtma_wind = rtma_wind * 2.23694
        rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)

        rtma_rh = rtma_rh[0, :, :]
        rtma_wind = rtma_wind[0, :, :] 

    elif data != None and time != None:
        try:
            ds = data
            rtma_time = time
            
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['gust10m']
            rtma_wind = rtma_wind * 2.23694
            rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :]

            print ("Unpacked the data successfully!")
        except Exception as e:
            print("Unable to unpack the data. Downloading the data again!")

            ds, rtma_time = da.NOMADS_OPENDAP_Downloads.RTMA_CONUS.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['gust10m']
            rtma_wind = rtma_wind * 2.23694
            rtma_rh = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :] 

            print("Data retrieved and unpacked successfully!")

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")
    

    mask = (rtma_rh <= low_relative_humidity_threshold) & (rtma_wind >= high_wind_gust_threshold)
    lon = mask['lon']
    lat = mask['lat']

    lons = ds['lon']
    lats = ds['lat']

    plot_proj_1 = ccrs.PlateCarree()
    plot_proj_2 = ccrs.PlateCarree()
    plot_proj_3 = ccrs.PlateCarree()

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    datacrs = ccrs.PlateCarree()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')
    gs = gridspec.GridSpec(15, 15)
    ax0 = fig.add_subplot(gs[0:15, 0:14], projection=plot_proj_1)
    ax0.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax0.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax0.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
    ax0.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
    if show_rivers == True:
        ax0.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
    else:
        pass
    if show_gacc_borders == True:
        ax0.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
    else:
        pass
    if show_psa_borders == True:
        ax0.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
    else:
        pass
    if show_county_borders == True:
        ax0.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
    else:
        pass
    if show_state_borders == True:
        ax0.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
    else:
        pass

    ax0.set_title("Exceptionally Dry & Gusty Areas", fontsize=subplot_title_font_size, fontweight='bold')

    # Plot the decimate
    try:
        ax0.pcolormesh(lon,lat,mask, transform=ccrs.PlateCarree(),cmap=cmap_rfw, zorder=2, alpha=alpha)

    except Exception as e:
        pass


    ax1 = fig.add_subplot(gs[1:6, 10:15], projection=plot_proj_2)
    ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
    ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
    if show_rivers == True:
        ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
    else:
        pass
    ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, zorder=4)
    if show_gacc_borders == True:
        ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
    else:
        pass
    if show_psa_borders == True:
        ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
    else:
        pass
    if show_county_borders == True:
        ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
    else:
        pass
    if show_state_borders == True:
        ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
    else:
        pass

    cs_rh = ax1.contourf(lons, lats, rtma_rh, 
                     transform=plot_proj_2, levels=np.arange(0, low_relative_humidity_threshold + 1, 1), cmap=cmap_rh, alpha=alpha)

    cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='right', pad=colorbar_pad)
    cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')


    ax2 = fig.add_subplot(gs[9:14, 10:15], projection=plot_proj_3)
    ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
    ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
    ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
    if show_rivers == True:
        ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
    else:
        pass
    ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, zorder=4)
    if show_gacc_borders == True:
        ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
    else:
        pass
    if show_psa_borders == True:
        ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
    else:
        pass
    if show_county_borders == True:
        ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
    else:
        pass
    if show_state_borders == True:
        ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
    else:
        pass

    cs_wind = ax2.contourf(lons, lats, rtma_wind, 
                     transform=plot_proj_3, levels=np.arange(high_wind_gust_threshold, high_wind_gust_threshold + 55, 5), cmap=cmap_wind, alpha=alpha)

    cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='right', pad=colorbar_pad)
    cbar_wind.set_label(label="Wind Gust (MPH)", size=colorbar_label_font_size, fontweight='bold')   
    

    fig.suptitle("RTMA Exceptionally Dry & Gusty Areas (Shaded)\nRH <= " + str(low_relative_humidity_threshold) + "% & Wind Gusts >= " + str(high_wind_gust_threshold) + " MPH\nAnalysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+ ")", fontsize=title_font_size, fontweight='bold')

    ax0.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC')+")", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
   verticalalignment='bottom', transform=ax0.transAxes)

    return fig   

