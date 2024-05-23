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
from dateutil import tz
from calc import unit_conversion
from metpy.units import units

class Counties_Perspective:

    r'''
    This class hosts the National Weather Service Temperature forecast graphics using state and county borders as 
    the geographic reference. 

    '''

    class data_download_included_in_function:

        r'''
        This class hosts functions that include the data download within the function. Each time the function is called the data is downloaded and plots onto the map. 

        This is the recommended class for users who want to make a small amount of images. 

        If the user wants to make a large volume of images, please see the data_download_not_included_in_function class so that the user will only need to download the data once (download the data in the file that is automated before calling the plotting function) to maximize efficiency and execution time. 

        '''

        def plot_extreme_heat_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, show_counties, state_linewidth, county_linewidth): 
        
            r'''
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
            
            directory_name = directory_name
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
    
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxt.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
    
        def plot_frost_freeze_forecast(directory_name, temperature_bottom_bound, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, temp_scale_step, show_rivers, show_counties, state_linewidth, county_linewidth): 
        
            r'''
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
            
            directory_name = directory_name
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temperature_bottom_bound = temperature_bottom_bound
            temp_scale_step = temp_scale_step
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
    
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            cmap = colormaps.cool_temperatures_colormap()
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.mint.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 5]", fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig6.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                fig7.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
    
        def plot_maximum_temperature_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, show_counties, state_linewidth, county_linewidth): 
        
            r'''
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
            
            directory_name = directory_name
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
    
            cmap = colormaps.temperature_colormap()
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxt.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
        def plot_minimum_temperature_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, show_counties, state_linewidth, county_linewidth): 
        
            r'''
            THIS FUNCTION PLOTS AREAS WHERE THERE IS EXTREME HEAT IN THE FORECAST. DURING THE WARM SEASON (APRIL - OCTOBER) EXTREME HEAT IS DEFINED AS THE Minimum Temperature >= 120F AND COLD SEASON (NOVEMBER - MARCH) Minimum Temperature >= 100F AND IS BASED ON THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE Minimum Temperature GRIDS
        
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
            
            directory_name = directory_name
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
    
            cmap = colormaps.temperature_colormap()
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.mint.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs 
    
    
        def plot_NWS_Nights_2_through_7_minimum_temperature_trends(directory_name, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth, color_table_shrink, colorbar_fontsize):
    
            r'''
            This function plots the latest available NOAA/NWS Maximum RH Trend Forecast. 
    
            Inputs: 1) directory_name (String) - File path on the NWS FTP server to the file being downloaded. 
                       (example for Pacific Southwest the directory_name is: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
    
                    2) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.
    
                    3) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.
    
                    4) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.
    
                    5) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.
    
                    6) central_longitude (Integer or Float) - The central longitude. Defaults to -96.
    
                    7) central_latitude (Integer or Float) - The central latitude. Defaults to 39.
    
                    8) first_standard_parallel (Integer or Float) - Southern standard parallel. 
    
                    9) second_standard_parallel (Integer or Float) - Northern standard parallel. 
                    
                    10) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
    
                    11) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
    
                    12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
                    13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
                    14) key_x_position (Integer or Float) - The x-position of the colortable key. 
    
                    15) key_y_position (Integer or Float) - The y-position of the colortable key. 
    
                    16) subplot_title_fontsize (Integer) - The fontsize of the plot title. 
    
                    17) signature_fontsize (Integer) - The fontsize of the signature. 
    
                    18) key_fontsize (Integer) - The fontsize of the key. 
    
                    19) show_counties (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    
                    20) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 
                    21) state_linewidth (Integer) - Width of the state borders. 
    
                    22) county_linewidth (Integer) - Width of the county borders.
    
            Return: A list of figures for each forecast day. 
            '''
    
    
            local_time, utc_time = standard.plot_creation_time()
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
            contour_step = contour_step
    
            cmap = colormaps.relative_humidity_change_colormap()
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
                
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.mint.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, False)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
    
            diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
            diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
            diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
            diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
            diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
            if test_7 == True:
                diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
            else:
                pass
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 2]', fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 3]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 4]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
    
            return figs
    
    
        def plot_NWS_Days_2_through_7_maximum_temperature_trends(directory_name, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth, color_table_shrink, colorbar_fontsize):
    
            r'''
            This function plots the latest available NOAA/NWS Maximum RH Trend Forecast. 
    
            Inputs: 1) directory_name (String) - File path on the NWS FTP server to the file being downloaded. 
                       (example for Pacific Southwest the directory_name is: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
    
                    2) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.
    
                    3) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.
    
                    4) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.
    
                    5) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.
    
                    6) central_longitude (Integer or Float) - The central longitude. Defaults to -96.
    
                    7) central_latitude (Integer or Float) - The central latitude. Defaults to 39.
    
                    8) first_standard_parallel (Integer or Float) - Southern standard parallel. 
    
                    9) second_standard_parallel (Integer or Float) - Northern standard parallel. 
                    
                    10) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
    
                    11) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
    
                    12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
                    13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
                    14) key_x_position (Integer or Float) - The x-position of the colortable key. 
    
                    15) key_y_position (Integer or Float) - The y-position of the colortable key. 
    
                    16) subplot_title_fontsize (Integer) - The fontsize of the plot title. 
    
                    17) signature_fontsize (Integer) - The fontsize of the signature. 
    
                    18) key_fontsize (Integer) - The fontsize of the key. 
    
                    19) show_counties (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    
                    20) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 
                    21) state_linewidth (Integer) - Width of the state borders. 
    
                    22) county_linewidth (Integer) - Width of the county borders.
    
            Return: A list of figures for each forecast day. 
            '''
    
            local_time, utc_time = standard.plot_creation_time()
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
            contour_step = contour_step
    
            cmap = colormaps.relative_humidity_change_colormap()
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
                
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxt.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, False)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
            diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
            diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
            diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
            diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
            if test_7 == True:
                diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
            else:
                pass


            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 2]', fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 3]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 4]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
    
            return figs


    class data_download_not_included_in_function:

        r'''
        This class hosts functions that do not include the data download within the function. 

        This is the recommended class for users who want to make a large amount of images so that minimal data downloads are needed. 

        '''

        def plot_extreme_heat_forecast(file_path, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, show_counties, state_linewidth, county_linewidth): 
        
            r'''
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
            
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
    
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
    
        def plot_frost_freeze_forecast(file_path, temperature_bottom_bound, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, temp_scale_step, show_rivers, show_counties, state_linewidth, county_linewidth): 
        
            r'''
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
            
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temperature_bottom_bound = temperature_bottom_bound
            temp_scale_step = temp_scale_step
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
    
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            cmap = colormaps.cool_temperatures_colormap()
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 5]", fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig6.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                fig7.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
    
        def plot_maximum_temperature_forecast(file_path, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, show_counties, state_linewidth, county_linewidth): 
        
            r'''
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
            
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
    
            cmap = colormaps.temperature_colormap()
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
        def plot_minimum_temperature_forecast(file_path, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, show_counties, state_linewidth, county_linewidth): 
        
            r'''
            THIS FUNCTION PLOTS AREAS WHERE THERE IS EXTREME HEAT IN THE FORECAST. DURING THE WARM SEASON (APRIL - OCTOBER) EXTREME HEAT IS DEFINED AS THE Minimum Temperature >= 120F AND COLD SEASON (NOVEMBER - MARCH) Minimum Temperature >= 100F AND IS BASED ON THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE Minimum Temperature GRIDS
        
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
            
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
    
            cmap = colormaps.temperature_colormap()
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs 
    
    
        def plot_NWS_Nights_2_through_7_minimum_temperature_trends(file_path, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth, color_table_shrink, colorbar_fontsize):
    
            r'''
            This function plots the latest available NOAA/NWS Maximum RH Trend Forecast. 
    
            Inputs: 1) directory_name (String) - File path on the NWS FTP server to the file being downloaded. 
                       (example for Pacific Southwest the directory_name is: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
    
                    2) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.
    
                    3) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.
    
                    4) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.
    
                    5) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.
    
                    6) central_longitude (Integer or Float) - The central longitude. Defaults to -96.
    
                    7) central_latitude (Integer or Float) - The central latitude. Defaults to 39.
    
                    8) first_standard_parallel (Integer or Float) - Southern standard parallel. 
    
                    9) second_standard_parallel (Integer or Float) - Northern standard parallel. 
                    
                    10) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
    
                    11) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
    
                    12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
                    13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
                    14) key_x_position (Integer or Float) - The x-position of the colortable key. 
    
                    15) key_y_position (Integer or Float) - The y-position of the colortable key. 
    
                    16) subplot_title_fontsize (Integer) - The fontsize of the plot title. 
    
                    17) signature_fontsize (Integer) - The fontsize of the signature. 
    
                    18) key_fontsize (Integer) - The fontsize of the key. 
    
                    19) show_counties (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    
                    20) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 
                    21) state_linewidth (Integer) - Width of the state borders. 
    
                    22) county_linewidth (Integer) - Width of the county borders.
    
            Return: A list of figures for each forecast day. 
            '''
    
    
            local_time, utc_time = standard.plot_creation_time()
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
            contour_step = contour_step
    
            cmap = colormaps.relative_humidity_change_colormap()
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
                
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
    
            diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
            diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
            diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
            diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
            diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
            if test_7 == True:
                diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
            else:
                pass
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 2]', fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 3]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 4]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
    
            return figs
    
    
        def plot_NWS_Days_2_through_7_maximum_temperature_trends(file_path, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth, color_table_shrink, colorbar_fontsize):
    
            r'''
            This function plots the latest available NOAA/NWS Maximum RH Trend Forecast. 
    
            Inputs: 1) directory_name (String) - File path on the NWS FTP server to the file being downloaded. 
                       (example for Pacific Southwest the directory_name is: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
    
                    2) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.
    
                    3) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.
    
                    4) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.
    
                    5) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.
    
                    6) central_longitude (Integer or Float) - The central longitude. Defaults to -96.
    
                    7) central_latitude (Integer or Float) - The central latitude. Defaults to 39.
    
                    8) first_standard_parallel (Integer or Float) - Southern standard parallel. 
    
                    9) second_standard_parallel (Integer or Float) - Northern standard parallel. 
                    
                    10) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
    
                    11) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
    
                    12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
                    13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
                    14) key_x_position (Integer or Float) - The x-position of the colortable key. 
    
                    15) key_y_position (Integer or Float) - The y-position of the colortable key. 
    
                    16) subplot_title_fontsize (Integer) - The fontsize of the plot title. 
    
                    17) signature_fontsize (Integer) - The fontsize of the signature. 
    
                    18) key_fontsize (Integer) - The fontsize of the key. 
    
                    19) show_counties (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    
                    20) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 
                    21) state_linewidth (Integer) - Width of the state borders. 
    
                    22) county_linewidth (Integer) - Width of the county borders.
    
            Return: A list of figures for each forecast day. 
            '''
    
    
            local_time, utc_time = standard.plot_creation_time()
            state_linewidth = state_linewidth
            county_linewidth = county_linewidth
            contour_step = contour_step
    
            cmap = colormaps.relative_humidity_change_colormap()
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
                
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
    
            diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
            diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
            diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
            diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
            diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
            if test_7 == True:
                diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
            else:
                pass
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 2]', fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 3]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 4]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_counties == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
    
            return figs
        

