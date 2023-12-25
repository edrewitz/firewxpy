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
from NWS_Generic_Forecast_Graphics import standard


class Counties_Perspective:

    def plot_SPC_critical_fire_weather_risk_outlook_states_with_counties(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink):
    
        r'''
        THIS FUNCTION PLOTS THE NOAA/NWS STORM PREDICTION CENTER'S CRITICAL FIRE WEATHER RISK OUTLOOK
    
        ALTHOUGH THE BOUNDS OF THE PLOT ARE CUSTOMIZED BY THE USER, THE RECOMMENDED SETTING TO CAPTURE CONUS IS:
    
        NORTH = 51
        SOUTH = 20
        EAST = -65
        WEST = -125 
    
        THIS PRODUCT IS NOT AVAILABLE FOR ALASKA OR HAWAII
    
        RETURNS: FIGURES SHOWING THE SPC CRITICAL FIRE WEATHER RISK FOR EACH DAY
    
        PYTHON PACKAGE DEPENDENCIES:
        1) MATPLOTLIB
        2) PYGRIB
        3) NUMPY
        4) CARTOPY
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023    
        '''
        
        short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.critfireo.bin')
            
        first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.critfireo.bin')
        
        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 12
            
        files = count_of_GRIB_files
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()
        
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.critfireo.bin')
    
        ####################################
        ##### DAY 1 FIGURE #################
        ####################################
        if files == 1:
            
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.88, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=0.75)
            ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
    
            fig1 = None
            fig2 = None
        
        ####################################
        ##### DAY 2 FIGURE #################
        ####################################    
        if files == 2:
    
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.88, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=0.75)
            ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig1 = plt.figure(figsize=(9,5))
            fig1.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig1.text(0.60, 0.88, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_2_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar1 = fig1.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Critical Fire Weather Risk", fontweight='bold')
    
            fig3 = None
            
        ####################################
        ##### DAY 3 FIGURE #################
        ####################################     
        if files == 3:
    
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=0.75)
            ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig1 = plt.figure(figsize=(9,5))
            fig1.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig1.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_2_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar1 = fig1.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig2 = plt.figure(figsize=(9,5))
            fig2.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig2.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.add_feature(USCOUNTIES, linewidth=0.75)
            ax2.set_title('Critical Fire Wx Forecast (Days 3-8)\nStart: '+ grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_3_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar2 = fig2.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Critical Fire Weather Risk", fontweight='bold')
    
        if files > 3:
    
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=0.75)
            ax.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig1 = plt.figure(figsize=(9,5))
            fig1.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig1.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.add_feature(USCOUNTIES, linewidth=0.75)
            ax1.set_title('Critical Fire Wx Forecast (Days 3-8)\nStart: '+ grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_2_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar1 = fig1.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig2 = None
    
        return fig, fig1, fig2


    def plot_SPC_critical_fire_weather_risk_outlook_states_only(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink):
    
        r'''
        THIS FUNCTION PLOTS THE NOAA/NWS STORM PREDICTION CENTER'S CRITICAL FIRE WEATHER RISK OUTLOOK
    
        ALTHOUGH THE BOUNDS OF THE PLOT ARE CUSTOMIZED BY THE USER, THE RECOMMENDED SETTING TO CAPTURE CONUS IS:
    
        NORTH = 51
        SOUTH = 20
        EAST = -65
        WEST = -125 
    
        THIS PRODUCT IS NOT AVAILABLE FOR ALASKA OR HAWAII
    
        RETURNS: FIGURES SHOWING THE SPC CRITICAL FIRE WEATHER RISK FOR EACH DAY
    
        PYTHON PACKAGE DEPENDENCIES:
        1) MATPLOTLIB
        2) PYGRIB
        3) NUMPY
        4) CARTOPY
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023    
        '''
        
        short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.critfireo.bin')
            
        first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.critfireo.bin')
        
        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 12
            
        files = count_of_GRIB_files
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()
        
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.critfireo.bin')
    
        ####################################
        ##### DAY 1 FIGURE #################
        ####################################
        if files == 1:
            
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.88, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
    
            fig1 = None
            fig2 = None
        
        ####################################
        ##### DAY 2 FIGURE #################
        ####################################    
        if files == 2:
    
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.88, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig1 = plt.figure(figsize=(9,5))
            fig1.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig1.text(0.60, 0.88, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_2_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar1 = fig1.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Critical Fire Weather Risk", fontweight='bold')
    
            fig3 = None
            
        ####################################
        ##### DAY 3 FIGURE #################
        ####################################     
        if files == 3:
    
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig1 = plt.figure(figsize=(9,5))
            fig1.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig1.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_2_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar1 = fig1.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig2 = plt.figure(figsize=(9,5))
            fig2.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig2.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=0.5)
            ax2.set_title('Critical Fire Wx Forecast (Days 3-8)\nStart: '+ grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_3_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar2 = fig2.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Critical Fire Weather Risk", fontweight='bold')
    
        if files > 3:
    
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig1 = plt.figure(figsize=(9,5))
            fig1.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig1.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=0.5)
            ax1.set_title('Critical Fire Wx Forecast (Days 3-8)\nStart: '+ grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_2_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar1 = fig1.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig2 = None
    
        return fig, fig1, fig2




class Predictive_Services_Areas_Perspective:


    def plot_SPC_critical_fire_weather_risk_outlook_predictive_services_areas(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink):
    
        r'''
        THIS FUNCTION PLOTS THE NOAA/NWS STORM PREDICTION CENTER'S CRITICAL FIRE WEATHER RISK OUTLOOK
    
        ALTHOUGH THE BOUNDS OF THE PLOT ARE CUSTOMIZED BY THE USER, THE RECOMMENDED SETTING TO CAPTURE CONUS IS:
    
        NORTH = 51
        SOUTH = 20
        EAST = -65
        WEST = -125 
    
        THIS PRODUCT IS NOT AVAILABLE FOR ALASKA OR HAWAII
    
        RETURNS: FIGURES SHOWING THE SPC CRITICAL FIRE WEATHER RISK FOR EACH DAY
    
        PYTHON PACKAGE DEPENDENCIES:
        1) MATPLOTLIB
        2) PYGRIB
        3) NUMPY
        4) CARTOPY
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023    
        '''
        
        short_term_data = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data(directory_name, 'ds.critfireo.bin')
            
        first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files = parsers.NDFD.sort_GRIB_files(short_term_data, 'ds.critfireo.bin')
        
        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 12
            
        files = count_of_GRIB_files
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')
        
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.critfireo.bin')
    
        ####################################
        ##### DAY 1 FIGURE #################
        ####################################
        if files == 1:
            
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.88, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=0.75)
            ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
    
            fig1 = None
            fig2 = None
        
        ####################################
        ##### DAY 2 FIGURE #################
        ####################################    
        if files == 2:
    
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.88, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=0.75)
            ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig1 = plt.figure(figsize=(9,5))
            fig1.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig1.text(0.60, 0.88, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=0.75)
            ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_2_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar1 = fig1.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Critical Fire Weather Risk", fontweight='bold')
    
            fig3 = None
            
        ####################################
        ##### DAY 3 FIGURE #################
        ####################################     
        if files == 3:
    
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=0.75)
            ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig1 = plt.figure(figsize=(9,5))
            fig1.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig1.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=0.75)
            ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_2_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar1 = fig1.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig2 = plt.figure(figsize=(9,5))
            fig2.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig2.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=0.75)
            ax2.set_title('Critical Fire Wx Forecast (Days 3-8)\nStart: '+ grb_3_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_3_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar2 = fig2.colorbar(cs2, shrink=0.80)
            cbar2.set_label(label="Critical Fire Weather Risk", fontweight='bold')
    
        if files > 3:
    
            fig = plt.figure(figsize=(9,5))
            fig.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=0.75)
            ax.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_1_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_1_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar = fig.colorbar(cs, shrink=0.80)
            cbar.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig1 = plt.figure(figsize=(9,5))
            fig1.text(0.13, 0.06, 'Developed by: Eric Drewitz - Powered by MetPy | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            fig1.text(0.60, 0.85, 'Risk Index\n4-6 (Yellow) - Elevated\n6-8 (Orange) - Critical\n8-10 (Red) - Extreme', fontsize=8, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=0.75)
            ax1.set_title('Critical Fire Wx Forecast (Days 3-8)\nStart: '+ grb_2_start.strftime('%m/%d/%Y %HZ') + '\nEnd:'+ grb_2_end.strftime('%m/%d/%Y %HZ'), fontsize=10, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            cbar1 = fig1.colorbar(cs1, shrink=0.80)
            cbar1.set_label(label="Critical Fire Weather Risk", fontweight='bold')
            
            fig2 = None
    
        return fig, fig1, fig2
