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
import colormaps

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from NWS_Generic_Forecast_Graphics import standard

class Counties_Perspective:

    class CONUS:

        r'''
        THIS NESTED CLASS HOSTS THE IMAGES FOR CONUS AKA THE "LOWER-48"
        '''
    
        def plot_relative_humidity_poor_recovery_short_term_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS OF POOR OVERNIGHT RELATIVE HUMIDITY RECOVERY FROM THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
        
        
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
            
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
         
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
             
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
                    
                    ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=0.70)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                    fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax4.add_feature(cfeature.STATES, linewidth=0.5)
                    ax4.add_feature(USCOUNTIES, linewidth=1.5)
                    ax4.set_title('Night 5 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                    cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig
    
    
        
        def plot_relative_humidity_poor_recovery_extended_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS OF POOR OVERNIGHT RELATIVE HUMIDITY RECOVERY FROM THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
        
        
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
            
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
         
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
        
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=0.70)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_title('Night 7 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 4 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Night 5 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_title('Night 6 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax4.add_feature(cfeature.STATES, linewidth=0.5)
                ax4.add_feature(USCOUNTIES, linewidth=1.5)
                ax4.set_title('Night 7 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig
        
        def plot_relative_humidity_excellent_recovery_short_term_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS OF EXCELLENT OVERNIGHT RELATIVE HUMIDITY RECOVERY FROM THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
            
            short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.excellent_recovery_colormap()
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
            
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
         
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
             
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
                    
                    ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                    fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax4.add_feature(cfeature.STATES, linewidth=0.5)
                    ax4.add_feature(USCOUNTIES, linewidth=1.5)
                    ax4.set_title('Night 5 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                    cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig
        
        def plot_relative_humidity_excellent_recovery_extended_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS OF EXCELLENT OVERNIGHT RELATIVE HUMIDITY RECOVERY FROM THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
            
            extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.excellent_recovery_colormap()
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
            
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
         
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
             
            if files == 3:
        
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_title('Night 7 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 4 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Night 5 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_title('Night 6 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax4.add_feature(cfeature.STATES, linewidth=0.5)
                ax4.add_feature(USCOUNTIES, linewidth=1.5)
                ax4.set_title('Night 7 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig
        
        
        
        def plot_red_flag_minimum_relative_humidity_short_term_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS WHERE MINIMUM RELATIVE HUMIDITY IS FORECAST TO MEET AND/OR EXCEED THE RED FLAG WARNING CRITERIA FOR MINIMUM RELATIVE HUMIDITY (MIN RH <= 15%) AND IS BASED ON THE National Weather Service Short-Term Forecast
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MINIMUM RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.minrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.minrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
        
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
            
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
         
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
             
                if utc_time.hour > 21 or utc_time.hour <= 6:
        
                    fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
                    
                    ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
        
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
                
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour > 21 or utc_time.hour <= 6:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour > 21 or utc_time.hour <= 6:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                    fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax4.add_feature(cfeature.STATES, linewidth=0.5)
                    ax4.add_feature(USCOUNTIES, linewidth=1.5)
                    ax4.set_title('Day 5 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                    cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour > 21 or utc_time.hour <= 6:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig
    
    
        def plot_red_flag_minimum_relative_humidity_extended_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS WHERE MINIMUM RELATIVE HUMIDITY IS FORECAST TO MEET AND/OR EXCEED THE RED FLAG WARNING CRITERIA FOR MINIMUM RELATIVE HUMIDITY (MIN RH <= 15%) AND IS BASED ON THE National Weather Service Extended Forecast
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MINIMUM RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, 'ds.minrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, 'ds.minrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
        
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
            
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
        
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
         
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
        
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Day 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Day 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_title('Day 7 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Day 3 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Day 4 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Day 5 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_title('Day 6 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax4.add_feature(cfeature.STATES, linewidth=0.5)
                ax4.add_feature(USCOUNTIES, linewidth=1.5)
                ax4.set_title('Day 7 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig


        def plot_maximum_relative_humidity_short_term_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS THE NWS OVERNIGHT RELATIVE HUMIDITY FORECAST AND THE FORECAST TRENDS OF OVERNIGHT RELATIVE HUMIDITY 
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.relative_humidity_colormap()

            cmap_change = colormaps.relative_humidity_change_colormap()
        
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
    
            lons = lons_1
            lats = lats_1
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
         
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
             
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
                    
                    ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files == 4:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files >= 5:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                    fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax4.add_feature(cfeature.STATES, linewidth=0.5)
                    ax4.add_feature(USCOUNTIES, linewidth=1.5)
                    ax4.set_title('Night 5 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                    cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            return fig
    
    
        def plot_maximum_relative_humidity_extended_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS THE NWS OVERNIGHT RELATIVE HUMIDITY FORECAST AND THE FORECAST TRENDS OF OVERNIGHT RELATIVE HUMIDITY 
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.relative_humidity_colormap()
            cmap_change = colormaps.relative_humidity_change_colormap()
        
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
    
            lons = lons_1
            lats = lats_1
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
        
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
         
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files == 3:
        
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Night 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files == 4:
        
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Night 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_title('Night 7 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files >= 5:
        
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Night 4 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Night 5 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_title('Night 6 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax4.add_feature(cfeature.STATES, linewidth=0.5)
                ax4.add_feature(USCOUNTIES, linewidth=1.5)
                ax4.set_title('Night 7 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            return fig


        def plot_minimum_relative_humidity_short_term_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS THE NWS FORECAST MINIMUM RELATIVE HUMIDITY AND THE MINIMUM RELATIVE HUMIDITY FORECAST TRENDS
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MIN RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.minrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.minrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.relative_humidity_colormap()
            cmap_change = colormaps.relative_humidity_change_colormap()
        
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
    
            lons = lons_1
            lats = lats_1
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
         
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
             
                if utc_time.hour >= 22 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
                    
                    ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
                
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 22 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files == 4:
    
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 22 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files >= 5:
        
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                    fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax4.add_feature(cfeature.STATES, linewidth=0.5)
                    ax4.add_feature(USCOUNTIES, linewidth=1.5)
                    ax4.set_title('Day 5 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                    cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 22 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax0.add_feature(cfeature.STATES, linewidth=0.5)
                    ax0.add_feature(USCOUNTIES, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax1.add_feature(cfeature.STATES, linewidth=0.5)
                    ax1.add_feature(USCOUNTIES, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax2.add_feature(cfeature.STATES, linewidth=0.5)
                    ax2.add_feature(USCOUNTIES, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                    ax3.add_feature(cfeature.STATES, linewidth=0.5)
                    ax3.add_feature(USCOUNTIES, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            return fig
    
    
        def plot_minimum_relative_humidity_extended_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS THE NWS FORECAST MINIMUM RELATIVE HUMIDITY AND THE MINIMUM RELATIVE HUMIDITY FORECAST TRENDS
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MIN RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, 'ds.minrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, 'ds.minrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.relative_humidity_colormap()
            cmap_change = colormaps.relative_humidity_change_colormap()
        
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
    
            lons = lons_1
            lats = lats_1
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax.add_feature(cfeature.STATES, linewidth=0.5)
                ax.add_feature(USCOUNTIES, linewidth=1.5)
                ax.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
        
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
         
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
             
            if files == 3:
        
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Day 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files == 4:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Day 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_title('Day 7 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files >= 5:
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=0.5)
                ax0.add_feature(USCOUNTIES, linewidth=1.5)
                ax0.set_title('Day 3 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=0.5)
                ax1.add_feature(USCOUNTIES, linewidth=1.5)
                ax1.set_title('Day 4 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=0.5)
                ax2.add_feature(USCOUNTIES, linewidth=1.5)
                ax2.set_title('Day 5 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=0.5)
                ax3.add_feature(USCOUNTIES, linewidth=1.5)
                ax3.set_title('Day 6 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax4.add_feature(cfeature.STATES, linewidth=0.5)
                ax4.add_feature(USCOUNTIES, linewidth=1.5)
                ax4.set_title('Day 7 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            return fig


class Predictive_Services_Areas_Perspective:

    r'''
    THIS CLASS HOSTS A VARIETY OF PLOTTING FUNCTIONS. 

    THESE FUNCTIONS PLOT THE NATIONAL WEATHER SERVICE GRIDDED FORECAST DATA IN VARIOUS DIFFERENT WAYS

    GENERIC FORECAST FUNCTIONS OFFER SLIGHTLY MORE CUSTOMIZATION AS BOTH THE GENERIC FUNCTIONS ARE NOT PRESETS FOR A CERTAIN WEATHER ELEMENT. 

    THIS CLASS PLOTS THE DATA USING PREDICTIVE SERVICES AREAS (PSA) BOUNDARIES AS A REFERENCE POINT. 

    (C) METEOROLOGIST ERIC J. DREWITZ 2023

    '''

    class CONUS:
    
        r'''
        THIS NESTED CLASS HOSTS THE IMAGES FOR CONUS AKA THE "LOWER-48"
        '''


        def plot_relative_humidity_poor_recovery_short_term_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS OF POOR OVERNIGHT RELATIVE HUMIDITY RECOVERY FROM THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
        
        
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')

    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(PSAs, linewidth=1.5)
                ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
         
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
             
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
                    
                    ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=0.70)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                    fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax4.add_feature(PSAs, linewidth=1.5)
                    ax4.set_title('Night 5 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                    cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1),cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig
    
        def plot_relative_humidity_poor_recovery_extended_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS OF POOR OVERNIGHT RELATIVE HUMIDITY RECOVERY FROM THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
        
        
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
            
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(PSAs, linewidth=1.5)
                ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
         
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
        
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=0.70)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5)
                ax3.set_title('Night 7 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 4 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Night 5 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5)
                ax3.set_title('Night 6 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(PSAs, linewidth=1.5)
                ax4.set_title('Night 7 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig
        
        def plot_relative_humidity_excellent_recovery_short_term_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS OF EXCELLENT OVERNIGHT RELATIVE HUMIDITY RECOVERY FROM THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
            
            short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
        
        
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')
            cmap = colormaps.excellent_recovery_colormap()
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(PSAs, linewidth=1.5)
                ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
         
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs) 
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
             
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
                    
                    ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                    fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax4.add_feature(PSAs, linewidth=1.5)
                    ax4.set_title('Night 5 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                    cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig
        
        def plot_relative_humidity_excellent_recovery_extended_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS OF EXCELLENT OVERNIGHT RELATIVE HUMIDITY RECOVERY FROM THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
            
            extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')
            cmap = colormaps.excellent_recovery_colormap()
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
            
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(PSAs, linewidth=1.5)
                ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 18Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
         
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
             
            if files == 3:
        
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5)
                ax3.set_title('Night 7 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 4 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Night 5 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5)
                ax3.set_title('Night 6 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(PSAs, linewidth=1.5)
                ax4.set_title('Night 7 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig
        
        
        
        def plot_red_flag_minimum_relative_humidity_short_term_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS WHERE MINIMUM RELATIVE HUMIDITY IS FORECAST TO MEET AND/OR EXCEED THE RED FLAG WARNING CRITERIA FOR MINIMUM RELATIVE HUMIDITY (MIN RH <= 15%) AND IS BASED ON THE National Weather Service Short-Term Forecast
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MINIMUM RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.minrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.minrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
        
        
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
            
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(PSAs, linewidth=1.5)
                ax.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
         
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
             
                if utc_time.hour > 21 or utc_time.hour <= 6:
        
                    fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
                    
                    ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
        
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
                
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour > 21 or utc_time.hour <= 6:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour > 21 or utc_time.hour <= 6:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                    fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax4.add_feature(PSAs, linewidth=1.5)
                    ax4.set_title('Day 5 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                    cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                if utc_time.hour > 21 or utc_time.hour <= 6:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig
    
    
        def plot_red_flag_minimum_relative_humidity_extended_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS AREAS WHERE MINIMUM RELATIVE HUMIDITY IS FORECAST TO MEET AND/OR EXCEED THE RED FLAG WARNING CRITERIA FOR MINIMUM RELATIVE HUMIDITY (MIN RH <= 15%) AND IS BASED ON THE National Weather Service Extended Forecast
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MINIMUM RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, 'ds.minrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, 'ds.minrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
        
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
            
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(PSAs, linewidth=1.5)
                ax.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
        
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
         
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
        
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Day 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 4:
        
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Day 6 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5)
                ax3.set_title('Day 7 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files >= 5:
        
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Day 3 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Day 4 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Day 5 Forecast\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5)
                ax3.set_title('Day 6 Forecast\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(PSAs, linewidth=1.5)
                ax4.set_title('Day 7 Forecast\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            return fig


        def plot_maximum_relative_humidity_short_term_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS THE NWS OVERNIGHT RELATIVE HUMIDITY FORECAST AND THE FORECAST TRENDS OF OVERNIGHT RELATIVE HUMIDITY 
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')
            cmap = colormaps.relative_humidity_colormap()
            cmap_change = colormaps.relative_humidity_change_colormap()
        
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
    
            lons = lons_1
            lats = lats_1
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(PSAs, linewidth=1.5)
                ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
         
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
             
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
                    
                    ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
                
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files == 4:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files >= 5:
        
                if utc_time.hour >= 18 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                    fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax4.add_feature(PSAs, linewidth=1.5)
                    ax4.set_title('Night 5 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                    cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 6 and utc_time.hour < 18:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            return fig
    
    
        def plot_maximum_relative_humidity_extended_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS THE NWS OVERNIGHT RELATIVE HUMIDITY FORECAST AND THE FORECAST TRENDS OF OVERNIGHT RELATIVE HUMIDITY 
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAX RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, 'ds.maxrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, 'ds.maxrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')
            cmap = colormaps.relative_humidity_colormap()
            cmap_change = colormaps.relative_humidity_change_colormap()
        
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
    
            lons = lons_1
            lats = lats_1
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(PSAs, linewidth=1.5)
                ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
        
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
         
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files == 3:
        
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Night 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files == 4:
        
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Night 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5)
                ax3.set_title('Night 7 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files >= 5:
        
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Night 4 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Night 5 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5)
                ax3.set_title('Night 6 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(PSAs, linewidth=1.5)
                ax4.set_title('Night 7 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            return fig


        def plot_minimum_relative_humidity_short_term_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS THE NWS FORECAST MINIMUM RELATIVE HUMIDITY AND THE MINIMUM RELATIVE HUMIDITY FORECAST TRENDS
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MIN RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.minrh.bin')
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.minrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')

            cmap = colormaps.relative_humidity_colormap()
            cmap_change = colormaps.relative_humidity_change_colormap()
        
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
    
            lons = lons_1
            lats = lats_1
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(PSAs, linewidth=1.5)
                ax.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
                
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
         
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
             
                if utc_time.hour >= 22 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
                    
                    ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 3:
                
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 22 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                    fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files == 4:
    
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap='BrBG', transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 22 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                    fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                    ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files >= 5:
        
                if utc_time.hour > 6 and utc_time.hour <= 21:
        
                    fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                    fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax4.add_feature(PSAs, linewidth=1.5)
                    ax4.set_title('Day 5 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                    cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                if utc_time.hour >= 22 or utc_time.hour < 6:
        
                    fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                    fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                    fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                    ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                    ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax0.add_feature(PSAs, linewidth=1.5)
                    ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                    cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                    cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                    ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax1.add_feature(PSAs, linewidth=1.5)
                    ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                    cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax2.add_feature(PSAs, linewidth=1.5)
                    ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                    cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                    ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                    ax3.add_feature(PSAs, linewidth=1.5)
                    ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                    cs3 = ax3.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                    cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                    cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            return fig
    
    
        def plot_minimum_relative_humidity_extended_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink): 
        
            r'''
            THIS FUNCTION PLOTS THE NWS FORECAST MINIMUM RELATIVE HUMIDITY AND THE MINIMUM RELATIVE HUMIDITY FORECAST TRENDS
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MIN RELATIVE HUMIDITY GRIDS
        
            THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
            1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
            2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
        
            PYTHON MODULE DEPENDENCIES:
            1. CARTOPY
            2. METPY
            3. NUMPY
            4. MATPLOTLIB
        
            COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
            '''
        
            extended_data = da.FTP_Downloads.get_NWS_NDFD_extended_grid_data(directory_name, 'ds.minrh.bin')

            cmap = colormaps.relative_humidity_colormap()
            cmap_change = colormaps.relative_humidity_change_colormap()
            
            first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(extended_data, 'ds.minrh.bin')
        
            local_time, utc_time = standard.plot_creation_time()
            grid_time_interval = 12
            
            files = count_of_GRIB_files
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')
        
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
    
            lons = lons_1
            lats = lats_1
           
            if files == 1:
        
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
                
                ax = plt.subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(PSAs, linewidth=1.5)
                ax.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
        
                cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar = fig.colorbar(cs, shrink=color_table_shrink)
                cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            if files == 2:
        
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
         
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
             
            if files == 3:
        
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Day 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files == 4:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Day 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5)
                ax3.set_title('Day 7 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            if files >= 5:
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
        
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5)
                ax0.set_title('Day 3 Forecast\nStart: ' + grb_1_start.strftime('%m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y 06Z'), fontweight='bold')
            
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
            
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5)
                ax1.set_title('Day 4 Forecast Trend\nStart: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5)
                ax2.set_title('Day 5 Forecast Trend\nStart: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5)
                ax3.set_title('Day 6 Forecast Trend\nStart: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
            
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(PSAs, linewidth=1.5)
                ax4.set_title('Day 7 Forecast Trend\nStart: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
            
                cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            return fig