class Predictive_Services_Areas_Perspective:

    r'''
    THIS CLASS HOSTS A VARIETY OF PLOTTING FUNCTIONS. 

    THESE FUNCTIONS PLOT THE NATIONAL WEATHER SERVICE GRIDDED FORECAST DATA IN VARIOUS DIFFERENT WAYS

    GENERIC FORECAST FUNCTIONS OFFER SLIGHTLY MORE CUSTOMIZATION AS BOTH THE GENERIC FUNCTIONS ARE NOT PRESETS FOR A CERTAIN WEATHER ELEMENT. 

    THIS CLASS PLOTS THE DATA USING PREDICTIVE SERVICES AREAS (PSA) BOUNDARIES AS A REFERENCE POINT. 

    (C) METEOROLOGIST ERIC J. DREWITZ 2023

    '''

    class data_download_included_in_function:

        r'''
        This class hosts functions that include the data download within the function. Each time the function is called the data is downloaded and plots onto the map. 

        This is the recommended class for users who want to make a small amount of images. 

        If the user wants to make a large volume of images, please see the data_download_not_included_in_function class so that the user will only need to download the data once (download the data in the file that is automated before calling the plotting function) to maximize efficiency and execution time. 

        '''

        def plot_extreme_heat_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth): 
        
            r'''
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
            
            directory_name = directory_name
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
    
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxt.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax6.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
    
        def plot_frost_freeze_forecast(directory_name, temperature_bottom_bound, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, temp_scale_step, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth): 
        
            r'''
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
            
            directory_name = directory_name
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temperature_bottom_bound = temperature_bottom_bound
            temp_scale_step = temp_scale_step
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
    
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
            cmap = colormaps.cool_temperatures_colormap()
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.mint.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 5]", fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig6.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax6.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                fig7.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
    
        def plot_maximum_temperature_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth): 
        
            r'''
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
            
            directory_name = directory_name
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
    
            cmap = colormaps.temperature_colormap()
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxt.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax6.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
        def plot_minimum_temperature_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth): 
        
            r'''
            THIS FUNCTION PLOTS AREAS WHERE THERE IS EXTREME HEAT IN THE FORECAST. DURING THE WARM SEASON (APRIL - OCTOBER) EXTREME HEAT IS DEFINED AS THE Minimum Temperature >= 120F AND COLD SEASON (NOVEMBER - MARCH) Minimum Temperature >= 100F AND IS BASED ON THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE Minimum Temperature GRIDS
        
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
            
            directory_name = directory_name
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
    
            cmap = colormaps.temperature_colormap()
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.mint.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax6.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs 
    
    
        def plot_NWS_Nights_2_through_7_minimum_temperature_trends(directory_name, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth, color_table_shrink, colorbar_fontsize):
    
            r'''
            This function plots the latest available NOAA/NWS Maximum RH Trend Forecast. 
    
            Inputs: 1) directory_name (String) - File path on the NWS FTP server to the file being downloaded. 
                       (example for Pacific Southwest the directory_name is: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
    
                    2) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.
    
                    3) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.
    
                    4) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.
    
                    5) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.
    
                    6) central_longitude (Integer or Float) - The central longitude. Defaults to -96.
    
                    7) central_latitude (Integer or Float) - The central latitude. Defaults to 39.
    
                    8) first_standard_parallel (Integer or Float) - Southern standard parallel. 
    
                    9) second_standard_parallel (Integer or Float) - Northern standard parallel. 
                    
                    10) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
    
                    11) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
    
                    12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
                    13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
                    14) key_x_position (Integer or Float) - The x-position of the colortable key. 
    
                    15) key_y_position (Integer or Float) - The y-position of the colortable key. 
    
                    16) subplot_title_fontsize (Integer) - The fontsize of the plot title. 
    
                    17) signature_fontsize (Integer) - The fontsize of the signature. 
    
                    18) key_fontsize (Integer) - The fontsize of the key. 
    
                    19) show_counties (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    
                    20) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 
                    21) state_linewidth (Integer) - Width of the state borders. 
    
                    22) county_linewidth (Integer) - Width of the county borders.
    
            Return: A list of figures for each forecast day. 
            '''
    
    
            local_time, utc_time = standard.plot_creation_time()
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
            contour_step = contour_step
    
            cmap = colormaps.relative_humidity_change_colormap()
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
                
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.mint.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, False)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
    
            diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
            diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
            diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
            diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
            diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
            if test_7 == True:
                diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
            else:
                pass
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 2]', fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 3]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 4]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
    
            return figs
    
    
        def plot_NWS_Days_2_through_7_maximum_temperature_trends(directory_name, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth, color_table_shrink, colorbar_fontsize):
    
            r'''
            This function plots the latest available NOAA/NWS Maximum RH Trend Forecast. 
    
            Inputs: 1) directory_name (String) - File path on the NWS FTP server to the file being downloaded. 
                       (example for Pacific Southwest the directory_name is: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
    
                    2) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.
    
                    3) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.
    
                    4) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.
    
                    5) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.
    
                    6) central_longitude (Integer or Float) - The central longitude. Defaults to -96.
    
                    7) central_latitude (Integer or Float) - The central latitude. Defaults to 39.
    
                    8) first_standard_parallel (Integer or Float) - Southern standard parallel. 
    
                    9) second_standard_parallel (Integer or Float) - Northern standard parallel. 
                    
                    10) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
    
                    11) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
    
                    12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
                    13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
                    14) key_x_position (Integer or Float) - The x-position of the colortable key. 
    
                    15) key_y_position (Integer or Float) - The y-position of the colortable key. 
    
                    16) subplot_title_fontsize (Integer) - The fontsize of the plot title. 
    
                    17) signature_fontsize (Integer) - The fontsize of the signature. 
    
                    18) key_fontsize (Integer) - The fontsize of the key. 
    
                    19) show_counties (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    
                    20) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 
                    21) state_linewidth (Integer) - Width of the state borders. 
    
                    22) county_linewidth (Integer) - Width of the county borders.
    
            Return: A list of figures for each forecast day. 
            '''
    
    
            local_time, utc_time = standard.plot_creation_time()
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
            contour_step = contour_step
    
            cmap = colormaps.relative_humidity_change_colormap()
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
                
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
            da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxt.bin')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, False)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
    
            diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
            diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
            diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
            diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
            diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
            if test_7 == True:
                diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
            else:
                pass
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 2]', fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 3]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 4]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
    
            return figs


    class data_download_not_included_in_function:

        r'''
        This class hosts functions that do not include the data download within the function. 

        This is the recommended class for users who want to make a large amount of images so that minimal data downloads are needed. 

        '''

        def plot_extreme_heat_forecast(file_path, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth): 
        
            r'''
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
            
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
    
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax6.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nExtreme Heat (Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap='hot', transform=datacrs, extend='max')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap='hot', transform=datacrs, extend='max')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
    
        def plot_frost_freeze_forecast(file_path, temperature_bottom_bound, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, temp_scale_step, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth): 
        
            r'''
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
            
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temperature_bottom_bound = temperature_bottom_bound
            temp_scale_step = temp_scale_step
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
    
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
            cmap = colormaps.cool_temperatures_colormap()
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 5]", fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig6.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax6.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                fig7.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
    
        def plot_maximum_temperature_forecast(file_path, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth): 
        
            r'''
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
            
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
    
            cmap = colormaps.temperature_colormap()
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax6.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMaximum Temperature (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs
    
        def plot_minimum_temperature_forecast(file_path, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, title_fontsize, subplot_title_fontsize, colorbar_fontsize, signature_x_position, signature_y_position, signature_fontsize, start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth): 
        
            r'''
            THIS FUNCTION PLOTS AREAS WHERE THERE IS EXTREME HEAT IN THE FORECAST. DURING THE WARM SEASON (APRIL - OCTOBER) EXTREME HEAT IS DEFINED AS THE Minimum Temperature >= 120F AND COLD SEASON (NOVEMBER - MARCH) Minimum Temperature >= 100F AND IS BASED ON THE NATIONAL WEATHER SERVICE FORECAST
        
            IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE Minimum Temperature GRIDS
        
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
            
            start_of_warm_season_month = start_of_warm_season_month
            end_of_warm_season_month = end_of_warm_season_month
            start_of_cool_season_month = start_of_cool_season_month
            end_of_cool_season_month = end_of_cool_season_month
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            color_table_shrink = color_table_shrink
            title_fontsize = title_fontsize
            subplot_title_fontsize = subplot_title_fontsize 
            colorbar_fontsize = colorbar_fontsize
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position 
            signature_fontsize = signature_fontsize
            temp_scale_warm_start = temp_scale_warm_start
            temp_scale_warm_stop = temp_scale_warm_stop
            temp_scale_step = temp_scale_step
            temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
            temp_scale_cool_start = temp_scale_cool_start
            temp_scale_cool_stop = temp_scale_cool_stop
            temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
    
            cmap = colormaps.temperature_colormap()
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
    
            local_time, utc_time = standard.plot_creation_time()
        
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
            temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
            temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, True)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig1.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 1]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig1.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 1]", fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig2.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 2]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig2.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 2]", fontsize=title_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig3.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 3]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig3.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 3]", fontsize=title_fontsize, fontweight='bold')
        
            ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig4.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 4]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig4.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 4]", fontsize=title_fontsize, fontweight='bold')
        
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig5.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 5]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig5.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 5]", fontsize=title_fontsize, fontweight='bold')
        
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig6.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 6]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig6.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 6]", fontsize=title_fontsize, fontweight='bold')
        
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax6.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    fig7.suptitle("National Weather Service Forecast\nMinimum Temperature (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
            
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs, extend='both')
        
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs, extend='both')
        
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
            return figs 
    
    
        def plot_NWS_Nights_2_through_7_minimum_temperature_trends(file_path, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth, color_table_shrink, colorbar_fontsize):
    
            r'''
            This function plots the latest available NOAA/NWS Maximum RH Trend Forecast. 
    
            Inputs: 1) directory_name (String) - File path on the NWS FTP server to the file being downloaded. 
                       (example for Pacific Southwest the directory_name is: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
    
                    2) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.
    
                    3) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.
    
                    4) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.
    
                    5) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.
    
                    6) central_longitude (Integer or Float) - The central longitude. Defaults to -96.
    
                    7) central_latitude (Integer or Float) - The central latitude. Defaults to 39.
    
                    8) first_standard_parallel (Integer or Float) - Southern standard parallel. 
    
                    9) second_standard_parallel (Integer or Float) - Northern standard parallel. 
                    
                    10) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
    
                    11) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
    
                    12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
                    13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
                    14) key_x_position (Integer or Float) - The x-position of the colortable key. 
    
                    15) key_y_position (Integer or Float) - The y-position of the colortable key. 
    
                    16) subplot_title_fontsize (Integer) - The fontsize of the plot title. 
    
                    17) signature_fontsize (Integer) - The fontsize of the signature. 
    
                    18) key_fontsize (Integer) - The fontsize of the key. 
    
                    19) show_counties (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    
                    20) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 
                    21) state_linewidth (Integer) - Width of the state borders. 
    
                    22) county_linewidth (Integer) - Width of the county borders.
    
            Return: A list of figures for each forecast day. 
            '''
    
    
            local_time, utc_time = standard.plot_creation_time()
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
            contour_step = contour_step
    
            cmap = colormaps.relative_humidity_change_colormap()
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
                
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
    
            diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
            diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
            diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
            diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
            diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
            if test_7 == True:
                diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
            else:
                pass
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 2]', fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 3]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 4]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
    
            return figs
    
    
        def plot_NWS_Days_2_through_7_maximum_temperature_trends(file_path, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_rivers, gacc_boundary_linewidth, psa_boundary_linewidth, color_table_shrink, colorbar_fontsize):
    
            r'''
            This function plots the latest available NOAA/NWS Maximum RH Trend Forecast. 
    
            Inputs: 1) directory_name (String) - File path on the NWS FTP server to the file being downloaded. 
                       (example for Pacific Southwest the directory_name is: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
    
                    2) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.
    
                    3) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.
    
                    4) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.
    
                    5) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.
    
                    6) central_longitude (Integer or Float) - The central longitude. Defaults to -96.
    
                    7) central_latitude (Integer or Float) - The central latitude. Defaults to 39.
    
                    8) first_standard_parallel (Integer or Float) - Southern standard parallel. 
    
                    9) second_standard_parallel (Integer or Float) - Northern standard parallel. 
                    
                    10) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
    
                    11) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
    
                    12) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 
                    13) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.
                    14) key_x_position (Integer or Float) - The x-position of the colortable key. 
    
                    15) key_y_position (Integer or Float) - The y-position of the colortable key. 
    
                    16) subplot_title_fontsize (Integer) - The fontsize of the plot title. 
    
                    17) signature_fontsize (Integer) - The fontsize of the signature. 
    
                    18) key_fontsize (Integer) - The fontsize of the key. 
    
                    19) show_counties (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    
                    20) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 
                    21) state_linewidth (Integer) - Width of the state borders. 
    
                    22) county_linewidth (Integer) - Width of the county borders.
    
            Return: A list of figures for each forecast day. 
            '''
    
    
            local_time, utc_time = standard.plot_creation_time()
            gacc_boundary_linewidth = gacc_boundary_linewidth
            psa_boundary_linewidth = psa_boundary_linewidth
            contour_step = contour_step
    
            cmap = colormaps.relative_humidity_change_colormap()
            
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
                
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()
    
            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False)
    
            try:
                if grb_7_vals.all() != None:
                    test_7 = True
    
            except Exception as e:
                test_7 = False       
    
    
            diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
            diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
            diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
            diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
            diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
            if test_7 == True:
                diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
            else:
                pass
    
            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)
            grb_2_start = grb_2_start.replace(tzinfo=from_zone)
            grb_2_start = grb_2_start.astimezone(to_zone)
            grb_3_start = grb_3_start.replace(tzinfo=from_zone)
            grb_3_start = grb_3_start.astimezone(to_zone)
            grb_4_start = grb_4_start.replace(tzinfo=from_zone)
            grb_4_start = grb_4_start.astimezone(to_zone)
            grb_5_start = grb_5_start.replace(tzinfo=from_zone)
            grb_5_start = grb_5_start.astimezone(to_zone)
            grb_6_start = grb_6_start.replace(tzinfo=from_zone)
            grb_6_start = grb_6_start.astimezone(to_zone)
            if test_7 == True:
                grb_7_start = grb_7_start.replace(tzinfo=from_zone)
                grb_7_start = grb_7_start.astimezone(to_zone)
            else:
                pass
    
            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
            grb_2_end = grb_2_end.replace(tzinfo=from_zone)
            grb_2_end = grb_2_end.astimezone(to_zone)
            grb_3_end = grb_3_end.replace(tzinfo=from_zone)
            grb_3_end = grb_3_end.astimezone(to_zone)
            grb_4_end = grb_4_end.replace(tzinfo=from_zone)
            grb_4_end = grb_4_end.astimezone(to_zone)
            grb_5_end = grb_5_end.replace(tzinfo=from_zone)
            grb_5_end = grb_5_end.astimezone(to_zone)
            grb_6_end = grb_6_end.replace(tzinfo=from_zone)
            grb_6_end = grb_6_end.astimezone(to_zone)
            if test_7 == True:
                grb_7_end = grb_7_end.replace(tzinfo=from_zone)
                grb_7_end = grb_7_end.astimezone(to_zone)
            else:
                pass
                
            files = count
    
            figs = [] 
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 2]', fontsize=title_fontsize, fontweight='bold')
        
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax1.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 3]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax2.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 4]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax3.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax4.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            ax5.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Day 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(GACC, linewidth=gacc_boundary_linewidth, zorder=5)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                ax7.add_feature(PSAs, linewidth=psa_boundary_linewidth, zorder=4)
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', transform=datacrs, zorder=2, extend='both')
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
    
            return figs
