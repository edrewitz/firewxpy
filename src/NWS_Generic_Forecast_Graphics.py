# THIS SCRIPT PLOTS VARIOUS DATASETS THROUGH VARIOUS DIFFERENT FUNCTIONS
#
# THIS IS THE NWS FTP DATA ACCESS FILE FOR FireWxPy
#
# DEPENDENCIES INCLUDE:
# 1. MATPLOTLIB
# 2. DATETIME
# 3. PYTZ
# 4. CARTOPY
# 5. METPY
#
#  (C) METEOROLOGIST ERIC J. DREWITZ
#               USDA/USFS

#### IMPORTS ####

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

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables

class standard:

    r'''

    THIS CLASS HOSTS STANDARD FUNCTIONS TO GET THE PLOT CREATION TIME IN UTC AND LOCAL AS WELL AS A GENERIC "NO DATA" IMAGE WHICH IS TO BE RETURNED IF THERE IS NO DATA. 

    '''
        

    def plot_creation_time():
        r'''
        FUNCTION TO GET THE CURRENT DATE/TIME FOR PLOT HEADER/FOOTER
    
        RETURNS VALUES IN THE ORDER OF:
        1. CURRENT LOCAL DATE/TIME
        2. CURRENT UTC DATE/TIME
    
        PYTHON MODULE DEPENDENCIES:
        1. DATETIME
        2. PYTZ
        
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
    
        now = datetime.now()
        UTC = now.astimezone(pytz.utc)
        
        sec = now.second
        mn = now.minute
        hr = now.hour
        dy = now.day
        mon = now.month
        yr = now.year
        
        sec1 = UTC.second
        mn1 = UTC.minute
        hr1 = UTC.hour
        dy1 = UTC.day
        mon1 = UTC.month
        yr1 = UTC.year
        
        Local_Time_Now = datetime(yr, mon, dy, hr, mn, sec)
        UTC_Now = datetime(yr1, mon1, dy1, hr1, mn1, sec1)
        
        return Local_Time_Now, UTC_Now
    
    
    def no_data_graphic():
        r'''
        THIS FUNCTION RETURNS A DEFAULT GRAPHIC WHEN NO DATA IS PRESENT
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
        local_time, utc_time = standard.plot_creation_time()
        
        fig = plt.figure(figsize=(20,10))
        ax = plt.subplot(1, 1, 1)
        plt.axis('off')
        fig.text(0.04, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontsize=20, fontweight='bold')
        ax.text(0.1, 0.6, 'NO DATA FOR: ' + utc_time.strftime('%m/%d/%Y %HZ'), fontsize=60, fontweight='bold')
    
        return fig

