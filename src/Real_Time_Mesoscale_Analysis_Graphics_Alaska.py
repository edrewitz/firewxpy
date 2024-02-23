'''
This file hosts all the Real Time Mesoscale Analysis (RTMA) plotting functions in FireWxPy. 
The RTMA data consists of gridded data for current conditions with a grid spacing of 2.5km x 2.5km.

There are 2 primary classes which are used to define the perspective of the plot: 
1) Counties_Perspective - This class uses state and county borders as the geographical reference. 
2) Predictive_Services_Areas_Perspective - This class uses the Geographic Area Coordination Center (GACC) and Predictive Services Area (PSA) boundaries as the geographical reference. 

Inside of the aforementied 2 primary classes are a series of subclasses or nested classes. Given the size of Alaska, these subclasses breakdown the view throughout the state. 
These subclasses within the Counties_Perspective and Predictive_Services_Areas_Perspective are as follows:

Counties_Perspective:
                1) Entire_State - This is the view for the entire state. Boundaries: West = 174W, East = 128W, South = 45N, North = 80N
                2) South_Central - This is the view for Southcentral Alaska. Boundaries: West = 155W, East = 140.75W, South = 58.75N, North = 64N
                3) Southwest - This is the view for Southwest Alaska. Boundaries: West = 168W, East = 153W, South = 55N, North = 64N
                4) Southeast - This is the view for Southeast Alaska. Boundaries: West = 144.75W, East = 129.75W, South = 54.5N, North = 61N
                5) Interior_And_Northslope - This is the view for Interior Alaska and the Northslope. Boundaries: West = 169.5W, East = 140.75W, South = 63N, North = 75N
                6) Kodiak - This is the view for Kodiak Island. Boundaries: West = 156W, East = 150.75W, South = 56N, North = 59.1N

Predictive_Services_Areas_Perspective:
                1) Entire_State - This is the view for the entire state. Boundaries: West = 174W, East = 128W, South = 45N, North = 80N
                2) South_Central - This is the view for Southcentral Alaska. Boundaries: West = 155W, East = 140.75W, South = 58.75N, North = 64N
                3) Southwest - This is the view for Southwest Alaska. Boundaries: West = 168W, East = 153W, South = 55N, North = 64N
                4) Southeast - This is the view for Southeast Alaska. Boundaries: West = 144.75W, East = 129.75W, South = 54.5N, North = 61N
                5) Interior_And_Northslope - This is the view for Interior Alaska and the Northslope. Boundaries: West = 169.5W, East = 140.75W, South = 63N, North = 75N

*** Due to all of Kodiak Island being in the same PSA, there is no Kodiak subclass in the Predictive_Services_Areas_Perspective. Kodiak is only accessible in the Counties_Perspective.***

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

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from NWS_Generic_Forecast_Graphics import standard


class Counties_Perspective:

  r'''
  This class hosts all the graphical functions that use county and state borders as the geographic reference. 
  ''''

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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
          
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for temperature, filtered to areas where the temperature is below freezing. 
          
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
                                          1) Downloads the temperature and dewpoint data arrays for the current time.
                                          2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data array.
                                          3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the relative humidity <= 25%. 
          
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis filtered low relative humidity (RH <= 25%)
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Gust >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
          
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
         South_Central: This class hosts the graphics for Southcentral Alaska. 
         This includes: 1) Anchorage Bowl, 2) Kenai Peninsula, 3) Matanuska Valley, 4) Susitna Valley, 5) Copper River Basin and 6) Prince William Sound Area. 
         Latitude/Longitude Bounds: (West = 155W, East = 140.75W, South = 58.75N, North = 64N)
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
          
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for temperature, filtered to areas where the temperature is below freezing. 
          
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
          This function does the following:
                                          1) Downloads the temperature and dewpoint data arrays for the current time.
                                          2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data array.
                                          3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the relative humidity <= 25%. 
          
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis filtered low relative humidity (RH <= 25%)
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Gust >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
          
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
        Southwest: This class hosts the graphics for Southwest Alaska. 
        This includes the 1) Kuskokwim Valley, 2) Kuskokwim Delta and 3) Bristol Bay. 
        Latitude/Longitude Bounds: (West = 168W, East = 153W, South = 55N, North = 64N)
             
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
          
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for temperature, filtered to areas where the temperature is below freezing. 
          
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
          This function does the following:
                                          1) Downloads the temperature and dewpoint data arrays for the current time.
                                          2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data array.
                                          3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the relative humidity <= 25%. 
          
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis filtered low relative humidity (RH <= 25%)
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
  
  
      def plot_hot_dry_windy_areas_based_on_wind_gusts(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
  
          r'''
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Gust >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          ax.set_extent([-168, -153, 55, 64], datacrs)
  
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
          
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
          Southeast: This class hosts the graphics for Southeast Alaska. 
          This includes 1) All the islands in the Alaska Panhandle, 2) Yakutat.
          Latitude/Longitude Bounds: (West = 144.75W, East = 129.75W, South = 54.5N, North = 61N)
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
          
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for temperature, filtered to areas where the temperature is below freezing. 
          
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
          This function does the following:
                                          1) Downloads the temperature and dewpoint data arrays for the current time.
                                          2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data array.
                                          3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the relative humidity <= 25%. 
          
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis filtered low relative humidity (RH <= 25%)
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
  
  
      def plot_hot_dry_windy_areas_based_on_wind_gusts(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
  
          r'''
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Gust >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
  
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
          
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
          Interior_And_Northslope: This class hosts the graphics for the Alaskan Interior and North Slope.
          This includes: 1) North Slope, 2) Brooks Range, 3) Seward Peninsula, 4) Arctic National Wildlife Refuge (ANWR). 
          Latitude/Longitude Bounds: (West = 169.5W, East = 140.75W, South = 63N, North = 75N)
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
          
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for temperature, filtered to areas where the temperature is below freezing. 
          
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
          This function does the following:
                                          1) Downloads the temperature and dewpoint data arrays for the current time.
                                          2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data array.
                                          3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the relative humidity <= 25%. 
          
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis filtered low relative humidity (RH <= 25%)
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
  
  
  
      def plot_hot_dry_windy_areas_based_on_wind_gusts(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
  
          r'''
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Gust >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
  
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
          
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
          Kodiak: This class hosts the graphics for Kodiak Island. 
          This includes all communities on Kodiak Island. 
          Latitude/Longitude Bounds: (West = 156W, East = 150.75W, South = 56N, North = 59.1N)
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
          
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for temperature, filtered to areas where the temperature is below freezing. 
          
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
          This function does the following:
                                          1) Downloads the temperature and dewpoint data arrays for the current time.
                                          2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data array.
                                          3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the relative humidity <= 25%. 
          
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis filtered low relative humidity (RH <= 25%)
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
  
  
      def plot_hot_dry_windy_areas_based_on_wind_gusts(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
  
          r'''
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Gust >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          ax.set_extent([-156, -150.75, 56, 59.1], datacrs)
  
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
          
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

class Predictive_Services_Areas_Perspective:

  r'''
  This class hosts all the graphical functions that use Geographic Area Coordination Center (GACC) and Predictive Services Areas (PSAs) as the geographic reference. 
  ''''

  class Entire_State:
  
      r'''
      
      Entire_State: This class allows the user to view the entire state of Alaska. 
      Latitude/Longitude Bounds: (West = 174W, East = 128W, South = 45N, North = 80N)
      
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
          
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for temperature, filtered to areas where the temperature is below freezing. 
          
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
          This function does the following:
                                          1) Downloads the temperature and dewpoint data arrays for the current time.
                                          2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data array.
                                          3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the relative humidity <= 25%. 
          
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis filtered low relative humidity (RH <= 25%)
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Gust >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
          
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
  
  
  
      def plot_hot_dry_windy_areas_based_on_wind_gusts_4_panel(fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size, title_font_size, colorbar_label_font_size, color_table_shrink, subplot_title_font_size, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, colorbar_pad):
  
          r'''
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
          
          '''            
          local_time, utc_time = standard.plot_creation_time()
  
          colorbar_pad = colorbar_pad
  
          first_subplot_aspect_ratio = first_subplot_aspect_ratio
  
          subsequent_subplot_aspect_ratio = subsequent_subplot_aspect_ratio
  
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
          ax0.set_aspect(first_subplot_aspect_ratio)
          ax0.set_extent([-174, -128, 45, 80], datacrs)
          ax0.set_title("Hot & Dry & Windy Areas", fontsize=subplot_title_font_size, fontweight='bold')
  
          try:
              ax0.pcolormesh(lon,lat,mask,transform=datacrs,cmap=cmap)
              
          except Exception as e:
              pass
  
  
          ax1 = plt.subplot(gs[0:8, 8:15], projection=datacrs)
          ax1.add_feature(GACC, linewidth=2.5, zorder=3)
          ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
          ax1.set_aspect(subsequent_subplot_aspect_ratio)
          ax1.set_extent([-174, -128, 45, 80], datacrs)
          ax1.set_title("Temperature", fontsize=subplot_title_font_size, fontweight='bold')
  
          cs_temp = ax1.contourf(lon_vals, lat_vals, temperature, levels=np.arange(75, 100, 1), cmap=cmap_temperature, transform=datacrs)
          cbar_temp = fig.colorbar(cs_temp, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
          cbar_temp.set_label(label='Temperature (\N{DEGREE SIGN}F)', size=colorbar_label_font_size, fontweight='bold') 
  
          ax2 = plt.subplot(gs[8:15, 0:7], projection=datacrs)
          ax2.add_feature(GACC, linewidth=2.5, zorder=3)
          ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
          ax2.set_aspect(subsequent_subplot_aspect_ratio)
          ax2.set_extent([-174, -128, 45, 80], datacrs)
          ax2.set_title("Relative Humidity", fontsize=subplot_title_font_size, fontweight='bold')
  
          cs_rh = ax2.contourf(lon_vals, lat_vals, relative_humidity, levels=np.arange(0, 26, 1), cmap=cmap_rh, transform=datacrs)
          cbar_rh = fig.colorbar(cs_rh, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
          cbar_rh.set_label(label='Relative Humidity (%)', size=colorbar_label_font_size, fontweight='bold') 
  
  
          ax3 = plt.subplot(gs[8:15, 8:15], projection=datacrs)
          ax3.add_feature(GACC, linewidth=2.5, zorder=3)
          ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
          ax3.set_aspect(subsequent_subplot_aspect_ratio)
          ax3.set_extent([-174, -128, 45, 80], datacrs)
          ax3.set_title("Wind Gust", fontsize=subplot_title_font_size, fontweight='bold')
  
          cs_wind = ax3.contourf(lon_vals, lat_vals, wind_gust, levels=np.arange(15, 75, 5), cmap=cmap_wind, transform=datacrs)
          cbar_wind = fig.colorbar(cs_wind, shrink=color_table_shrink, location='bottom', pad=colorbar_pad)
          cbar_wind.set_label(label='Wind Gust (MPH)', size=colorbar_label_font_size, fontweight='bold') 
  
          
          fig.suptitle("Hot & Dry & Windy Areas (Shaded)\nT >= 75\N{DEGREE SIGN}F & RH <= 25% & Wind Gusts >= 15 MPH\nValid: " + time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=title_font_size, fontweight='bold')
          
          ax2.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: NOAA/NCEP/NOMADS", fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
         verticalalignment='bottom', transform=ax2.transAxes) 
  
          return fig
  
  
  
  class South_Central:
  
      r'''
         South_Central: This class hosts the graphics for Southcentral Alaska. 
         This includes: 1) Anchorage Bowl, 2) Kenai Peninsula, 3) Matanuska Valley, 4) Susitna Valley, 5) Copper River Basin and 6) Prince William Sound Area. 
         Latitude/Longitude Bounds: (West = 155W, East = 140.75W, South = 58.75N, North = 64N)
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
          
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for temperature, filtered to areas where the temperature is below freezing. 
          
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
          This function does the following:
                                          1) Downloads the temperature and dewpoint data arrays for the current time.
                                          2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data array.
                                          3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the relative humidity <= 25%. 
          
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis filtered low relative humidity (RH <= 25%)
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Gust >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
          
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
        Southwest: This class hosts the graphics for Southwest Alaska. 
        This includes the 1) Kuskokwim Valley, 2) Kuskokwim Delta and 3) Bristol Bay. 
        Latitude/Longitude Bounds: (West = 168W, East = 153W, South = 55N, North = 64N)
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
          
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for temperature, filtered to areas where the temperature is below freezing. 
          
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
          This function does the following:
                                          1) Downloads the temperature and dewpoint data arrays for the current time.
                                          2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data array.
                                          3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the relative humidity <= 25%. 
          
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis filtered low relative humidity (RH <= 25%)
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
  
  
      def plot_hot_dry_windy_areas_based_on_wind_gusts(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
  
          r'''
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Gust >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          ax.set_extent([-168, -153, 55, 64], datacrs)
  
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
          
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
          Southeast: This class hosts the graphics for Southeast Alaska. 
          This includes 1) All the islands in the Alaska Panhandle, 2) Yakutat.
          Latitude/Longitude Bounds: (West = 144.75W, East = 129.75W, South = 54.5N, North = 61N)
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
          
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for temperature, filtered to areas where the temperature is below freezing. 
          
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
          This function does the following:
                                          1) Downloads the temperature and dewpoint data arrays for the current time.
                                          2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data array.
                                          3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the relative humidity <= 25%. 
          
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis filtered low relative humidity (RH <= 25%)
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
  
  
      def plot_hot_dry_windy_areas_based_on_wind_gusts(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
  
          r'''
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Gust >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          ax.set_extent([-144.75, -129.75, 54.5, 61], datacrs)
  
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
          
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
          Interior_And_Northslope: This class hosts the graphics for the Alaskan Interior and North Slope.
          This includes: 1) North Slope, 2) Brooks Range, 3) Seward Peninsula, 4) Arctic National Wildlife Refuge (ANWR). 
          Latitude/Longitude Bounds: (West = 169.5W, East = 140.75W, South = 63N, North = 75N)
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the 24-Hour difference with respect to wind speed (MPH). 
          
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for temperature, filtered to areas where the temperature is below freezing. 
          
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
          This function does the following:
                                          1) Downloads the temperature and dewpoint data arrays for the current time.
                                          2) Uses MetPy to calculate the relative humidity data array from the temperature and dewpoint data array.
                                          3) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the relative humidity <= 25%. 
          
  
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
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis filtered low relative humidity (RH <= 25%)
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
  
  
      def plot_hot_dry_windy_areas_based_on_wind_gusts(fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_font_size, signature_font_size):
  
          r'''
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Gust >= 15 MPH). 
                                          6) Plots the 2.5km x 2.5km Real Time Mesoscale Analysis for areas where the aforementioned "Hot Dry and Windy" criteria are met. 
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
  
          Returns:
                  1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis showing current areas of hot, dry and windy conditions. 
          
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
          ax.set_extent([-169.5, -140.75, 63, 75], datacrs)
  
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind speed data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind speed data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind speed filtered only showing areas where Wind Speed >= 15 MPH
          
          
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
          This function does the following:
                                          1) Downloads the latest available temperature, dewpoint, and wind gust data arrays. 
                                          2) Converts the temperature values from Kelvin to Fahrenheit.
                                          3) Uses MetPy to calculate a relative humidity data array from the temperature and dewpoint data arrays. 
                                          4) Converts the wind gust data array from m/s to MPH. 
                                          5) Masks all areas where the following criteria is not met: Temperature >= 75F, RH <= 25% and Wind Speed >= 15 MPH). 
                                          6) Plots a figure that consists of 4 subplots.
                                          List of subplots:
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH
                                           
          
  
          Inputs:
  
              1) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
  
              2) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
  
              3) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
  
              4) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
  
              5) title_font_size (Integer) - The fontsize of the title of the figure. 
  
              6) signature_font_size (Integer) - The fontsize of the signature of the figure. 
  
              7) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 
  
              8) color_table_shrink (Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 
  
              9) subplot_title_font_size (Integer) - Fontsize of all subplot titles. 
              
              10) first_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the first subplot. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size. 
              
              11) subsequent_subplot_aspect_ratio (Integer or Float) - The width to height ratio of the second, third and fourth subplots. When some subplots have colorbars while others do not in the same figure, this needs to be edited so all subplots appear to have the same size.
  
              12) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                         Default setting is 0.05.
                                         Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                         Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 
  
  
          Returns:
                  1) A figure showing the four aforementioned subplots:                                                             
                                                      1) Plot where the hot, dry and windy conditions are located. 
                                                      2) Plot the relative humidity filtered only showing areas where the RH <= 25%
                                                      3) Plot the temperature filtered only showing areas where T >= 75F
                                                      4) Plot the wind gust filtered only showing areas where Wind Gust >= 15 MPH                
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
  
