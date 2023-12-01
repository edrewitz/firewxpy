# THIS SCRIPT PLOTS VARIOUS DATASETS THROUGH VARIOUS DIFFERENT FUNCTIONS
#
# THIS IS THE NWS FTP DATA ACCESS FILE FOR FIREPY
#
# DEPENDENCIES INCLUDE:
# 1. MATPLOTLIB
# 2. DATETIME
# 3. PYTZ
# 4. CARTOPY
# 5. METPY
#
#  (C) ERIC J. DREWITZ
#       METEOROLOGIST
#         USDA/USFS

#### IMPORTS ####
from datetime import datetime, timedelta
import pytz
import matplotlib.pyplot as plt
from metpy.plots import colortables
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
from metpy.plots import USCOUNTIES
import numpy as np

def plot_creation_time():
    '''
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


def plot_NWS_forecast(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, local_time, utc_time, grid_time_interval, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, color_table, color_table_start, color_table_stop, color_table_step): 

    '''
    THIS FUNCTION MAKES A GENERIC CUSTOMIZED PLOT OF THE LATEST NOAA/NWS NDFD GRID FORECAST DATA

    THE FOLLOWING IS CUSTOMIZABLE BY THE USER:
    1. LATITUDE/LONGITUDE BOUNDS OF THE PLOT
    2. CENTRAL LATITUDE/LONGITUDE AND STANDARD PARALLELS FOR PLOT
    3. WEATHER PARAMETER 
    4. COLOR TABLE FOR PLOT 
    5. COLOR TABLE START, STOP AND STEP
    6. GRID TIME INTERVALS IN HOURS (DIFFERENT GRIDS ARE DIFFERENT LENGTHS IN TIME)

    PYTHON MODULE DEPENDENCIES:
    1. CARTOPY
    2. METPY
    3. NUMPY
    4. MATPLOTLIB

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
    '''

    files = count_of_GRIB_files
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()
    
   
    if files == 1:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        lats, lons = first_GRIB_file.latlons()

        fig = plt.figure(figsize=(10,10))
        fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
        fig.suptitle("National Weather Service Forecast", fontweight='bold')
        
        ax = plt.subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.STATES, linewidth=0.5)
        ax.add_feature(USCOUNTIES, linewidth=0.75)
        ax.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar = fig.colorbar(cs, shrink=0.80)

    if files == 2:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()

        fig = plt.figure(figsize=(9,5))
        fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
        fig.suptitle("National Weather Service Forecast", fontweight='bold')
        
        ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
        ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax0.add_feature(cfeature.STATES, linewidth=0.5)
        ax0.add_feature(USCOUNTIES, linewidth=0.75)
        ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar0 = fig.colorbar(cs0, shrink=0.80)

        ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.STATES, linewidth=0.5)
        ax1.add_feature(USCOUNTIES, linewidth=0.75)
        ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar1 = fig.colorbar(cs1, shrink=0.80)

    if files == 3:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
        
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()

        fig = plt.figure(figsize=(15,5))
        fig.text(0.26, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
        fig.suptitle("National Weather Service Forecast", fontweight='bold')
        
        ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
        ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax0.add_feature(cfeature.STATES, linewidth=0.5)
        ax0.add_feature(USCOUNTIES, linewidth=0.75)
        ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar0 = fig.colorbar(cs0, shrink=0.80)

        ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.STATES, linewidth=0.5)
        ax1.add_feature(USCOUNTIES, linewidth=0.75)
        ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar1 = fig.colorbar(cs1, shrink=0.80)

        ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax2.add_feature(cfeature.STATES, linewidth=0.5)
        ax2.add_feature(USCOUNTIES, linewidth=0.75)
        ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar2 = fig.colorbar(cs2, shrink=0.80)

    if files == 4:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
        grb_4_vals = fourth_GRIB_file.values
        grb_4_start = fourth_GRIB_file.validDate
        grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
        
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        lats_4, lons_4 = fourth_GRIB_file.latlons()

        fig = plt.figure(figsize=(12,10))
        fig.text(0.33, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
        fig.suptitle("National Weather Service Forecast", fontweight='bold')
        
        ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
        ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax0.add_feature(cfeature.STATES, linewidth=0.5)
        ax0.add_feature(USCOUNTIES, linewidth=0.75)
        ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar0 = fig.colorbar(cs0, shrink=0.80)

        ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.STATES, linewidth=0.5)
        ax1.add_feature(USCOUNTIES, linewidth=0.75)
        ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar1 = fig.colorbar(cs1, shrink=0.80)

        ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax2.add_feature(cfeature.STATES, linewidth=0.5)
        ax2.add_feature(USCOUNTIES, linewidth=0.75)
        ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar2 = fig.colorbar(cs2, shrink=0.80)

        ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax3.add_feature(cfeature.STATES, linewidth=0.5)
        ax3.add_feature(USCOUNTIES, linewidth=0.75)
        ax3.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar3 = fig.colorbar(cs3, shrink=0.80) 

    if files >= 5:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
        grb_4_vals = fourth_GRIB_file.values
        grb_4_start = fourth_GRIB_file.validDate
        grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
        grb_5_vals = fifth_GRIB_file.values
        grb_5_start = fifth_GRIB_file.validDate
        grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
          
        
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        lats_4, lons_4 = fourth_GRIB_file.latlons()
        lats_5, lons_5 = fifth_GRIB_file.latlons()

        fig = plt.figure(figsize=(25,5))
        fig.text(0.40, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
        fig.suptitle("National Weather Service Forecast", fontweight='bold')
        
        ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
        ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax0.add_feature(cfeature.STATES, linewidth=0.5)
        ax0.add_feature(USCOUNTIES, linewidth=0.75)
        ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar0 = fig.colorbar(cs0, shrink=0.80)

        ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax1.add_feature(cfeature.STATES, linewidth=0.5)
        ax1.add_feature(USCOUNTIES, linewidth=0.75)
        ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar1 = fig.colorbar(cs1, shrink=0.80)

        ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax2.add_feature(cfeature.STATES, linewidth=0.5)
        ax2.add_feature(USCOUNTIES, linewidth=0.75)
        ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar2 = fig.colorbar(cs2, shrink=0.80)

        ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax3.add_feature(cfeature.STATES, linewidth=0.5)
        ax3.add_feature(USCOUNTIES, linewidth=0.75)
        ax3.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar3 = fig.colorbar(cs3, shrink=0.80)

        ax4 = plt.subplot(1, 5, 4, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax4.add_feature(cfeature.STATES, linewidth=0.5)
        ax4.add_feature(USCOUNTIES, linewidth=0.75)
        ax4.set_title('Start: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, transform=datacrs)
        cbar4 = fig.colorbar(cs4, shrink=0.80) 

    return fig


def plot_NWS_poor_RH_recovery_forecast(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, local_time, utc_time, grid_time_interval, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel): 

    '''
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

    files = count_of_GRIB_files
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()
    
   
    if files == 1:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        lats, lons = first_GRIB_file.latlons()

        fig = plt.figure(figsize=(10,10))
        fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
        fig.suptitle("National Weather Service Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
        
        ax = plt.subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.STATES, linewidth=0.5)
        ax.add_feature(USCOUNTIES, linewidth=0.75)
        ax.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
        cbar = fig.colorbar(cs, shrink=0.80)
        cbar.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files == 2:
       
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
            
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        
        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
 
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
     
        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(10,10))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
            
            ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files == 3:

        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
            
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        
        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(15,6))
            fig.text(0.26, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')

        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')

            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files == 4:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
        grb_4_vals = fourth_GRIB_file.values
        grb_4_start = fourth_GRIB_file.validDate
        grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
        
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        lats_4, lons_4 = fourth_GRIB_file.latlons()

        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(12,10))
            fig.text(0.33, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')

            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=0.80) 
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')

        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(15,6))
            fig.text(0.26, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')

            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files >= 5:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
        grb_4_vals = fourth_GRIB_file.values
        grb_4_start = fourth_GRIB_file.validDate
        grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
        grb_5_vals = fifth_GRIB_file.values
        grb_5_start = fifth_GRIB_file.validDate
        grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
          
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        lats_4, lons_4 = fourth_GRIB_file.latlons()
        lats_5, lons_5 = fifth_GRIB_file.latlons()

        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(25,5))
            fig.text(0.40, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')

            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=0.80)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax4 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=0.5)
            ax4.add_feature(USCOUNTIES, linewidth=0.75)
            ax4.set_title('Start: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar4 = fig.colorbar(cs4, shrink=0.80)
            cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')

        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(12,10))
            fig.text(0.33, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')

            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=0.80)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')

    return fig