class Counties_Perspective:

    r'''

    THIS CLASS HOSTS A VARIETY OF PLOTTING FUNCTIONS. 

    THESE FUNCTIONS PLOT THE NATIONAL WEATHER SERVICE GRIDDED FORECAST DATA IN VARIOUS DIFFERENT WAYS

    GENERIC FORECAST FUNCTIONS OFFER SLIGHTLY MORE CUSTOMIZATION AS BOTH THE GENERIC FUNCTIONS ARE NOT PRESETS FOR A CERTAIN WEATHER ELEMENT. 

    THIS CLASS PLOTS THE DATA USING COUNTY AND STATE BOUNDARIES AS A REFERENCE POINT. 

    (C) METEOROLOGIST ERIC J. DREWITZ 2023


    '''


    def plot_generic_short_term_forecast(directory_name, parameter, grid_time_interval, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, color_table, color_table_start, color_table_stop, color_table_step, plot_title, sub_plot_1_title, sub_plot_2_title, sub_plot_3_title, sub_plot_4_title, sub_plot_5_title, fig_x_length, fig_y_length, color_bar_shrink, state_border_color, county_border_color, state_border_line_thickness, county_border_line_thickness, signature_x_position, signature_y_position): 
    
        r'''
        THIS FUNCTION MAKES A GENERIC CUSTOMIZED PLOT OF THE LATEST SHORT-TERM NOAA/NWS NDFD GRID FORECAST DATA
    
        THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
        1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
        2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        3. WEATHER PARAMETER 
        4. COLOR TABLE FOR PLOT 
        5. COLOR TABLE START, STOP AND STEP
        6. GRID TIME INTERVALS IN HOURS (DIFFERENT GRIDS ARE DIFFERENT LENGTHS IN TIME)
        7. PLOT TITLE - TITLE MUST BE ENTERED AS A STRING VARIABLE
        8. COLORBAR SHRINK - FLOAT VARIABLE THAT DETERMINES THE SIZE OF THE COLORBAR. THE DEFAULT IS 1.0. TO SHRINK THE SIZE OF THE COLORBAR SET SHRINK TO A FLOAT VALUE BETWEEN 0 AND 1. TO INCREASE THE SIZE OF THE COLORBAR SET THE SHRINK VALUE TO ABOVE 1. 
        9. FIGURE SIZE IS CUSTOMIZED BY THE INTEGER VARIABLES (fig_x_length, fig_y_length) IF YOUR PLOT COMES OUT LOOKING FUNKY (I.E. WORDS OVERLAPPING, COLORBARS NOT SIZED PROPERLY EVEN AFTER YOU EDIT THE SIZE OF THE COLORBAR SHRINK ETC.), EDIT THE SIZE OF THE FIGURE SIZE
    
        PYTHON MODULE DEPENDENCIES:
        1. CARTOPY
        2. METPY
        3. NUMPY
        4. MATPLOTLIB
        5. PARSERS
        6. DATA_ACCESS
    
        **IF THE USER WANTS TO MAKE 2 SEPERATE PLOTS WITH 1 AS THE SHORT-TERM AND THE OTHER AS THE EXTENDED, THE PROGRAMS FOR EACH NEED TO BE RUN IN DIFFERENT FOLDERS SO THE BINARY FILE DOESN'T OVERWRITE ITSELF**
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
        
        short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, parameter)
        
        first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, parameter)
    
        local_time, utc_time = standard.plot_creation_time()
    
        
        files = count_of_GRIB_files
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()
    
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, parameter)

       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_bar_shrink)
    
        if files == 2:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax3.set_title(sub_plot_4_title + '\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_bar_shrink) 
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax3.set_title(sub_plot_4_title + '\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_bar_shrink)
    
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax4.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax4.set_title(sub_plot_5_title + '\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar4 = fig.colorbar(cs4, shrink=color_bar_shrink) 
    
        return fig
    
    def plot_generic_extended_forecast(directory_name, parameter, grid_time_interval, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, color_table, color_table_start, color_table_stop, color_table_step, plot_title, sub_plot_1_title, sub_plot_2_title, sub_plot_3_title, sub_plot_4_title, sub_plot_5_title, fig_x_length, fig_y_length, color_bar_shrink, state_border_color, county_border_color, state_border_line_thickness, county_border_line_thickness, signature_x_position, signature_y_position): 
    
        r'''
        THIS FUNCTION MAKES A GENERIC CUSTOMIZED PLOT OF THE LATEST EXTENDED NOAA/NWS NDFD GRID FORECAST DATA
    
        THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
        1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
        2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        3. WEATHER PARAMETER 
        4. COLOR TABLE FOR PLOT 
        5. COLOR TABLE START, STOP AND STEP
        6. GRID TIME INTERVALS IN HOURS (DIFFERENT GRIDS ARE DIFFERENT LENGTHS IN TIME)
        7. PLOT TITLE - TITLE MUST BE ENTERED AS A STRING VARIABLE
        8. COLORBAR SHRINK - FLOAT VARIABLE THAT DETERMINES THE SIZE OF THE COLORBAR. THE DEFAULT IS 1.0. TO SHRINK THE SIZE OF THE COLORBAR SET SHRINK TO A FLOAT VALUE BETWEEN 0 AND 1. TO INCREASE THE SIZE OF THE COLORBAR SET THE SHRINK VALUE TO ABOVE 1. 
        9. FIGURE SIZE IS CUSTOMIZED BY THE INTEGER VARIABLES (fig_x_length, fig_y_length) IF YOUR PLOT COMES OUT LOOKING FUNKY (I.E. WORDS OVERLAPPING, COLORBARS NOT SIZED PROPERLY EVEN AFTER YOU EDIT THE SIZE OF THE COLORBAR SHRINK ETC.), EDIT THE SIZE OF THE FIGURE SIZE
        10. THE TITLES FOR EACH SUBPLOT
    
        PYTHON MODULE DEPENDENCIES:
        1. CARTOPY
        2. METPY
        3. NUMPY
        4. MATPLOTLIB
        5. PARSERS
        6. DATA_ACCESS
    
        **IF THE USER WANTS TO MAKE 2 SEPERATE PLOTS WITH 1 AS THE SHORT-TERM AND THE OTHER AS THE EXTENDED, THE PROGRAMS FOR EACH NEED TO BE RUN IN DIFFERENT FOLDERS SO THE BINARY FILE DOESN'T OVERWRITE ITSELF**
        
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
        
        
        extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, parameter)
        
        first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, parameter)
    
        local_time, utc_time = standard.plot_creation_time()
    
        
        files = count_of_GRIB_files
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()
    
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, parameter)
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_bar_shrink)
    
        if files == 2:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax3.set_title(sub_plot_4_title + '\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_bar_shrink) 
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax3.set_title(sub_plot_4_title + '\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_bar_shrink)
    
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=state_border_line_thickness, edgecolor=state_border_color, zorder=3)
            ax4.add_feature(USCOUNTIES, linewidth=county_border_line_thickness, edgecolor=county_border_color, zorder=2)
            ax4.set_title(sub_plot_5_title + '\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar4 = fig.colorbar(cs4, shrink=color_bar_shrink) 
    
        return fig


class Predictive_Services_Areas_Perspective:

    r'''
    THIS CLASS HOSTS A VARIETY OF PLOTTING FUNCTIONS. 

    THESE FUNCTIONS PLOT THE NATIONAL WEATHER SERVICE GRIDDED FORECAST DATA IN VARIOUS DIFFERENT WAYS

    GENERIC FORECAST FUNCTIONS OFFER SLIGHTLY MORE CUSTOMIZATION AS BOTH THE GENERIC FUNCTIONS ARE NOT PRESETS FOR A CERTAIN WEATHER ELEMENT. 

    THIS CLASS PLOTS THE DATA USING PREDICTIVE SERVICES AREAS (PSA) BOUNDARIES AS A REFERENCE POINT. 

    (C) METEOROLOGIST ERIC J. DREWITZ 2023

    '''

    def plot_generic_short_term_forecast(directory_name, parameter, grid_time_interval, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, color_table, color_table_start, color_table_stop, color_table_step, plot_title, sub_plot_1_title, sub_plot_2_title, sub_plot_3_title, sub_plot_4_title, sub_plot_5_title, fig_x_length, fig_y_length, color_bar_shrink, PSA_Border_Color, PSA_Border_Line_Thickness, GACC_Border_Color, GACC_Border_Thickness, signature_x_position, signature_y_position): 
    
        r'''
        THIS FUNCTION MAKES A GENERIC CUSTOMIZED PLOT OF THE LATEST SHORT-TERM NOAA/NWS NDFD GRID FORECAST DATA
    
        THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
        1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
        2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        3. WEATHER PARAMETER 
        4. COLOR TABLE FOR PLOT 
        5. COLOR TABLE START, STOP AND STEP
        6. GRID TIME INTERVALS IN HOURS (DIFFERENT GRIDS ARE DIFFERENT LENGTHS IN TIME)
        7. PLOT TITLE - TITLE MUST BE ENTERED AS A STRING VARIABLE
        8. COLORBAR SHRINK - FLOAT VARIABLE THAT DETERMINES THE SIZE OF THE COLORBAR. THE DEFAULT IS 1.0. TO SHRINK THE SIZE OF THE COLORBAR SET SHRINK TO A FLOAT VALUE BETWEEN 0 AND 1. TO INCREASE THE SIZE OF THE COLORBAR SET THE SHRINK VALUE TO ABOVE 1. 
        9. FIGURE SIZE IS CUSTOMIZED BY THE INTEGER VARIABLES (fig_x_length, fig_y_length) IF YOUR PLOT COMES OUT LOOKING FUNKY (I.E. WORDS OVERLAPPING, COLORBARS NOT SIZED PROPERLY EVEN AFTER YOU EDIT THE SIZE OF THE COLORBAR SHRINK ETC.), EDIT THE SIZE OF THE FIGURE SIZE
    
        PYTHON MODULE DEPENDENCIES:
        1. CARTOPY
        2. METPY
        3. NUMPY
        4. MATPLOTLIB
        5. PARSERS
        6. DATA_ACCESS
    
        **IF THE USER WANTS TO MAKE 2 SEPERATE PLOTS WITH 1 AS THE SHORT-TERM AND THE OTHER AS THE EXTENDED, THE PROGRAMS FOR EACH NEED TO BE RUN IN DIFFERENT FOLDERS SO THE BINARY FILE DOESN'T OVERWRITE ITSELF**
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
        
        short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, parameter)
        
        first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, parameter)
    
        local_time, utc_time = standard.plot_creation_time()
    
        
        files = count_of_GRIB_files
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs(PSA_Border_Color)
    
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, parameter)

       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_bar_shrink)
    
        if files == 2:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax3.set_title(sub_plot_4_title + '\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_bar_shrink) 
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax3.set_title(sub_plot_4_title + '\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_bar_shrink)
    
            ax4 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax4.set_title(sub_plot_5_title + '\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar4 = fig.colorbar(cs4, shrink=color_bar_shrink) 
    
        return fig
    
    def plot_generic_extended_forecast(directory_name, parameter, grid_time_interval, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, color_table, color_table_start, color_table_stop, color_table_step, plot_title, sub_plot_1_title, sub_plot_2_title, sub_plot_3_title, sub_plot_4_title, sub_plot_5_title, fig_x_length, fig_y_length, color_bar_shrink, PSA_Border_Color, PSA_Border_Line_Thickness, GACC_Border_Color, GACC_Border_Thickness, signature_x_position, signature_y_position): 
    
        r'''
        THIS FUNCTION MAKES A GENERIC CUSTOMIZED PLOT OF THE LATEST EXTENDED NOAA/NWS NDFD GRID FORECAST DATA
    
        THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
        1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
        2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        3. WEATHER PARAMETER 
        4. COLOR TABLE FOR PLOT 
        5. COLOR TABLE START, STOP AND STEP
        6. GRID TIME INTERVALS IN HOURS (DIFFERENT GRIDS ARE DIFFERENT LENGTHS IN TIME)
        7. PLOT TITLE - TITLE MUST BE ENTERED AS A STRING VARIABLE
        8. COLORBAR SHRINK - FLOAT VARIABLE THAT DETERMINES THE SIZE OF THE COLORBAR. THE DEFAULT IS 1.0. TO SHRINK THE SIZE OF THE COLORBAR SET SHRINK TO A FLOAT VALUE BETWEEN 0 AND 1. TO INCREASE THE SIZE OF THE COLORBAR SET THE SHRINK VALUE TO ABOVE 1. 
        9. FIGURE SIZE IS CUSTOMIZED BY THE INTEGER VARIABLES (fig_x_length, fig_y_length) IF YOUR PLOT COMES OUT LOOKING FUNKY (I.E. WORDS OVERLAPPING, COLORBARS NOT SIZED PROPERLY EVEN AFTER YOU EDIT THE SIZE OF THE COLORBAR SHRINK ETC.), EDIT THE SIZE OF THE FIGURE SIZE
        10. THE TITLES FOR EACH SUBPLOT
    
        PYTHON MODULE DEPENDENCIES:
        1. CARTOPY
        2. METPY
        3. NUMPY
        4. MATPLOTLIB
        5. PARSERS
        6. DATA_ACCESS
    
        **IF THE USER WANTS TO MAKE 2 SEPERATE PLOTS WITH 1 AS THE SHORT-TERM AND THE OTHER AS THE EXTENDED, THE PROGRAMS FOR EACH NEED TO BE RUN IN DIFFERENT FOLDERS SO THE BINARY FILE DOESN'T OVERWRITE ITSELF**
        
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
        
        
        extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, parameter)
        
        first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, parameter)
    
        local_time, utc_time = standard.plot_creation_time()
    
        
        files = count_of_GRIB_files
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs(PSA_Border_Color)
    
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, parameter)
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_bar_shrink)
    
        if files == 2:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax3.set_title(sub_plot_4_title + '\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_bar_shrink) 
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length,fig_y_length))
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\n" + plot_title, fontweight='bold')
            
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax0.set_title(sub_plot_1_title + '\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_bar_shrink)
    
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax1.set_title(sub_plot_2_title + '\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_bar_shrink)
    
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax2.set_title(sub_plot_3_title + '\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_bar_shrink)
    
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax3.set_title(sub_plot_4_title + '\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_bar_shrink)
    
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(PSAs, linewidth=PSA_Border_Line_Thickness)
            ax4.set_title(sub_plot_5_title + '\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
            cbar4 = fig.colorbar(cs4, shrink=color_bar_shrink) 
    
        return fig




            
