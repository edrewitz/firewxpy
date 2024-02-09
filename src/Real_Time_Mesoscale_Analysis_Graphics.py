'''
This script hosts all the Real Time Mesoscale Analysis (RTMA) plotting functions in FireWxPy. 
The RTMA data consists of gridded data for current conditions with a grid spacing of 2.5km x 2.5km.

There are 3 primary classes which are used to define the perspective of the plot: 
1) Counties_Perspective - This class uses state and county borders as the geographical reference. 
2) Predictive_Services_Areas_Perspective - This class uses the Geographic Area Coordination Center (GACC) and Predictive Services Area (PSA) boundaries as the geographical reference. 
3) Islands - This class is seperate from the previous two due to the only boundaries being the coastline. 


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

from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from NWS_Generic_Forecast_Graphics import standard


class Counties_Perspective:


    r'''This class hosts a variety of plotting functions with two different domains: 1) Alaska and 2) CONUS. 

    The Counties_Perspective class uses county and state borders as the geographical reference. 



    (C) METEOROLOGIST ERIC J. DREWITZ 2024

    '''
    class Alaska:

        r'''
            The Alaska domain class is then divided into 6 nested classes sectioning out Alaska into 4 regions plus the 1 nested class that covers the entire state of Alaska. 

            Class names of the 6 different regional nested classes in the Alaska class:

                1) Entire_State: This class allows the user to view the entire state of Alaska. 
                   Latitude/Longitude Bounds: (West = 174W, East = 128W, South = 45N, North = 80N)

                2) South_Central: This class hosts the graphics for Southcentral Alaska. 
                   This includes: 1) Anchorage Bowl, 2) Kenai Peninsula, 3) Matanuska Valley, 4) Susitna Valley, 5) Copper River Basin and 6) Prince William Sound Area. 
                   Latitude/Longitude Bounds: (West = 155W, East = 140.75W, South = 58.75N, North = 64N)

                3) Southwest: This class hosts the graphics for Southwest Alaska. 
                   This includes the 1) Kuskokwim Valley, 2) Kuskokwim Delta and 3) Bristol Bay. 
                   Latitude/Longitude Bounds: (West = 168W, East = 153W, South = 55N, North = 64N)

                4) Southeast: This class hosts the graphics for Southeast Alaska. 
                   This includes 1) All the islands in the Alaska Panhandle, 2) Yakutat.
                   Latitude/Longitude Bounds: (West = 144.75W, East = 129.75W, South = 54.5N, North = 61N)

                5) Interior_And_Northslope: This class hosts the graphics for the Alaskan Interior and North Slope.
                   This includes: 1) North Slope, 2) Brooks Range, 3) Seward Peninsula, 4) Arctic National Wildlife Refuge (ANWR). 
                   Latitude/Longitude Bounds: (West = 169.5W, East = 140.75W, South = 63N, North = 75N)

                6) Kodiak: This class hosts the graphics for Kodiak Island. 
                   This includes all communities on Kodiak Island. 
                   Latitude/Longitude Bounds: (West = 156W, East = 150.75W, South = 56N, North = 59.1N)


        '''

        class Entire_State:

            r'''
            
            Entire_State: This class allows the user to view the entire state of Alaska. 
            Latitude/Longitude Bounds: (West = 174W, East = 128W, South = 45N, North = 80N)
            
            '''
            
            def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot. 

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                param = parameter
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, param)
    
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    data_to_plot = data_to_plot * 2.23694
    
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
                plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
            def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''

                This function does the following:
                                                1) Downloads the temperature and dewpoint data arrays.
                                                2) Uses MetPy to calculate the relative humidity from the temperature and dewpoint data arrays.
                                                3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for Relative Humidity (%).

                

                Inputs:

                    1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    5) title_font_size (Integer) - The fontsize of the title of the figure. 

                    6) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    8) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for Relative Humidity (%)
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                This function does the following:
                                                1) Downloads the temperature and dewpoint data arrays.
                                                2) Uses MetPy to calculate the relative humidity from the temperature and dewpoint data arrays.
                                                3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for Relative Humidity (%) filtering out any relative humidity values > 25% and < 80%.

                

                Inputs:

                    1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    5) title_font_size (Integer) - The fontsize of the title of the figure. 

                    6) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    8) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for Relative Humidity (%) only showing areas where the relative humidity is <= 25% and relative humidity >= 80%
                
                '''            
                local_time, utc_time = standard.plot_creation_time()

                colorbar_label_font_size = colorbar_label_font_size

                colorbar_pad = colorbar_pad
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap_high = colormaps.excellent_recovery_colormap()
                cmap_low = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap=cmap_low, transform=datacrs)
                cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
                cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap_high, transform=datacrs)
                cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=8, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                This function does the following:
                                                1) Downloads the temperature and dewpoint data arrays for the current time and the data arrays for 24 hours ago from the data arrays for the current time.
                                                2) Uses MetPy to calculate the relative humidity from the temperature and dewpoint data arrays for both times (current time and current time - 24 hours).
                                                3) Subtracts the relative humidity data array from 24 hours ago from the relative humidity data array of the current time (Current RH - RH from 24 hours ago).
                                                4) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis of the difference between the current relative humidity data array from the relative humidity data array from 24 hours ago.
                

                Inputs:

                    1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    5) title_font_size (Integer) - The fontsize of the title of the figure. 

                    6) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    8) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to relative humidity (%)
                
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                This function does the following:
                                                1) Downloads the temperature data array for the current time and the temperature data array for 24 hours ago from the data array for the current time.
                                                2) Converts the temperature values from Kelvin to Fahrenheit.
                                                3) Subtracts the temperature data array from 24 hours ago from the temperature data array of the current time (Current Temperature - Temperature from 24 hours ago).
                                                4) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis of the difference between the current temperature data array from the temperature data array from 24 hours ago.
                

                Inputs:

                    1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    5) title_font_size (Integer) - The fontsize of the title of the figure. 

                    6) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    8) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to temperature (degrees F)
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
                parameter = 'tmp2m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                This function does the following:
                                                1) Downloads the wind speed data array for the current time and the wind speed data array for 24 hours ago from the data array for the current time.
                                                2) Converts the wind speed values from m/s to MPH.
                                                3) Subtracts the wind speed data array from 24 hours ago from the wind speed data array of the current time (Current Wind Speed - Wind Speed from 24 hours ago).
                                                4) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis of the difference between the current wind speed data array from the wind speed data array from 24 hours ago.
                

                Inputs:

                    1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    5) title_font_size (Integer) - The fontsize of the title of the figure. 

                    6) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    8) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to temperature (degrees F)
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                parameter = 'wind10m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                This function does the following:
                                                1) Downloads the latest temperature data array.
                                                2) Converts the temperature values from Kelvin to Fahrenheit.
                                                3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the temperature is <= 32F.
                

                Inputs:

                    1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    5) title_font_size (Integer) - The fontsize of the title of the figure. 

                    6) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    8) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to temperature (degrees F)
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontsize=title_font_size, fontweight='bold')
                
                plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                This function does the following:
                                                1) Downloads the temperature and dewpoint data arrays for the current time and the temperature data array for 24 hours ago from the data array for the current time.
                                                2) Converts the temperature values from Kelvin to Fahrenheit.
                                                3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the temperature is <= 32F.
                

                Inputs:

                    1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    5) title_font_size (Integer) - The fontsize of the title of the figure. 

                    6) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    8) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to temperature (degrees F)
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap_rh = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-174, -128, 45, 80], datacrs)
    
    
                cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, location='right', pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
                plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-174, -128, 45, 80], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sutained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_wind_gusts(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-174, -128, 45, 80], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gust >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                gs = gridspec.GridSpec(15, 15)
                ax0 = plt.subplot(gs[0:8, 0:7], projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(1)
                ax0.set_extent([-174, -128, 45, 80], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(gs[0:8, 8:15], projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(1)
                ax1.set_extent([-174, -128, 45, 80], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(gs[8:15, 0:7], projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(1)
                ax2.set_extent([-174, -128, 45, 80], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(gs[8:15, 8:15], projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_aspect(1)
                ax3.set_extent([-174, -128, 45, 80], datacrs)
                ax3.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_wind.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sutained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax2.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                gs = gridspec.GridSpec(15, 15)
                ax0 = plt.subplot(gs[0:8, 0:7], projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(1)
                ax0.set_extent([-174, -128, 45, 80], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(gs[0:8, 8:15], projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(1)
                ax1.set_extent([-174, -128, 45, 80], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(gs[8:15, 0:7], projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(1)
                ax2.set_extent([-174, -128, 45, 80], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(gs[8:15, 8:15], projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_aspect(1)
                ax3.set_extent([-174, -128, 45, 80], datacrs)
                ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax2.transAxes) 
    
                return fig



        class South_Central:

            r'''
            THIS NESTED CLASS WILL ZOOM INTO SOUTHCENTRAL ALASKA

            '''



            def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot. 

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                param = parameter
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, param)
    
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    data_to_plot = data_to_plot * 2.23694
    
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
                plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
            def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()

                colorbar_label_font_size = colorbar_label_font_size

                colorbar_pad = colorbar_pad
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.excellent_recovery_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
                cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
                parameter = 'tmp2m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                parameter = 'wind10m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap_rh = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
    
    
                cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, ax=ax, location='right', pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
                plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig

            def plot_hot_dry_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_wind_gusts(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gust >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5, zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax3.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs, zorder=1)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sustained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig


        class Southwest:

            r'''
            THIS NESTED CLASS IS FOR SOUTHWEST ALASKA
            '''

            def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot. 

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                param = parameter
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, param)
    
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    data_to_plot = data_to_plot * 2.23694
    
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
                plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
            def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()

                colorbar_label_font_size = colorbar_label_font_size

                colorbar_pad = colorbar_pad
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.excellent_recovery_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
                cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=8, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
                parameter = 'tmp2m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                parameter = 'wind10m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap_rh = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-168, -153, 55, 64], datacrs)
    
    
                cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, location='right', pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
                plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-168, -153, 55, 64], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-168, -153, 55, 64], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-168, -153, 55, 64], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-168, -153, 55, 64], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5, zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-168, -153, 55, 64], datacrs)
                ax3.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs, zorder=1)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sustained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-168, -153, 55, 64], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-168, -153, 55, 64], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-168, -153, 55, 64], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-168, -153, 55, 64], datacrs)
                ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig


        class Southeast:

            r'''
            THIS NESTED CLASS IS FOR SOUTHWEST ALASKA
            '''

            def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot. 

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                param = parameter
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, param)
    
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    data_to_plot = data_to_plot * 2.23694
    
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
                plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
            def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()

                colorbar_label_font_size = colorbar_label_font_size

                colorbar_pad = colorbar_pad
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.excellent_recovery_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
                cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
                parameter = 'tmp2m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                parameter = 'wind10m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap_rh = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
    
    
                cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, location='right', pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
                plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5, zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax3.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs, zorder=1)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sustained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig


        class Interior_And_Northslope:

            r'''
            THIS NESTED CLASS IS FOR THE INTERIOR AND NORTHSLOPE OF ALASKA
            '''

            def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot. 

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                param = parameter
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, param)
    
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    data_to_plot = data_to_plot * 2.23694
    
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
                plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
            def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()

                colorbar_label_font_size = colorbar_label_font_size

                colorbar_pad = colorbar_pad
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.excellent_recovery_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
                cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
                parameter = 'tmp2m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                parameter = 'wind10m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap_rh = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
    
    
                cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, ax=ax, location='right', pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
                plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig

            def plot_hot_dry_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_sustained_winds_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5, zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax3.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs, zorder=1)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sustained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig



        class Kodiak:

            r'''
            THIS NESTED CLASS IS FOR KODIAK
            '''

            def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot. 

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                param = parameter
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, param)
    
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    data_to_plot = data_to_plot * 2.23694
    
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-156, -150.75, 56, 59.1], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
                plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
            def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-156, -150.75, 56, 59.1], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()

                colorbar_label_font_size = colorbar_label_font_size

                colorbar_pad = colorbar_pad
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.excellent_recovery_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-156, -150.75, 56, 59.1], datacrs)
                
                cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
                cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-156, -150.75, 56, 59.1], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
                parameter = 'tmp2m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-156, -150.75, 56, 59.1], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                parameter = 'wind10m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-156, -150.75, 56, 59.1], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-156, -150.75, 56, 59.1], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap_rh = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-156, -150.75, 56, 59.1], datacrs)
    
    
                cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, location='right', pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
                plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-156, -150.75, 56, 59.1], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-156, -150.75, 56, 59.1], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-156, -150.75, 56, 59.1], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-156, -150.75, 56, 59.1], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5, zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-156, -150.75, 56, 59.1], datacrs)
                ax3.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs, zorder=1)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sustained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-156, -150.75, 56, 59.1], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-156, -150.75, 56, 59.1], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-156, -150.75, 56, 59.1], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-156, -150.75, 56, 59.1], datacrs)
                ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig

    
    class CONUS:

        r'''
        THIS NESTED CLASS HOSTS THE IMAGES FOR CONUS AKA THE "LOWER-48"
        '''

        def plot_generic_real_time_mesoanalysis_no_METARs(parameter, plot_title, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, state_border_color, state_border_line_thickness, county_border_color, county_border_line_thickness, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot. For the full parameter list, visit: https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/NDFD/NWS/CONUS/CONDUIT/Best.html

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            param = parameter

            if param == 'Wind_speed_gust_Analysis_height_above_ground' or param == 'Wind_speed_Analysis_height_above_ground' or param == 'Wind_speed_error_height_above_ground' or param == 'Wind_speed_gust_error_height_above_ground' or param == 'u-component_of_wind_Analysis_height_above_ground' or param == 'v-component_of_wind_Analysis_height_above_ground':

                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                data = data * 2.23694

            if param == 'Temperature_Analysis_height_above_ground' or param == 'Dewpoint_temperature_Analysis_height_above_ground' or param == 'Temperature_error_height_above_ground' or param == 'Dewpoint_temperature_error_height_above_ground':
                
                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(data)
                

            else:
                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                
            plot_proj = data.metpy.cartopy_crs
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)

            cs = ax.contourf(data.metpy.x, data.metpy.y, data, 
                             transform=data.metpy.cartopy_crs, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')

            plt.title(plot_title + "\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_generic_real_time_mesoanalysis_with_METARs(parameter, plot_title, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, mask, state_border_color, state_border_line_thickness, county_border_color, county_border_line_thickness, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            param = parameter

            if param == 'Wind_speed_gust_Analysis_height_above_ground' or param == 'Wind_speed_Analysis_height_above_ground' or param == 'Wind_speed_error_height_above_ground' or param == 'Wind_speed_gust_error_height_above_ground' or param == 'u-component_of_wind_Analysis_height_above_ground' or param == 'v-component_of_wind_Analysis_height_above_ground':

               rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
               rtma_data = rtma_data * 2.23694

            if param == 'Temperature_Analysis_height_above_ground' or param == 'Dewpoint_temperature_Analysis_height_above_ground' or param == 'Temperature_error_height_above_ground' or param == 'Dewpoint_temperature_error_height_above_ground':
                
                rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
                rtma_data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
                

            else:
               rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
                
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='blue',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title(plot_title + "\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\n\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') +"\n\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig



        def plot_relative_humidity_with_METARs(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, mask, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, mask)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.relative_humidity_colormap()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=1)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='darkorange',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title("Real Time Mesoscale Analysis Relative Humidity\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nMETAR Observations Valid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig

        def plot_red_flag_relative_humidity_with_METARs(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, mask, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT FILTERS THE RELATIVE HUMIDITY DATASET TO ONLY PLOT WHERE THE RELATIVE HUMIDITY IS 15% OR LESS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, mask)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=1)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='darkorange',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title("Real Time Mesoscale Analysis Red-Flag Relative Humidity (RH <=15%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nMETAR Observations Valid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig
 

        def plot_low_and_high_relative_humidity(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT FILTERS THE RELATIVE HUMIDITY DATASET TO ONLY PLOT WHERE THE RELATIVE HUMIDITY IS 15% OR LESS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''
            colorbar_label_font_size = colorbar_label_font_size

            colorbar_pad = colorbar_pad

            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.excellent_recovery_colormap()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            cs_low = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=1)

            cs_high = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(80, 101, 1), cmap=cmap, alpha=1)

            cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_low.set_label(label="Low Relative Humidity (RH <= 15%)", size=colorbar_label_font_size, fontweight='bold')

            cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_high.set_label(label="High Relative Humidity (RH >= 80%)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_relative_humidity_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE RELATIVE HUMIDITY FROM THE CURRENT TIME AND THE RELATIVE HUMIDITY FROM 24 HOURS AGO AND PLOTS THE 24 HOUR RELATIVE HUMIDITY CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            
            cmap = colormaps.relative_humidity_change_colormap()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_relative_humidity_24_hour_difference_data(utc_time)

            rtma_time_24 = rtma_time - timedelta(hours=24)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-60, 65, 5), cmap=cmap, alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Relative Humidity Change (%)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("24-Hour Relative Humidity Change (%)\nValid: " + rtma_time_24.strftime('%m/%d/%Y %HZ') + " - " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_temperature_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE TEMPERATURE FROM THE CURRENT TIME AND THE TEMPERATURE FROM 24 HOURS AGO AND PLOTS THE 24 HOUR TEMPERATURE CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Temperature_Analysis_height_above_ground')

            rtma_time_24 = rtma_time - timedelta(hours=24)

            rtma_data = calc.unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(rtma_data)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='lime', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-20, 21, 1), cmap='seismic', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Temperature Change (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + rtma_time_24.strftime('%m/%d/%Y %HZ') + " - " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_wind_speed_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE WIND SPEED FROM THE CURRENT TIME AND THE WIND SPEED FROM 24 HOURS AGO AND PLOTS THE 24 HOUR WIND SPEED CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Wind_speed_Analysis_height_above_ground')

            rtma_time_24 = rtma_time - timedelta(hours=24)

            rtma_data = rtma_data * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-30, 31, 1), cmap='PuOr_r', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Wind Speed Change (MPH)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + rtma_time_24.strftime('%m/%d/%Y %HZ') + " - " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_current_frost_freeze_areas(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT SHOWS THE CURRENT AREAS EXPERIENCING BELOW FREEZING TEMPERATURES SINCE FROST/FREEZE CAN TURN LIVE FUEL INTO DEAD FUEL WHICH CAN ULTIMATELY LEAD TO MORE SUCCEPTABLE FUELS FOR WILDFIRE.

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Temperature_Analysis_height_above_ground')

            rtma_data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-10, 33, 1), cmap='cool_r', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_relative_humidity_overlayed_with_red_flag_wind_speed(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''
            colorbar_label_font_size = colorbar_label_font_size

            colorbar_pad = colorbar_pad

            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)

            rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Wind_speed_Analysis_height_above_ground')

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            cs_rh = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=0.5)

            cs_wind = ax.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 100, 5), cmap='BuPu', alpha=0.5)


            cbar_rh = fig.colorbar(cs_rh, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            cbar_wind = fig.colorbar(cs_wind, location='right', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_wind.set_label(label="Wind Speed (MPH)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("Red-Flag Warning Conditions (RH <= 15% and Wind Speed >= 25 MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_dry_and_windy_areas_based_on_sustained_winds(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_speed_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap = colormaps.red_flag_warning_criteria_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_speed_threshold = red_flag_warning_wind_speed_threshold

            rtma_rh, rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_red_flag_warning_parameters_using_wind_speed(utc_time)

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_wind >= red_flag_warning_wind_speed_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj = mask.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            # Plot the mask
            try:
                ax.pcolormesh(lon,lat,mask,transform=ccrs.PlateCarree(),cmap=cmap)

            except Exception as e:
                pass
                

            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Wind Speed >= " + str(red_flag_warning_wind_speed_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_dry_and_windy_areas_based_on_wind_gusts(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_gust_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON WIND GUSTS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap = colormaps.red_flag_warning_criteria_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_gust_threshold = red_flag_warning_wind_gust_threshold

            rtma_rh, rtma_gust, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_red_flag_warning_parameters_using_wind_gust(utc_time)

            rtma_gust = rtma_gust * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_gust >= red_flag_warning_wind_gust_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj = mask.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            # Plot the mask
            try:
                ax.pcolormesh(lon,lat,mask,transform=ccrs.PlateCarree(),cmap=cmap)

            except Exception as e:
                pass
                

            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Wind Gust >= " + str(red_flag_warning_wind_gust_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_dry_and_windy_areas_based_on_sustained_winds_3_panel(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_speed_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, plot_title_font_size, subplot_title_font_size, colorbar_shrink, colorbar_pad, colorbar_label_font_size, signature_x_position, signature_y_position, signature_font_size,  first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap_rfw = colormaps.red_flag_warning_criteria_colormap()
            cmap_rh = colormaps.low_relative_humidity_colormap()
            cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_speed_threshold = red_flag_warning_wind_speed_threshold

            rtma_rh, rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_red_flag_warning_parameters_using_wind_speed(utc_time)

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_wind >= red_flag_warning_wind_speed_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj_1 = mask.metpy.cartopy_crs
            plot_proj_2 = rtma_rh.metpy.cartopy_crs
            plot_proj_3 = rtma_wind.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax0 = fig.add_subplot(1, 3, 1, projection=plot_proj_1)
            ax0.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_aspect(first_subplot_aspect_ratio)
            ax0.set_title("Exceptionally Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')

            # Plot the mask
            try:
                ax0.pcolormesh(lon,lat,mask, transform=ccrs.PlateCarree(),cmap=cmap_rfw)

            except Exception as e:
                pass


            ax1 = fig.add_subplot(1, 3, 2, projection=plot_proj_2)
            ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_aspect(subsequent_subplot_aspect_ratio)
            ax1.set_title("Low Relative Humidity Areas", fontsize=subplot_title_font_size, fontweight='bold')

            cs_rh = ax1.contourf(rtma_rh.metpy.x, rtma_rh.metpy.y, rtma_rh, 
                             transform=rtma_rh.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap=cmap_rh, alpha=1)

            cbar_rh = fig.colorbar(cs_rh, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')


            ax2 = fig.add_subplot(1, 3, 3, projection=plot_proj_3)
            ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_aspect(subsequent_subplot_aspect_ratio)
            ax2.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

            cs_wind = ax2.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 75, 5), cmap=cmap_wind, alpha=1)

            cbar_wind = fig.colorbar(cs_wind, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_wind.set_label(label="Sustained Wind Speed (MPH)", size=colorbar_label_font_size, fontweight='bold')   
            

            fig.suptitle("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Sustained Wind Speed >= " + str(red_flag_warning_wind_speed_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=plot_title_font_size, fontweight='bold')
            
            ax0.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy\n(C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax0.transAxes)

            return fig        


        def plot_dry_and_windy_areas_based_on_wind_gusts_3_panel(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_gust_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, plot_title_font_size, subplot_title_font_size, colorbar_shrink, colorbar_pad, colorbar_label_font_size, signature_x_position, signature_y_position, signature_font_size,  first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap_rfw = colormaps.red_flag_warning_criteria_colormap()
            cmap_rh = colormaps.low_relative_humidity_colormap()
            cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_gust_threshold = red_flag_warning_wind_gust_threshold

            rtma_rh, rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_red_flag_warning_parameters_using_wind_gust(utc_time)

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_wind >= red_flag_warning_wind_gust_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj_1 = mask.metpy.cartopy_crs
            plot_proj_2 = rtma_rh.metpy.cartopy_crs
            plot_proj_3 = rtma_wind.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax0 = fig.add_subplot(1, 3, 1, projection=plot_proj_1)
            ax0.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_aspect(first_subplot_aspect_ratio)
            ax0.set_title("Exceptionally Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')

            # Plot the mask
            try:
                ax0.pcolormesh(lon,lat,mask, transform=ccrs.PlateCarree(),cmap=cmap_rfw)

            except Exception as e:
                pass


            ax1 = fig.add_subplot(1, 3, 2, projection=plot_proj_2)
            ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_aspect(subsequent_subplot_aspect_ratio)
            ax1.set_title("Low Relative Humidity Areas", fontsize=subplot_title_font_size, fontweight='bold')

            cs_rh = ax1.contourf(rtma_rh.metpy.x, rtma_rh.metpy.y, rtma_rh, 
                             transform=rtma_rh.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap=cmap_rh, alpha=1)

            cbar_rh = fig.colorbar(cs_rh, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')


            ax2 = fig.add_subplot(1, 3, 3, projection=plot_proj_3)
            ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_aspect(subsequent_subplot_aspect_ratio)
            ax2.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

            cs_wind = ax2.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 75, 5), cmap=cmap_wind, alpha=1)

            cbar_wind = fig.colorbar(cs_wind, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_wind.set_label(label="Wind Gust (MPH)", size=colorbar_label_font_size, fontweight='bold')   
            

            fig.suptitle("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Wind Gust >= " + str(red_flag_warning_wind_gust_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=plot_title_font_size, fontweight='bold')
            
            ax0.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy\n(C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax0.transAxes)

            return fig     


        def plot_red_flag_relative_humidity_overlayed_with_red_flag_wind_gusts(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON WIND GUSTS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''
            colorbar_label_font_size = colorbar_label_font_size

            local_time, utc_time = standard.plot_creation_time()

            colorbar_pad = colorbar_pad

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)

            rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Wind_speed_gust_Analysis_height_above_ground')

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            cs_rh = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=0.5)

            cs_wind = ax.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 100, 5), cmap='BuPu', alpha=0.5)


            cbar_rh = fig.colorbar(cs_rh, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            cbar_wind = fig.colorbar(cs_wind, location='right', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_wind.set_label(label="Wind Gust (MPH)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("Red-Flag Warning Conditions (RH <= 15% and Wind Gust >= 25 MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


class Predictive_Services_Areas_Perspective:


    r'''

    THIS CLASS HOSTS PLOTTING FUNCTIONS TO PLOT THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA

    THE IMAGES IN THIS CLASS OVERLAY A PREDICTIVE SERVICES AREAS PERSPECTIVE AS THE REFERENCE FOR THE PLOTS

    (C) METEOROLOGIST ERIC J. DREWITZ 2024

    '''


    class Alaska:

        class Entire_State:

            r'''
             THIS NESTED CLASS HOSTS THE IMAGES FOR THE ENTIRE STATE OF ALASKA
            '''
            
            def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad, PSA_Border_Color, GACC_Border_Color):
    
                r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot.

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                param = parameter
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, param)
    
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    data_to_plot = data_to_plot * 2.23694
    
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", PSA_Border_Color)

                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", GACC_Border_Color)
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
                plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
            def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()

                colorbar_label_font_size = colorbar_label_font_size

                colorbar_pad = colorbar_pad
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.excellent_recovery_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
                cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=8, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
                parameter = 'tmp2m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'lime')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                parameter = 'wind10m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-174, -128, 45, 80], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontsize=title_font_size, fontweight='bold')
                
                plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap_rh = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-174, -128, 45, 80], datacrs)
    
    
                cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, location='right', pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
                plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-174, -128, 45, 80], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sutained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_wind_gusts(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-174, -128, 45, 80], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gust >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                gs = gridspec.GridSpec(15, 15)
                ax0 = plt.subplot(gs[0:8, 0:7], projection=datacrs)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.set_aspect(1)
                ax0.set_extent([-174, -128, 45, 80], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(gs[0:8, 8:15], projection=datacrs)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.set_aspect(1)
                ax1.set_extent([-174, -128, 45, 80], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(gs[8:15, 0:7], projection=datacrs)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.set_aspect(1)
                ax2.set_extent([-174, -128, 45, 80], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(gs[8:15, 8:15], projection=datacrs)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.set_aspect(1)
                ax3.set_extent([-174, -128, 45, 80], datacrs)
                ax3.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_wind.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sutained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax2.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                gs = gridspec.GridSpec(15, 15)
                ax0 = plt.subplot(gs[0:8, 0:7], projection=datacrs)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.set_aspect(1)
                ax0.set_extent([-174, -128, 45, 80], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(gs[0:8, 8:15], projection=datacrs)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.set_aspect(1)
                ax1.set_extent([-174, -128, 45, 80], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(gs[8:15, 0:7], projection=datacrs)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.set_aspect(1)
                ax2.set_extent([-174, -128, 45, 80], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(gs[8:15, 8:15], projection=datacrs)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.set_aspect(1)
                ax3.set_extent([-174, -128, 45, 80], datacrs)
                ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=0.02)
                cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax2.transAxes) 
    
                return fig



        class South_Central:

            r'''
            THIS NESTED CLASS WILL ZOOM INTO SOUTHCENTRAL ALASKA

            '''



            def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad, PSA_Border_Color, GACC_Border_Color):
    
                r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot. 

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                param = parameter
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, param)
    
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    data_to_plot = data_to_plot * 2.23694
    
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", PSA_Border_Color)
    
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", GACC_Border_Color)
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
                plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
            def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()

                colorbar_label_font_size = colorbar_label_font_size

                colorbar_pad = colorbar_pad
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.excellent_recovery_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
                cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
                parameter = 'tmp2m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'lime')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                parameter = 'wind10m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap_rh = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
    
    
                cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, ax=ax, location='right', pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
                plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig

            def plot_hot_dry_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_wind_gusts(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-155, -140.75, 58.75, 64], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gust >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax3.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs, zorder=1)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sustained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-155, -140.75, 58.75, 64], datacrs)
                ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig


        class Southwest:

            r'''
            THIS NESTED CLASS IS FOR SOUTHWEST ALASKA
            '''

            def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad, PSA_Border_Color, GACC_Border_Color):
    
                r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot. 

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                param = parameter
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, param)
    
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    data_to_plot = data_to_plot * 2.23694
    
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", PSA_Border_Color)
    
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", GACC_Border_Color)
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
                plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
            def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()

                colorbar_label_font_size = colorbar_label_font_size

                colorbar_pad = colorbar_pad
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.excellent_recovery_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
                cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=8, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
                parameter = 'tmp2m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'lime')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                parameter = 'wind10m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-168, -153, 55, 64], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap_rh = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-168, -153, 55, 64], datacrs)
    
    
                cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, location='right', pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
                plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-168, -153, 55, 64], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-168, -153, 55, 64], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-168, -153, 55, 64], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-168, -153, 55, 64], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-168, -153, 55, 64], datacrs)
                ax3.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs, zorder=1)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sustained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-168, -153, 55, 64], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-168, -153, 55, 64], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-168, -153, 55, 64], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-168, -153, 55, 64], datacrs)
                ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig


        class Southeast:

            r'''
            THIS NESTED CLASS IS FOR SOUTHWEST ALASKA
            '''

            def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad, PSA_Border_Color, GACC_Border_Color):
    
                r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot.

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                param = parameter
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, param)
    
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    data_to_plot = data_to_plot * 2.23694
    
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", PSA_Border_Color)
    
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", GACC_Border_Color)
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
                plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
            def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()

                colorbar_label_font_size = colorbar_label_font_size

                colorbar_pad = colorbar_pad
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.excellent_recovery_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
                cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
                parameter = 'tmp2m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'lime')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                parameter = 'wind10m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap_rh = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
    
    
                cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, location='right', pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
                plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig


            def plot_hot_dry_windy_areas_based_on_sustained_winds_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax3.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs, zorder=1)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sustained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
                ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig


        class Interior_And_Northslope:

            r'''
            THIS NESTED CLASS IS FOR THE INTERIOR AND NORTHSLOPE OF ALASKA
            '''

            def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad, PSA_Border_Color, GACC_Border_Color):
    
                r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot. 

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                param = parameter
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, param)
    
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    data_to_plot = data_to_plot * 2.23694
    
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", PSA_Border_Color)
    
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", GACC_Border_Color)
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
                plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
            def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()

                colorbar_label_font_size = colorbar_label_font_size

                colorbar_pad = colorbar_pad
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.excellent_recovery_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
                cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
                cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                cmap = colormaps.relative_humidity_change_colormap()
                parameter = 'tmp2m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'lime')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
                parameter = 'wind10m'
    
                lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
                
                cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
                cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
                plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig
    
    
            def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
                r'''
                THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_relative_humidity(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap_rh = colormaps.low_relative_humidity_colormap()
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
    
    
                cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink, ax=ax, location='right', pad=colorbar_pad)
                cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
                plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig

            def plot_hot_dry_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
    
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax = plt.subplot(1,1,1, projection=datacrs)
                ax.add_feature(GACC, linewidth=2.5, zorder=3)
                ax.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
    
                try:
                    ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass
    
                
                plt.title("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_sustained_winds_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_speed >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax3.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs, zorder=1)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Sustained Wind Speed >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig



            def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
    
                r'''
                THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
                (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
                '''            
                local_time, utc_time = standard.plot_creation_time()
    
                lon_vals, lat_vals, time, relative_humidity, temperature, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Alaska.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
                mapcrs = ccrs.Mercator(central_longitude=-150, min_latitude=50, max_latitude=75.0, globe=None)
                datacrs = ccrs.PlateCarree()

                PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
                GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
                cmap = colormaps.red_flag_warning_criteria_colormap()
                cmap_rh = colormaps.low_relative_humidity_colormap()
                cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()
                cmap_temperature = colormaps.red_flag_warning_alaska_temperature_parameter_colormap()

                mask = (temperature >= 75) & (relative_humidity <= 25) & (wind_gust >= 15)
                lon = mask['lon']
                lat = mask['lat']
                
                fig = plt.figure(figsize=(fig_x_length,fig_y_length))
                ax0 = plt.subplot(4,1,1, projection=datacrs)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.set_aspect(first_subplot_aspect_ratio)
                ax0.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
                try:
                    ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
                except Exception as e:
                    pass


                ax1 = plt.subplot(4,1,2, projection=datacrs)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.set_aspect(subsequent_subplot_aspect_ratio)
                ax1.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')

                cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
                cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 

                ax2 = plt.subplot(4,1,3, projection=datacrs)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.set_aspect(subsequent_subplot_aspect_ratio)
                ax2.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')

                cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
                cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 


                ax3 = plt.subplot(4,1,4, projection=datacrs)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.set_aspect(subsequent_subplot_aspect_ratio)
                ax3.set_extent([-169.5, -140.75, 63, 75], datacrs)
                ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

                cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
                cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
                cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
    
                
                fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
                ax3.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax3.transAxes) 
    
                return fig

    
    class CONUS:

        r'''
        THIS NESTED CLASS HOSTS THE IMAGES FOR CONUS AKA THE "LOWER-48"
        '''


        def plot_generic_real_time_mesoanalysis_no_METARs(parameter, plot_title, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, GACC_Border_Color, GACC_Border_Line_Thickness, PSA_Border_Line_Thickness, PSA_Border_Color, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot. For the full parameter list, visit: https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/NDFD/NWS/CONUS/CONDUIT/Best.html

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            param = parameter

            if param == 'Wind_speed_gust_Analysis_height_above_ground' or param == 'Wind_speed_Analysis_height_above_ground' or param == 'Wind_speed_error_height_above_ground' or param == 'Wind_speed_gust_error_height_above_ground' or param == 'u-component_of_wind_Analysis_height_above_ground' or param == 'v-component_of_wind_Analysis_height_above_ground':

                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                data = data * 2.23694

            if param == 'Temperature_Analysis_height_above_ground' or param == 'Dewpoint_temperature_Analysis_height_above_ground' or param == 'Temperature_error_height_above_ground' or param == 'Dewpoint_temperature_error_height_above_ground':
                
                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(data)
                

            else:
                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                
            plot_proj = data.metpy.cartopy_crs
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", PSA_Border_Color)

            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", GACC_Border_Color)

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=GACC_Border_Line_Thickness, zorder=3)
            ax.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness, zorder=2)

            cs = ax.contourf(data.metpy.x, data.metpy.y, data, 
                             transform=data.metpy.cartopy_crs, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')

            plt.title(plot_title + "\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_generic_real_time_mesoanalysis_with_METARs(parameter, plot_title, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, mask, GACC_Border_Color, GACC_Border_Line_Thickness, PSA_Border_Line_Thickness, PSA_Border_Color, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            param = parameter

            if param == 'Wind_speed_gust_Analysis_height_above_ground' or param == 'Wind_speed_Analysis_height_above_ground' or param == 'Wind_speed_error_height_above_ground' or param == 'Wind_speed_gust_error_height_above_ground' or param == 'u-component_of_wind_Analysis_height_above_ground' or param == 'v-component_of_wind_Analysis_height_above_ground':

               rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
               rtma_data = rtma_data * 2.23694

            if param == 'Temperature_Analysis_height_above_ground' or param == 'Dewpoint_temperature_Analysis_height_above_ground' or param == 'Temperature_error_height_above_ground' or param == 'Dewpoint_temperature_error_height_above_ground':
                
                rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
                rtma_data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
                

            else:
               rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
                
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", PSA_Border_Color)
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", GACC_Border_Color)

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=GACC_Border_Line_Thickness, zorder=3)
            ax.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='blue',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title(plot_title + "\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\n\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') +"\n\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig



        def plot_relative_humidity_with_METARs(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, mask, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, mask)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

            cmap = colormaps.relative_humidity_colormap()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='darkorange',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title("Real Time Mesoscale Analysis Relative Humidity\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nMETAR Observations Valid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_relative_humidity_with_METARs(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, mask, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT FILTERS THE RELATIVE HUMIDITY DATASET TO ONLY PLOT WHERE THE RELATIVE HUMIDITY IS 15% OR LESS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, mask)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=1)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='darkorange',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title("Real Time Mesoscale Analysis Red-Flag Relative Humidity (RH <=15%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nMETAR Observations Valid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_low_and_high_relative_humidity(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT FILTERS THE RELATIVE HUMIDITY DATASET TO ONLY PLOT WHERE THE RELATIVE HUMIDITY IS 15% OR LESS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            colorbar_label_font_size = colorbar_label_font_size

            colorbar_pad = colorbar_pad
            
            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.excellent_recovery_colormap()

            plot_proj = rtma_data.metpy.cartopy_crs

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)

            cs_low = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=1)

            cs_high = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(80, 101, 1), cmap=cmap, alpha=1)

            cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_low.set_label(label="Low Relative Humidity (RH <= 15%)", size=colorbar_label_font_size, fontweight='bold')

            cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_high.set_label(label="High Relative Humidity (RH >= 80%)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_relative_humidity_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE RELATIVE HUMIDITY FROM THE CURRENT TIME AND THE RELATIVE HUMIDITY FROM 24 HOURS AGO AND PLOTS THE 24 HOUR RELATIVE HUMIDITY CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_relative_humidity_24_hour_difference_data(utc_time)

            rtma_time_24 = rtma_time - timedelta(hours=24)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
            cmap = colormaps.relative_humidity_change_colormap()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-60, 65, 5), cmap=cmap, alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Relative Humidity Change (%)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("24-Hour Relative Humidity Change (%)\nValid: " + rtma_time_24.strftime('%m/%d/%Y %HZ') + " - " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_temperature_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE TEMPERATURE FROM THE CURRENT TIME AND THE TEMPERATURE FROM 24 HOURS AGO AND PLOTS THE 24 HOUR TEMPERATURE CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Temperature_Analysis_height_above_ground')

            rtma_time_24 = rtma_time - timedelta(hours=24)

            rtma_data = calc.unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(rtma_data)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'lime')

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-20, 21, 1), cmap='seismic', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Temperature Change (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + rtma_time_24.strftime('%m/%d/%Y %HZ') + " - " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_wind_speed_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE WIND SPEED FROM THE CURRENT TIME AND THE WIND SPEED FROM 24 HOURS AGO AND PLOTS THE 24 HOUR WIND SPEED CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Wind_speed_Analysis_height_above_ground')

            rtma_time_24 = rtma_time - timedelta(hours=24)

            rtma_data = rtma_data * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-30, 31, 1), cmap='PuOr_r', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Wind Speed Change (MPH)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + rtma_time_24.strftime('%m/%d/%Y %HZ') + " - " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig
            

        def plot_current_frost_freeze_areas(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT SHOWS THE CURRENT AREAS EXPERIENCING BELOW FREEZING TEMPERATURES SINCE FROST/FREEZE CAN TURN LIVE FUEL INTO DEAD FUEL WHICH CAN ULTIMATELY LEAD TO MORE SUCCEPTABLE FUELS FOR WILDFIRE.

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Temperature_Analysis_height_above_ground')

            rtma_data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'red')

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-10, 33, 1), cmap='cool_r', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_relative_humidity_overlayed_with_red_flag_wind_speed(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            colorbar_label_font_size = colorbar_label_font_size

            colorbar_pad = colorbar_pad
            
            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)

            rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Wind_speed_Analysis_height_above_ground')

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)

            cs_rh = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=0.5)

            cs_wind = ax.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 100, 5), cmap='BuPu', alpha=0.5)


            cbar_rh = fig.colorbar(cs_rh, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            cbar_wind = fig.colorbar(cs_wind, location='right', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_wind.set_label(label="Wind Speed (MPH)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("Red-Flag Warning Conditions (RH <= 15% and Wind Speed >= 25 MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_relative_humidity_overlayed_with_red_flag_wind_gusts(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON WIND GUSTS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''
            colorbar_label_font_size = colorbar_label_font_size

            colorbar_pad = colorbar_pad

            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)

            rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Wind_speed_gust_Analysis_height_above_ground')

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)

            cs_rh = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=0.5)

            cs_wind = ax.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 100, 5), cmap='BuPu', alpha=0.5)


            cbar_rh = fig.colorbar(cs_rh, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            cbar_wind = fig.colorbar(cs_wind, location='right', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_wind.set_label(label="Wind Gust (MPH)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("Red-Flag Warning Conditions (RH <= 15% and Wind Gust >= 25 MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_dry_and_windy_areas_based_on_sustained_winds(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_speed_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap = colormaps.red_flag_warning_criteria_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_speed_threshold = red_flag_warning_wind_speed_threshold

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

            rtma_rh, rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_red_flag_warning_parameters_using_wind_speed(utc_time)

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_wind >= red_flag_warning_wind_speed_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj = mask.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)

            # Plot the mask
            try:
                ax.pcolormesh(lon,lat,mask,transform=ccrs.PlateCarree(),cmap=cmap)

            except Exception as e:
                pass
                

            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Wind Speed >= " + str(red_flag_warning_wind_speed_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_dry_and_windy_areas_based_on_wind_gusts(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_gust_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON WIND GUSTS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap = colormaps.red_flag_warning_criteria_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_gust_threshold = red_flag_warning_wind_gust_threshold

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

            rtma_rh, rtma_gust, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_red_flag_warning_parameters_using_wind_gust(utc_time)

            rtma_gust = rtma_gust * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_gust >= red_flag_warning_wind_gust_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj = mask.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)

            # Plot the mask
            try:
                ax.pcolormesh(lon,lat,mask,transform=ccrs.PlateCarree(),cmap=cmap)

            except Exception as e:
                pass
                

            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Wind Gust >= " + str(red_flag_warning_wind_gust_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_dry_and_windy_areas_based_on_sustained_winds_3_panel(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_speed_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, plot_title_font_size, subplot_title_font_size, colorbar_shrink, colorbar_pad, colorbar_label_font_size, signature_x_position, signature_y_position, signature_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap_rfw = colormaps.red_flag_warning_criteria_colormap()
            cmap_rh = colormaps.low_relative_humidity_colormap()
            cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_speed_threshold = red_flag_warning_wind_speed_threshold

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

            rtma_rh, rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_red_flag_warning_parameters_using_wind_speed(utc_time)

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_wind >= red_flag_warning_wind_speed_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj_1 = mask.metpy.cartopy_crs
            plot_proj_2 = rtma_rh.metpy.cartopy_crs
            plot_proj_3 = rtma_wind.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax0 = fig.add_subplot(1, 3, 1, projection=plot_proj_1)
            ax0.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax0.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.set_aspect(first_subplot_aspect_ratio)
            ax0.set_title("Exceptionally Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')

            # Plot the mask
            try:
                ax0.pcolormesh(lon,lat,mask, transform=ccrs.PlateCarree(),cmap=cmap_rfw)

            except Exception as e:
                pass


            ax1 = fig.add_subplot(1, 3, 2, projection=plot_proj_2)
            ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax1.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.set_aspect(subsequent_subplot_aspect_ratio)
            ax1.set_title("Low Relative Humidity Areas", fontsize=subplot_title_font_size, fontweight='bold')

            cs_rh = ax1.contourf(rtma_rh.metpy.x, rtma_rh.metpy.y, rtma_rh, 
                             transform=rtma_rh.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap=cmap_rh, alpha=1)

            cbar_rh = fig.colorbar(cs_rh, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')


            ax2 = fig.add_subplot(1, 3, 3, projection=plot_proj_3)
            ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax2.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.set_aspect(subsequent_subplot_aspect_ratio)
            ax2.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

            cs_wind = ax2.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 75, 5), cmap=cmap_wind, alpha=1)

            cbar_wind = fig.colorbar(cs_wind, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_wind.set_label(label="Sustained Wind Speed (MPH)", size=colorbar_label_font_size, fontweight='bold')   
            

            fig.suptitle("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Sustained Wind Speed >= " + str(red_flag_warning_wind_speed_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=plot_title_font_size, fontweight='bold')
            
            ax0.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy\n(C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax0.transAxes)

            return fig 


        def plot_dry_and_windy_areas_based_on_wind_gusts_3_panel(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_gust_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, plot_title_font_size, subplot_title_font_size, colorbar_shrink, colorbar_pad, colorbar_label_font_size, signature_x_position, signature_y_position, signature_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap_rfw = colormaps.red_flag_warning_criteria_colormap()
            cmap_rh = colormaps.low_relative_humidity_colormap()
            cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_gust_threshold = red_flag_warning_wind_gust_threshold

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

            rtma_rh, rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_red_flag_warning_parameters_using_wind_gust(utc_time)

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_wind >= red_flag_warning_wind_gust_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj_1 = mask.metpy.cartopy_crs
            plot_proj_2 = rtma_rh.metpy.cartopy_crs
            plot_proj_3 = rtma_wind.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax0 = fig.add_subplot(1, 3, 1, projection=plot_proj_1)
            ax0.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax0.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.set_aspect(first_subplot_aspect_ratio)
            ax0.set_title("Exceptionally Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')

            # Plot the mask
            try:
                ax0.pcolormesh(lon,lat,mask, transform=ccrs.PlateCarree(),cmap=cmap_rfw)

            except Exception as e:
                pass


            ax1 = fig.add_subplot(1, 3, 2, projection=plot_proj_2)
            ax1.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax1.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.set_aspect(subsequent_subplot_aspect_ratio)
            ax1.set_title("Low Relative Humidity Areas", fontsize=subplot_title_font_size, fontweight='bold')

            cs_rh = ax1.contourf(rtma_rh.metpy.x, rtma_rh.metpy.y, rtma_rh, 
                             transform=rtma_rh.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap=cmap_rh, alpha=1)

            cbar_rh = fig.colorbar(cs_rh, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')


            ax2 = fig.add_subplot(1, 3, 3, projection=plot_proj_3)
            ax2.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax2.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.set_aspect(subsequent_subplot_aspect_ratio)
            ax2.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

            cs_wind = ax2.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 75, 5), cmap=cmap_wind, alpha=1)

            cbar_wind = fig.colorbar(cs_wind, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_wind.set_label(label="Wind Gust (MPH)", size=colorbar_label_font_size, fontweight='bold')   
            

            fig.suptitle("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Wind Gust >= " + str(red_flag_warning_wind_gust_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=plot_title_font_size, fontweight='bold')
            
            ax0.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy\n(C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax0.transAxes)

            return fig

class Islands:

    r'''
    THIS CLASS HOSTS THE IMAGES FOR HAWAII, PUERTO RICO AND GUAM. SINCE EACH ISLAND IS ITS OWN PSA, THERE IS NO DIFFERENCE BETWEEN A COUNTY AND A PSA PERSPECTIVE FOR THESE AREAS, HENCE IT WILL BE ITS OWN CLASS IN ITS ENTIRETY SEPERATE FROM THE COUNTY AND PSA PERSPECTIVES
    '''

    class Hawaii:

        r'''
        THIS NESTED CLASS IS FOR THE GRAPHICS FOR HAWAII
        '''

        def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot.

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
            param = parameter
    
            lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_Data_single_parameter(utc_time, param)
    
            if param == 'tmp2m' or param == 'dpt2m':
                frac = 9/5
                data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
            if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                data_to_plot = data_to_plot * 2.23694
    
                
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
            plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
        def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
    
            lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_relative_humidity(utc_time)
                
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            cmap = colormaps.relative_humidity_colormap()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig

        def plot_red_flag_relative_humidity_with_METARs(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF HAWAII. THIS PLOT FILTERS THE RELATIVE HUMIDITY DATASET TO ONLY PLOT WHERE THE RELATIVE HUMIDITY IS 15% OR LESS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            lon_vals, lat_vals, rtma_time, relative_humidity_to_plot, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time_revised = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR_Hawaii(utc_time)
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.low_relative_humidity_colormap()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=datacrs)
            ax.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)

            cs = ax.contourf(lon_vals, lat_vals, relative_humidity_to_plot, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'].m, sfc_data['latitude'].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF'), color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF'), color='darkorange',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent'), color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'], sfc_data['v'])

            plt.title("Real Time Mesoscale Analysis Red-Flag Relative Humidity (RH <=15%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nMETAR Observations Valid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig
    
    
        def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF HAWAII. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()

            colorbar_label_font_size = colorbar_label_font_size

            colorbar_pad = colorbar_pad
    
            lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_relative_humidity(utc_time)
                
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()

            cmap_low = colormaps.low_relative_humidity_colormap()
            cmap_high = colormaps.excellent_recovery_colormap()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
                
            cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 61, 1), cmap=cmap_low, transform=datacrs)
            cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
            cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(90, 101, 1), cmap=cmap_high, transform=datacrs)
            cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
    
        def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
            cmap = colormaps.relative_humidity_change_colormap()
    
            lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 61, 1), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
    
        def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF HAWAII. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
            cmap = colormaps.relative_humidity_change_colormap()
            parameter = 'tmp2m'
    
            lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
    
        def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
            parameter = 'wind10m'
    
            lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
    
        def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
    
            lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
    
        def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
    
            lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_relative_humidity(utc_time)  
    
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            cmap_rh = colormaps.low_relative_humidity_colormap()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
    
    
            cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 46, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, location='right', pad=colorbar_pad)
            cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
            plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 45%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig


        def plot_dry_and_windy_areas_based_on_sustained_winds(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
            r'''
            THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
    
            lon_vals, lat_vals, time, relative_humidity, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            cmap = colormaps.red_flag_warning_criteria_colormap()

            mask = (relative_humidity <= 45) & (wind_speed >= 20)
            lon = mask['lon']
            lat = mask['lat']
                
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
    
            try:
                ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
            except Exception as e:
                pass

            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= 45% & Wind Speed >= 20 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig


        def plot_dry_and_windy_areas_based_on_wind_gust(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
    
            r'''
            THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
    
            lon_vals, lat_vals, time, relative_humidity, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            cmap = colormaps.red_flag_warning_criteria_colormap()

            mask = (relative_humidity <= 45) & (wind_gust >= 20)
            lon = mask['lon']
            lat = mask['lat']
                
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
    
            try:
                ax.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
            except Exception as e:
                pass

            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= 45% & Wind Gust >= 20 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig


        def plot_dry_and_windy_areas_based_on_sustained_winds_3_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, subplot_title_font_size, color_table_shrink, colorbar_label_font_size, colorbar_pad, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio):
    
            r'''
            THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
    
            lon_vals, lat_vals, time, relative_humidity, wind_speed = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_red_flag_warning_parameters_using_wind_speed(utc_time)  
    
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            cmap = colormaps.red_flag_warning_criteria_colormap()
            cmap_rh = colormaps.low_relative_humidity_colormap()
            cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()

            mask = (relative_humidity <= 45) & (wind_speed >= 20)
            lon = mask['lon']
            lat = mask['lat']
                
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax0 = plt.subplot(3,1,1, projection=datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=1.5)
            ax0.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
            ax0.set_aspect(first_subplot_aspect_ratio)
            ax0.set_title("Exceptionally Dry and Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
    
            try:
                ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
            except Exception as e:
                pass


            ax1 = plt.subplot(3,1,2, projection=datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=1.5)
            ax1.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
            ax1.set_aspect(subsequent_subplot_aspect_ratio)
            ax1.set_title("Low Relative Humidity Areas", fontsize=subplot_title_font_size, fontweight='bold')
        
        
            cs1 = ax1.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 46, 1), cmap=cmap_rh, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
            cbar1.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')


            ax2 = plt.subplot(3,1,3, projection=datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=1.5)
            ax2.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
            ax2.set_aspect(subsequent_subplot_aspect_ratio)
            ax2.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')
        
        
            cs2 = ax2.contourf(lon_vals, lat_vals, wind_speed, levels=np.arange(20, 85, 5), cmap=cmap_wind, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
            cbar2.set_label(label='Wind Speed (MPH)', size=colorbar_label_font_size, fontweight='bold')
    
                
            fig.suptitle("Exceptionally Dry & Windy Areas (Shaded)\nRH <= 45% & Sustained Wind Speed >= 20 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax2.transAxes) 
    
            return fig


        def plot_dry_and_windy_areas_based_on_wind_gust_3_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, subplot_title_font_size, color_table_shrink, colorbar_label_font_size, colorbar_pad, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio):
    
            r'''
            THIS FUNCTION SHADES ALL AREAS EXPERIENCING RED FLAG WARNING CONDITIONS BASED ON ALASKA CRITERIA (TEMPERATURE >= 75F, RELATIVE HUMIDITY <= 25% AND WIND SPEED >= 15 MPH)
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
    
            lon_vals, lat_vals, time, relative_humidity, wind_gust = da.NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_red_flag_warning_parameters_using_wind_gust(utc_time)  
    
            mapcrs = ccrs.Mercator(central_longitude=-157, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            cmap = colormaps.red_flag_warning_criteria_colormap()
            cmap_rh = colormaps.low_relative_humidity_colormap()
            cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()

            mask = (relative_humidity <= 45) & (wind_gust >= 20)
            lon = mask['lon']
            lat = mask['lat']
                
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax0 = plt.subplot(3,1,1, projection=datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=1.5)
            ax0.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
            ax0.set_aspect(first_subplot_aspect_ratio)
            ax0.set_title("Exceptionally Dry and Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
    
    
            try:
                ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
                    
            except Exception as e:
                pass


            ax1 = plt.subplot(3,1,2, projection=datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=1.5)
            ax1.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
            ax1.set_aspect(subsequent_subplot_aspect_ratio)
            ax1.set_title("Low Relative Humidity Areas", fontsize=subplot_title_font_size, fontweight='bold')
        
        
            cs1 = ax1.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 46, 1), cmap=cmap_rh, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
            cbar1.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')


            ax2 = plt.subplot(3,1,3, projection=datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=1.5)
            ax2.set_extent([-160.5, -154.5, 18.5, 22.5], datacrs)
            ax2.set_aspect(subsequent_subplot_aspect_ratio)
            ax2.set_title("Wind Gusts", fontsize=subplot_title_font_size, fontweight='bold')
        
        
            cs2 = ax2.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(20, 85, 5), cmap=cmap_wind, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
            cbar2.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold')
    
                
            fig.suptitle("Exceptionally Dry & Windy Areas (Shaded)\nRH <= 45% & Wind Gust >= 20 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax2.transAxes) 
    
            return fig


    class Puerto_Rico:

        r'''
        THIS NESTED CLASS IS FOR THE GRAPHICS FOR PUERTO RICO
        '''

        def plot_generic_real_time_mesoanalysis(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot.

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
            param = parameter
    
            lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Puerto_Rico.get_RTMA_Data_single_parameter(utc_time, param)
    
            if param == 'tmp2m' or param == 'dpt2m':
                frac = 9/5
                data_to_plot = (frac * (data_to_plot - 273.15)) + 32
    
            if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                data_to_plot = data_to_plot * 2.23694
    
                
            mapcrs = ccrs.Mercator(central_longitude=-66, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-68, -64.5, 17.5, 18.7], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')
                
            plt.title(plot_title + "\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
        def plot_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
    
            lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Puerto_Rico.get_RTMA_relative_humidity(utc_time)
                
            mapcrs = ccrs.Mercator(central_longitude=-66, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            cmap = colormaps.relative_humidity_colormap()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-68, -64.5, 17.5, 18.7], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("2.5km Real Time Mesoscale Analysis\nRelative Humidity (%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
    
        def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()

            colorbar_label_font_size = colorbar_label_font_size

            colorbar_pad = colorbar_pad
    
            lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Puerto_Rico.get_RTMA_relative_humidity(utc_time)
                
            mapcrs = ccrs.Mercator(central_longitude=-66, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            cmap = colormaps.excellent_recovery_colormap()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-68, -64.5, 17.5, 18.7], datacrs)
                
            cs_low = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(0, 26, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_low.set_label(label='Low Relative Humidity (RH <= 25%)', size=colorbar_label_font_size, fontweight='bold')
    
            cs_high = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_high.set_label(label='High Relative Humidity (RH >= 80%)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
    
        def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
            cmap = colormaps.relative_humidity_change_colormap()
    
            lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Puerto_Rico.get_RTMA_Data_24_hour_change_relative_humidity(utc_time)
            mapcrs = ccrs.Mercator(central_longitude=-66, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-68, -64.5, 17.5, 18.7], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-60, 65, 5), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label='Relative Humidity Change (%)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("24-Hour Relative Humidity Change (%)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
    
        def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
            cmap = colormaps.relative_humidity_change_colormap()
            parameter = 'tmp2m'
    
            lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Puerto_Rico.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
            mapcrs = ccrs.Mercator(central_longitude=-66, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-68, -64.5, 17.5, 18.7], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='seismic', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label='Temperature Change (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
    
        def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
            parameter = 'wind10m'
    
            lon_vals, lat_vals, time, time_24, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Puerto_Rico.get_RTMA_Data_24_hour_change_single_parameter(utc_time, parameter)
            mapcrs = ccrs.Mercator(central_longitude=-66, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-68, -64.5, 17.5, 18.7], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-30, 31, 1), cmap='PuOr_r', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label='Wind Speed Change (MPH)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + time_24.strftime('%m/%d/%Y %HZ') + " - " + time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
    
        def plot_current_frost_freeze_areas(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
    
            lon_vals, lat_vals, time, data_to_plot = da.NOMADS_OPENDAP_Downloads.RTMA_Puerto_Rico.get_RTMA_Data_single_parameter(utc_time, 'tmp2m')
                
            mapcrs = ccrs.Mercator(central_longitude=-66, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-68, -64.5, 17.5, 18.7], datacrs)
                
            cs = ax.contourf(lon_vals, lat_vals, data_to_plot, levels=np.arange(-40, 33, 1), cmap='cool_r', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold')
                
            plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig
    
    
        def plot_red_flag_warning_filtered_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):
    
            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF ALASKA. 
    
            (C) METEOROLOGIST ERIC J. DREWITZ 2024
                
            '''            
            local_time, utc_time = standard.plot_creation_time()
    
            lon_vals, lat_vals, time, relative_humidity = da.NOMADS_OPENDAP_Downloads.RTMA_Puerto_Rico.get_RTMA_relative_humidity(utc_time)  
    
            mapcrs = ccrs.Mercator(central_longitude=-66, min_latitude=0, max_latitude=30.0, globe=None)
            datacrs = ccrs.PlateCarree()
    
            cmap_rh = colormaps.low_relative_humidity_colormap()
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            ax = plt.subplot(1,1,1, projection=datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)
            ax.set_extent([-68, -64.5, 17.5, 18.7], datacrs)
    
    
            cs = ax.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, alpha=0.3, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink, ax=ax, location='right', pad=colorbar_pad)
            cbar.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold')
    
                
            plt.title("Red Flag Warning Filtered Relative Humidity (RH <= 25%)\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
                
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
               verticalalignment='bottom', transform=ax.transAxes) 
    
            return fig


    class GUAM:

        r'''
        THIS NESTED CLASS HOSTS THE IMAGES FOR GUAM

        '''

        def plot_generic_real_time_mesoanalysis_no_METARs(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, state_border_color, state_border_line_thickness, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''

                This function does the following:
                                                1) Downloads the data that corresponds to the parameter the user requests. 
                                                2) Converts the units of the data (if needed).
                                                3) Plots the data that corresponds to the parameter the user requests. 

                

                Inputs:
                    1) parameter (String) - The parameter the user chooses to plot.

                                Parameters:
                                    (total of 13)
                                     
                                    ceilceil
                                    ** cloud ceiling ceiling [m]
                                     
                                    dpt2m
                                    ** 2 m above ground dew point temperature [k]
                                     
                                    gust10m
                                    ** 10 m above ground wind speed (gust) [m/s]
                                     
                                    hgtsfc
                                    ** surface geopotential height [gpm]
                                     
                                    pressfc
                                    ** surface pressure [pa]
                                     
                                    spfh2m
                                    ** 2 m above ground specific humidity [kg/kg]
                                     
                                    tcdcclm
                                    ** entire atmosphere (considered as a single layer) total cloud cover [%]
                                     
                                    tmp2m
                                    ** 2 m above ground temperature [k]
                                     
                                    ugrd10m
                                    ** 10 m above ground u-component of wind [m/s]
                                     
                                    vgrd10m
                                    ** 10 m above ground v-component of wind [m/s]
                                     
                                    vissfc
                                    ** surface visibility [m]
                                     
                                    wdir10m
                                    ** 10 m above ground wind direction (from which blowing) [degtrue]
                                     
                                    wind10m
                                    ** 10 m above ground wind speed [m/s]

                    2) plot_title (String) - The title of the entire figure. 

                    3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                    4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                    5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                    6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                    7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                    8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                    9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                    10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                    11) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                    12) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                    13) title_font_size (Integer) - The fontsize of the title of the figure. 

                    14) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                    15) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                    16) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                               Default setting is 0.05.
                                               Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                               Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 


                Returns:
                        1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            param = parameter

            if param == 'Wind_speed_gust_Analysis_height_above_ground' or param == 'Wind_speed_Analysis_height_above_ground' or param == 'Wind_speed_error_height_above_ground' or param == 'Wind_speed_gust_error_height_above_ground' or param == 'u-component_of_wind_Analysis_height_above_ground' or param == 'v-component_of_wind_Analysis_height_above_ground':

                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_current_rtma_data(utc_time, param)
                data = data * 2.23694

            if param == 'Temperature_Analysis_height_above_ground' or param == 'Dewpoint_temperature_Analysis_height_above_ground' or param == 'Temperature_error_height_above_ground' or param == 'Dewpoint_temperature_error_height_above_ground':
                
                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_current_rtma_data(utc_time, param)
                data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(data)
                

            else:
                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_current_rtma_data(utc_time, param)
                
            plot_proj = data.metpy.cartopy_crs
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)

            cs = ax.contourf(data.metpy.x, data.metpy.y, data[0, :, :], 
                             transform=data.metpy.cartopy_crs, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')

            plt.title(plot_title + "\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_generic_real_time_mesoanalysis_with_METARs(parameter, plot_title, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, mask, state_border_color, state_border_line_thickness, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF GUAM. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            param = parameter

            if param == 'Wind_speed_gust_Analysis_height_above_ground' or param == 'Wind_speed_Analysis_height_above_ground' or param == 'Wind_speed_error_height_above_ground' or param == 'Wind_speed_gust_error_height_above_ground' or param == 'u-component_of_wind_Analysis_height_above_ground' or param == 'v-component_of_wind_Analysis_height_above_ground':

               rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR_GUAM(param, utc_time, mask)
               rtma_data = rtma_data * 2.23694

            if param == 'Temperature_Analysis_height_above_ground' or param == 'Dewpoint_temperature_Analysis_height_above_ground' or param == 'Temperature_error_height_above_ground' or param == 'Dewpoint_temperature_error_height_above_ground':
                
                rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR_GUAM(param, utc_time, mask)
                rtma_data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
                

            else:
               rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR_GUAM(param, utc_time, mask)
                
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data[0, :, :], 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label=color_table_title, size=colorbar_label_font_size, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='blue',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title(plot_title + "\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\n\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') +"\n\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig



        def plot_relative_humidity_with_METARs(fig_x_length, fig_y_length, color_table_shrink, mask, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF GUAM. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR_GUAM(utc_time, mask)
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.relative_humidity_colormap()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            
            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            
            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data[0, :, :], 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 101, 1), cmap=cmap, alpha=1)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='darkorange',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title("Real Time Mesoscale Analysis Relative Humidity\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nMETAR Observations Valid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig

        def plot_red_flag_relative_humidity_with_METARs(fig_x_length, fig_y_length, color_table_shrink, mask, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF GUAM. THIS PLOT FILTERS THE RELATIVE HUMIDITY DATASET TO ONLY PLOT WHERE THE RELATIVE HUMIDITY IS 15% OR LESS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR_GUAM(utc_time, mask)
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data[0, :, :], 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=1)

            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='darkorange',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title("Real Time Mesoscale Analysis Red-Flag Relative Humidity (RH <=15%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nMETAR Observations Valid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig
 

        def plot_low_and_high_relative_humidity(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF GUAM. THIS PLOT FILTERS THE RELATIVE HUMIDITY DATASET TO ONLY PLOT WHERE THE RELATIVE HUMIDITY IS 15% OR LESS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''
            colorbar_label_font_size = colorbar_label_font_size

            colorbar_pad = colorbar_pad

            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_current_rtma_relative_humidity_data(utc_time)
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.excellent_recovery_colormap()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)

            cs_low = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data[0, :, :], 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=1)

            cs_high = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data[0, :, :], 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(80, 101, 1), cmap=cmap, alpha=1)

            cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_low.set_label(label="Low Relative Humidity (RH <= 15%)", size=colorbar_label_font_size, fontweight='bold')

            cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_high.set_label(label="High Relative Humidity (RH >= 80%)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_relative_humidity_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF GUAM. THIS PLOT COMPARES THE RELATIVE HUMIDITY FROM THE CURRENT TIME AND THE RELATIVE HUMIDITY FROM 24 HOURS AGO AND PLOTS THE 24 HOUR RELATIVE HUMIDITY CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            
            cmap = colormaps.relative_humidity_change_colormap()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_rtma_relative_humidity_24_hour_difference_data(utc_time)

            rtma_time_24 = rtma_time - timedelta(hours=24)
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data[0, :, :], 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-60, 61, 1), cmap=cmap, alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Relative Humidity Change (%)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("24-Hour Relative Humidity Change (%)\nValid: " + rtma_time_24.strftime('%m/%d/%Y %HZ') + " - " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_temperature_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF GUAM. THIS PLOT COMPARES THE TEMPERATURE FROM THE CURRENT TIME AND THE TEMPERATURE FROM 24 HOURS AGO AND PLOTS THE 24 HOUR TEMPERATURE CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_rtma_data_24_hour_difference(utc_time, 'Temperature_Analysis_height_above_ground')

            rtma_time_24 = rtma_time - timedelta(hours=24)

            rtma_data = calc.unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(rtma_data)
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='lime', zorder=3)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data[0, :, :], 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-20, 21, 1), cmap='seismic', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Temperature Change (\N{DEGREE SIGN}F)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + rtma_time_24.strftime('%m/%d/%Y %HZ') + " - " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_wind_speed_change(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF GUAM. THIS PLOT COMPARES THE WIND SPEED FROM THE CURRENT TIME AND THE WIND SPEED FROM 24 HOURS AGO AND PLOTS THE 24 HOUR WIND SPEED CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_rtma_data_24_hour_difference(utc_time, 'Wind_speed_Analysis_height_above_ground')

            rtma_time_24 = rtma_time - timedelta(hours=24)

            rtma_data = rtma_data * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=3)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data[0, :, :], 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-30, 31, 1), cmap='PuOr_r', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Wind Speed Change (MPH)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + rtma_time_24.strftime('%m/%d/%Y %HZ') + " - " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig
            


        def plot_red_flag_criteria_based_on_sustained_winds(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF GUAM. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''
            colorbar_label_font_size = colorbar_label_font_size

            colorbar_pad = colorbar_pad

            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_current_rtma_relative_humidity_data(utc_time)

            rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_current_rtma_data(utc_time, 'Wind_speed_Analysis_height_above_ground')

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)

            cs_rh = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data[0, :, :], 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=0.5)

            cs_wind = ax.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind[0, :, :], 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 100, 5), cmap='BuPu', alpha=0.5)


            cbar_rh = fig.colorbar(cs_rh, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            cbar_wind = fig.colorbar(cs_wind, location='right', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_wind.set_label(label="Wind Speed (MPH)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("Red-Flag Warning Conditions (RH <= 15% and Wind Speed >= 25 MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_criteria_based_on_wind_gusts(fig_x_length, fig_y_length, color_table_shrink, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF GUAM. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON WIND GUSTS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''
            colorbar_label_font_size = colorbar_label_font_size

            colorbar_pad = colorbar_pad

            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_current_rtma_relative_humidity_data(utc_time)

            rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_current_rtma_data(utc_time, 'Wind_speed_gust_Analysis_height_above_ground')

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)

            cs_rh = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data[0, :, :], 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=0.5)

            cs_wind = ax.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind[0, :, :], 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 100, 5), cmap='BuPu', alpha=0.5)


            cbar_rh = fig.colorbar(cs_rh, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')

            cbar_wind = fig.colorbar(cs_wind, location='right', shrink=color_table_shrink, pad=colorbar_pad)
            cbar_wind.set_label(label="Wind Gust (MPH)", size=colorbar_label_font_size, fontweight='bold')


            plt.title("Red-Flag Warning Conditions (RH <= 15% and Wind Gust >= 25 MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_dry_and_windy_areas_based_on_sustained_winds(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_speed_threshold, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap = colormaps.red_flag_warning_criteria_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_speed_threshold = red_flag_warning_wind_speed_threshold

            rtma_rh, rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_red_flag_warning_parameters_using_wind_speed(utc_time)

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_wind >= red_flag_warning_wind_speed_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj = mask.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            # Plot the mask
            try:
                ax.pcolormesh(lon,lat,mask[0, :, :],transform=ccrs.PlateCarree(),cmap=cmap)

            except Exception as e:
                pass
                

            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Wind Speed >= " + str(red_flag_warning_wind_speed_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_dry_and_windy_areas_based_on_wind_gusts(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_gust_threshold, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON WIND GUSTS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap = colormaps.red_flag_warning_criteria_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_gust_threshold = red_flag_warning_wind_gust_threshold

            rtma_rh, rtma_gust, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_red_flag_warning_parameters_using_wind_gust(utc_time)

            rtma_gust = rtma_gust * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_gust >= red_flag_warning_wind_gust_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj = mask.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)

            # Plot the mask
            try:
                ax.pcolormesh(lon,lat,mask[0, :, :],transform=ccrs.PlateCarree(),cmap=cmap)

            except Exception as e:
                pass
                

            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Wind Gust >= " + str(red_flag_warning_wind_gust_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
            
            ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_dry_and_windy_areas_based_on_sustained_winds_3_panel(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_speed_threshold, fig_x_length, fig_y_length, plot_title_font_size, subplot_title_font_size, colorbar_shrink, colorbar_pad, colorbar_label_font_size, signature_x_position, signature_y_position, signature_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap_rfw = colormaps.red_flag_warning_criteria_colormap()
            cmap_rh = colormaps.low_relative_humidity_colormap()
            cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_speed_threshold = red_flag_warning_wind_speed_threshold

            rtma_rh, rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_red_flag_warning_parameters_using_wind_speed(utc_time)

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_wind >= red_flag_warning_wind_speed_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj_1 = mask.metpy.cartopy_crs
            plot_proj_2 = rtma_rh.metpy.cartopy_crs
            plot_proj_3 = rtma_wind.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax0 = fig.add_subplot(1, 3, 1, projection=plot_proj_1)
            ax0.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_aspect(first_subplot_aspect_ratio)
            ax0.set_title("Exceptionally Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')

            # Plot the mask
            try:
                ax0.pcolormesh(lon,lat,mask[0, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)

            except Exception as e:
                pass


            ax1 = fig.add_subplot(1, 3, 2, projection=plot_proj_2)
            ax1.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_aspect(subsequent_subplot_aspect_ratio)
            ax1.set_title("Low Relative Humidity Areas", fontsize=subplot_title_font_size, fontweight='bold')

            cs_rh = ax1.contourf(rtma_rh.metpy.x, rtma_rh.metpy.y, rtma_rh[0, :, :], 
                             transform=rtma_rh.metpy.cartopy_crs, levels=np.arange(0, 61, 1), cmap=cmap_rh, alpha=1)

            cbar_rh = fig.colorbar(cs_rh, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')


            ax2 = fig.add_subplot(1, 3, 3, projection=plot_proj_3)
            ax2.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_aspect(subsequent_subplot_aspect_ratio)
            ax2.set_title("Sustained Wind Speed", fontsize=subplot_title_font_size, fontweight='bold')

            cs_wind = ax2.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind[0, :, :], 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(20, 85, 5), cmap=cmap_wind, alpha=1)

            cbar_wind = fig.colorbar(cs_wind, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_wind.set_label(label="Sustained Wind Speed (MPH)", size=colorbar_label_font_size, fontweight='bold')   
            

            fig.suptitle("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Sustained Wind Speed >= " + str(red_flag_warning_wind_speed_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=plot_title_font_size, fontweight='bold')
            
            ax0.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy\n(C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax0.transAxes)

            return fig        


        def plot_dry_and_windy_areas_based_on_wind_gusts_3_panel(red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_gust_threshold, fig_x_length, fig_y_length, plot_title_font_size, subplot_title_font_size, colorbar_shrink, colorbar_pad, colorbar_label_font_size, signature_x_position, signature_y_position, signature_font_size,  first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2024
            
            '''

            local_time, utc_time = standard.plot_creation_time()

            cmap_rfw = colormaps.red_flag_warning_criteria_colormap()
            cmap_rh = colormaps.low_relative_humidity_colormap()
            cmap_wind = colormaps.red_flag_warning_wind_parameter_colormap()

            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold

            red_flag_warning_wind_gust_threshold = red_flag_warning_wind_gust_threshold

            rtma_rh, rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.GUAM.get_red_flag_warning_parameters_using_wind_gust(utc_time)

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=144.8, central_latitude=13.45, standard_parallels=(0,30))
            datacrs = ccrs.PlateCarree()


            mask = (rtma_rh <= red_flag_warning_relative_humidity_threshold) & (rtma_wind >= red_flag_warning_wind_gust_threshold)
            lon = mask['longitude']
            lat = mask['latitude']

            plot_proj_1 = mask.metpy.cartopy_crs
            plot_proj_2 = rtma_rh.metpy.cartopy_crs
            plot_proj_3 = rtma_wind.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax0 = fig.add_subplot(3, 1, 1, projection=plot_proj_1)
            ax0.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_aspect(first_subplot_aspect_ratio)
            ax0.set_title("Exceptionally Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')

            # Plot the mask
            try:
                ax0.pcolormesh(lon,lat,mask[0, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw, shading='auto')

            except Exception as e:
                pass


            ax1 = fig.add_subplot(3, 1, 2, projection=plot_proj_2)
            ax1.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_aspect(subsequent_subplot_aspect_ratio)
            ax1.set_title("Low Relative Humidity Areas", fontsize=subplot_title_font_size, fontweight='bold')

            cs_rh = ax1.contourf(rtma_rh.metpy.x, rtma_rh.metpy.y, rtma_rh[0, :, :], 
                             transform=rtma_rh.metpy.cartopy_crs, levels=np.arange(0, 61, 1), cmap=cmap_rh, alpha=1)

            cbar_rh = fig.colorbar(cs_rh, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_rh.set_label(label="Relative Humidity (%)", size=colorbar_label_font_size, fontweight='bold')


            ax2 = fig.add_subplot(3, 1, 3, projection=plot_proj_3)
            ax2.set_extent((144.5, 145.1, 13.15, 13.75), crs=ccrs.PlateCarree())
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_aspect(subsequent_subplot_aspect_ratio)
            ax2.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')

            cs_wind = ax2.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind[0, :, :], 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(20, 85, 5), cmap=cmap_wind, alpha=1)

            cbar_wind = fig.colorbar(cs_wind, shrink=colorbar_shrink, location='bottom', pad=colorbar_pad)
            cbar_wind.set_label(label="Wind Gust (MPH)", size=colorbar_label_font_size, fontweight='bold')   
            

            fig.suptitle("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Wind Gust >= " + str(red_flag_warning_wind_gust_threshold) + " MPH\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=plot_title_font_size, fontweight='bold')
            
            ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy\n(C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax2.transAxes)

            return fig    