def plot_NWS_excellent_RH_recovery_forecast(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, local_time, utc_time, grid_time_interval, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel): 

    '''
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

    files = count_of_GRIB_files
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()
    
   
    if files == 1:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        lats, lons = first_GRIB_file.latlons()

        fig = plt.figure(figsize=(10,10))
        fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
        fig.suptitle("National Weather Service Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
        
        ax = plt.subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.STATES, linewidth=0.5)
        ax.add_feature(USCOUNTIES, linewidth=0.75)
        ax.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
        cbar = fig.colorbar(cs, shrink=0.80)
        cbar.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files == 2:
       
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
            
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        
        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
 
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
     
        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(10,10))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
            
            ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files == 3:

        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
            
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        
        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(15,6))
            fig.text(0.26, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')

        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')

            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files == 4:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
        grb_4_vals = fourth_GRIB_file.values
        grb_4_start = fourth_GRIB_file.validDate
        grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
        
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        lats_4, lons_4 = fourth_GRIB_file.latlons()

        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(12,10))
            fig.text(0.33, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')

            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=0.80)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')

        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(15,6))
            fig.text(0.26, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')

            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files >= 5:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
        grb_4_vals = fourth_GRIB_file.values
        grb_4_start = fourth_GRIB_file.validDate
        grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
        grb_5_vals = fifth_GRIB_file.values
        grb_5_start = fifth_GRIB_file.validDate
        grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
          
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        lats_4, lons_4 = fourth_GRIB_file.latlons()
        lats_5, lons_5 = fifth_GRIB_file.latlons()

        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(25,5))
            fig.text(0.40, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')

            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=0.80)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax4 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=0.5)
            ax4.add_feature(USCOUNTIES, linewidth=0.75)
            ax4.set_title('Start: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar4 = fig.colorbar(cs4, shrink=0.80)
            cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')

        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(12,10))
            fig.text(0.33, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')

            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(80, 101, 1), cmap='Greens', transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=0.80)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')

    return fig






def plot_NWS_red_flag_min_rh_forecast(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, local_time, utc_time, grid_time_interval, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel): 

    '''
    THIS FUNCTION PLOTS AREAS WHERE MINIMUM RELATIVE HUMIDITY IS FORECAST TO MEET AND/OR EXCEED THE RED FLAG WARNING CRITERIA FOR MINIMUM RELATIVE HUMIDITY (MIN RH <= 15%) AND IS BASED ON THE NATIONAL WEATHER SERVICE FORECAST

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

    files = count_of_GRIB_files
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()
    
   
    if files == 1:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        lats, lons = first_GRIB_file.latlons()

        fig = plt.figure(figsize=(10,10))
        fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
        fig.suptitle("National Weather Service Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
        
        ax = plt.subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.STATES, linewidth=0.5)
        ax.add_feature(USCOUNTIES, linewidth=0.75)
        ax.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
        cbar = fig.colorbar(cs, shrink=0.80)
        cbar.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files == 2:
       
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
            
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        
        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
 
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
     
        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(10,10))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
            
            ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files == 3:

        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
            
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        
        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(15,5))
            fig.text(0.26, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')

        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')

            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files == 4:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
        grb_4_vals = fourth_GRIB_file.values
        grb_4_start = fourth_GRIB_file.validDate
        grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
        
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        lats_4, lons_4 = fourth_GRIB_file.latlons()

        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(12,10))
            fig.text(0.33, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')

            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=0.80)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')

        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(15,5))
            fig.text(0.26, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')

            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')

    if files >= 5:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
        grb_4_vals = fourth_GRIB_file.values
        grb_4_start = fourth_GRIB_file.validDate
        grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
        grb_5_vals = fifth_GRIB_file.values
        grb_5_start = fifth_GRIB_file.validDate
        grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
          
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        lats_4, lons_4 = fourth_GRIB_file.latlons()
        lats_5, lons_5 = fifth_GRIB_file.latlons()

        if utc_time.hour > 6 and utc_time.hour <= 18:

            fig = plt.figure(figsize=(25,5))
            fig.text(0.40, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')

            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=0.80)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax4 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=0.5)
            ax4.add_feature(USCOUNTIES, linewidth=0.75)
            ax4.set_title('Start: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar4 = fig.colorbar(cs4, shrink=0.80)
            cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')

        if utc_time.hour > 18 or utc_time.hour <= 6:

            fig = plt.figure(figsize=(12,10))
            fig.text(0.33, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')

            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=0.80)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')

    return fig


def plot_NWS_extreme_heat_forecast(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, local_time, utc_time, grid_time_interval, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel): 

    '''
    THIS FUNCTION PLOTS AREAS WHERE THERE IS EXTREME HEAT IN THE FORECAST. DURING THE WARM SEASON (APRIL - OCTOBER) EXTREME HEAT IS DEFINED AS THE MAXIMUM TEMPERATURE >= 120F AND COLD SEASON (NOVEMBER - MARCH) MAXIMUM TEMPERATURE >= 100F AND IS BASED ON THE NATIONAL WEATHER SERVICE FORECAST

    IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE MAXIMUM TEMPERATURE GRIDS

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

    files = count_of_GRIB_files
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()
    
   
    if files == 1:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        
        lats, lons = first_GRIB_file.latlons()

        fig = plt.figure(figsize=(10,10))
        fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')

        if utc_time.month >= 4 and utc_month <= 10:
            fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 120 \N{DEGREE SIGN}F)", fontweight='bold')

        if utc_time.month >= 11 or utc_month <= 3:
            fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)", fontweight='bold')
        
        ax = plt.subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.STATES, linewidth=0.5)
        ax.add_feature(USCOUNTIES, linewidth=0.75)
        ax.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

        if utc_time.month >= 4 and utc_month <= 10:
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

        if utc_time.month >= 11 or utc_month <= 3:
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
            
        cbar = fig.colorbar(cs, shrink=0.80)
        cbar.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')

    if files == 2:
       
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
            
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        
        if utc_time.hour >= 0 and utc_time.hour < 19:

            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            
            if utc_time.month >= 4 and utc_month <= 10:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 120 \N{DEGREE SIGN}F)", fontweight='bold')

            if utc_time.month >= 11 or utc_month <= 3:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)", fontweight='bold')
 
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
     
        if utc_time.hour >= 19 and utc_time.hour < 24:

            fig = plt.figure(figsize=(10,10))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            
            if utc_time.month >= 4 and utc_month <= 10:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 120 \N{DEGREE SIGN}F)", fontweight='bold')

            if utc_time.month >= 11 or utc_month <= 3:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)", fontweight='bold')
            
            ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')

            if utc_time.month >= 4 and utc_month <= 10:
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')

    if files == 3:

        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
            
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        
        if utc_time.hour >= 0 and utc_time.hour < 19:

            fig = plt.figure(figsize=(15,5))
            fig.text(0.26, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            
            if utc_time.month >= 4 and utc_month <= 10:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 120 \N{DEGREE SIGN}F)", fontweight='bold')

            if utc_time.month >= 11 or utc_month <= 3:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)", fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')

        if utc_time.hour >= 19 and utc_time.hour < 24:

            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            
            if utc_time.month >= 4 and utc_month <= 10:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 120 \N{DEGREE SIGN}F)", fontweight='bold')

            if utc_time.month >= 11 or utc_month <= 3:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)", fontweight='bold')

            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')

    if files == 4:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
        grb_4_vals = fourth_GRIB_file.values
        grb_4_start = fourth_GRIB_file.validDate
        grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
        
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        lats_4, lons_4 = fourth_GRIB_file.latlons()

        if utc_time.hour >= 0 and utc_time.hour < 19:

            fig = plt.figure(figsize=(12,10))
            fig.text(0.33, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            
            if utc_time.month >= 4 and utc_month <= 10:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 120 \N{DEGREE SIGN}F)", fontweight='bold')

            if utc_time.month >= 11 or utc_month <= 3:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)", fontweight='bold')

            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar3 = fig.colorbar(cs3, shrink=0.80)
            cbar3.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')

        if utc_time.hour >= 19 and utc_time.hour < 24:

            fig = plt.figure(figsize=(15,5))
            fig.text(0.26, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            
            if utc_time.month >= 4 and utc_month <= 10:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 120 \N{DEGREE SIGN}F)", fontweight='bold')

            if utc_time.month >= 11 or utc_month <= 3:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)", fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')

            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')

    if files >= 5:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
        grb_3_vals = third_GRIB_file.values
        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
        grb_4_vals = fourth_GRIB_file.values
        grb_4_start = fourth_GRIB_file.validDate
        grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
        grb_5_vals = fifth_GRIB_file.values
        grb_5_start = fifth_GRIB_file.validDate
        grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
          
        lats_1, lons_1 = first_GRIB_file.latlons()
        lats_2, lons_2 = second_GRIB_file.latlons()
        lats_3, lons_3 = third_GRIB_file.latlons()
        lats_4, lons_4 = fourth_GRIB_file.latlons()
        lats_5, lons_5 = fifth_GRIB_file.latlons()

        if utc_time.hour >= 0 and utc_time.hour < 19:

            fig = plt.figure(figsize=(25,5))
            fig.text(0.40, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            
            if utc_time.month >= 4 and utc_month <= 10:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 120 \N{DEGREE SIGN}F)", fontweight='bold')

            if utc_time.month >= 11 or utc_month <= 3:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)", fontweight='bold')

            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar3 = fig.colorbar(cs3, shrink=0.80)
            cbar3.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax4 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=0.5)
            ax4.add_feature(USCOUNTIES, linewidth=0.75)
            ax4.set_title('Start: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar4 = fig.colorbar(cs4, shrink=0.80)
            cbar4.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')

        if utc_time.hour >= 19 and utc_time.hour < 24:

            fig = plt.figure(figsize=(12,10))
            fig.text(0.33, 0.08, 'Plot Created With FirePY (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontweight='bold')
            
            if utc_time.month >= 4 and utc_month <= 10:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 120 \N{DEGREE SIGN}F)", fontweight='bold')

            if utc_time.month >= 11 or utc_month <= 3:
                fig.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)", fontweight='bold')

            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=0.5)
            ax0.add_feature(USCOUNTIES, linewidth=0.75)
            ax0.set_title('Start: ' + grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, shrink=0.80)
            cbar0.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Start: ' + grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar1 = fig.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Start: ' + grb_4_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar2 = fig.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=0.5)
            ax3.add_feature(USCOUNTIES, linewidth=0.75)
            ax3.set_title('Start: ' + grb_5_start.strftime('%m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_month <= 10:
                cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(120, 140, 5), cmap='hot', transform=datacrs)

            if utc_time.month >= 11 or utc_month <= 3:
                cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(100, 130, 5), cmap='hot', transform=datacrs)
                
            cbar3 = fig.colorbar(cs3, shrink=0.80)
            cbar3.set_label(label="Maximum Temperature (N{DEGREE SIGN}F)", fontweight='bold')

    return fig
