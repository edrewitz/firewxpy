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
import scipy.ndimage

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from NWS_Generic_Forecast_Graphics import standard
from dateutil import tz

class Counties_Perspective:

    def plot_NWS_7_Day_poor_overnight_recovery_relative_humidity_forecast(directory_name, poor_overnight_recovery_rh_threshold, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth, color_table_shrink):

        r'''
        This function plots the latest available NOAA/NWS Poor Overnight Recovery RH Forecast. 

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
        grid_time_interval = 24
        state_linewidth = state_linewidth
        county_linewidth = county_linewidth
        contour_step = contour_step
        poor_overnight_recovery_rh_threshold = poor_overnight_recovery_rh_threshold
        poor_overnight_recovery_rh_thresh = poor_overnight_recovery_rh_threshold + contour_step

        cmap = colormaps.low_relative_humidity_colormap()
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
            
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        try:
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_7_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_7_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.maxrh.bin')

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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)

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
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
            files = count
            
        except Exception as e:
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.maxrh.bin')

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
            files = count

        
        figs = [] 

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig1.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 1]', fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig2.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 2]', fontsize=title_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig3.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 3]', fontsize=title_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig4.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 4]', fontsize=title_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig5.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 5]', fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Relative Humidity (%)", fontweight='bold')

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig6.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 6]', fontsize=title_fontsize, fontweight='bold')
        
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax6.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
        cbar6.set_label(label="Relative Humidity (%)", fontweight='bold')

        if files == 7:

            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

            fig7.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 7]', fontsize=title_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

            cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
            cbar7.set_label(label="Relative Humidity (%)", fontweight='bold')
        
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


    def plot_NWS_7_Day_low_minimum_relative_humidity_forecast(directory_name, low_minimum_rh_threshold, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth, color_table_shrink):

        r'''
        This function plots the latest available NOAA/NWS Poor Overnight Recovery RH Forecast. 

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
        grid_time_interval = 24
        state_linewidth = state_linewidth
        county_linewidth = county_linewidth
        contour_step = contour_step
        low_minimum_rh_threshold = low_minimum_rh_threshold
        low_minimum_rh_thresh = low_minimum_rh_threshold + contour_step

        cmap = colormaps.low_relative_humidity_colormap()
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
            
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        try:
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_7_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_7_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.minrh.bin')

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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)

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
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
            files = count
            
        except Exception as e:
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.minrh.bin')

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
            files = count

        
        figs = [] 

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig1.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 1]', fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig2.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 2]', fontsize=title_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig3.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 3]', fontsize=title_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig4.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 4]', fontsize=title_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig5.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 5]', fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Relative Humidity (%)", fontweight='bold')

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig6.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 6]', fontsize=title_fontsize, fontweight='bold')
        
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax6.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
        cbar6.set_label(label="Relative Humidity (%)", fontweight='bold')

        if files == 7:

            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

            fig7.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 7]', fontsize=title_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

            cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
            cbar7.set_label(label="Relative Humidity (%)", fontweight='bold')
        
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
    
    def plot_relative_humidity_poor_recovery_short_term_forecast(directory_name, poor_overnight_recovery_rh_threshold, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink, signature_x_position_1, signature_y_position_1, signature_x_position_2, signature_y_position_2, signature_x_position_3, signature_y_position_3, signature_x_position_4, signature_y_position_4, signature_x_position_5, signature_y_position_5): 
    
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
    
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, count_of_GRIB_files, count = da.FTP_Downloads.get_latest_short_term_gridded_data(directory_name, 'ds.maxrh.bin')

        files = count

        try:
            if grb_1_vals.all() != None:
                test = True

        except Exception as e:
            test = False
    
        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 12
    
        files = count_of_GRIB_files
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        cmap = colormaps.low_relative_humidity_colormap()
       
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        contour_step = contour_step
        poor_overnight_recovery_rh_threshold = poor_overnight_recovery_rh_threshold
        poor_overnight_recovery_rh_thresh = poor_overnight_recovery_rh_threshold + contour_step
        
        
       
        if files == 1:

            grb_1_start = grb_1_start.replace(tzinfo=from_zone)
            grb_1_start = grb_1_start.astimezone(to_zone)

            grb_1_end = grb_1_end.replace(tzinfo=from_zone)
            grb_1_end = grb_1_end.astimezone(to_zone)
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(signature_x_position_1, signature_y_position_1, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= " + str(poor_overnight_recovery_rh_threshold)+"%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            if test == True:

                grb_1_start = grb_1_start.replace(tzinfo=from_zone)
                grb_1_start = grb_1_start.astimezone(to_zone)
                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                
                grb_1_end = grb_1_end.replace(tzinfo=from_zone)
                grb_1_end = grb_1_end.astimezone(to_zone)
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(signature_x_position_2, signature_y_position_2, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= " + str(poor_overnight_recovery_rh_threshold)+"%)", fontweight='bold')
     
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
         
            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
    
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(signature_x_position_1, signature_y_position_1, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= " + str(poor_overnight_recovery_rh_threshold)+"%)", fontweight='bold')
                
                ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
    
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
            
            if test == True:

                grb_1_start = grb_1_start.replace(tzinfo=from_zone)
                grb_1_start = grb_1_start.astimezone(to_zone)
                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                grb_3_start = grb_3_start.replace(tzinfo=from_zone)
                grb_3_start = grb_3_start.astimezone(to_zone)

                grb_1_end = grb_1_end.replace(tzinfo=from_zone)
                grb_1_end = grb_1_end.astimezone(to_zone)
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                grb_3_end = grb_3_end.replace(tzinfo=from_zone)
                grb_3_end = grb_3_end.astimezone(to_zone) 
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(signature_x_position_3, signature_y_position_3, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= " + str(poor_overnight_recovery_rh_threshold)+"%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=0.70)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                grb_3_start = grb_3_start.replace(tzinfo=from_zone)
                grb_3_start = grb_3_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                grb_3_end = grb_3_end.replace(tzinfo=from_zone)
                grb_3_end = grb_3_end.astimezone(to_zone)
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(signature_x_position_2, signature_y_position_2, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= " + str(poor_overnight_recovery_rh_threshold)+"%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            if test == True:

                grb_1_start = grb_1_start.replace(tzinfo=from_zone)
                grb_1_start = grb_1_start.astimezone(to_zone)
                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                grb_3_start = grb_3_start.replace(tzinfo=from_zone)
                grb_3_start = grb_3_start.astimezone(to_zone)
                grb_4_start = grb_4_start.replace(tzinfo=from_zone)
                grb_4_start = grb_4_start.astimezone(to_zone)
                
                grb_1_end = grb_1_end.replace(tzinfo=from_zone)
                grb_1_end = grb_1_end.astimezone(to_zone)
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                grb_3_end = grb_3_end.replace(tzinfo=from_zone)
                grb_3_end = grb_3_end.astimezone(to_zone)
                grb_4_end = grb_4_end.replace(tzinfo=from_zone)
                grb_4_end = grb_4_end.astimezone(to_zone)
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(signature_x_position_4, signature_y_position_4, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= " + str(poor_overnight_recovery_rh_threshold)+"%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                grb_3_start = grb_3_start.replace(tzinfo=from_zone)
                grb_3_start = grb_3_start.astimezone(to_zone)
                grb_4_start = grb_4_start.replace(tzinfo=from_zone)
                grb_4_start = grb_4_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                grb_3_end = grb_3_end.replace(tzinfo=from_zone)
                grb_3_end = grb_3_end.astimezone(to_zone)
                grb_4_end = grb_4_end.replace(tzinfo=from_zone)
                grb_4_end = grb_4_end.astimezone(to_zone)
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(signature_x_position_3, signature_y_position_3, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= " + str(poor_overnight_recovery_rh_threshold)+"%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            if test == True:

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
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(signature_x_position_5, signature_y_position_5, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= " + str(poor_overnight_recovery_rh_threshold)+"%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax4.set_title('Night 5 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                grb_3_start = grb_3_start.replace(tzinfo=from_zone)
                grb_3_start = grb_3_start.astimezone(to_zone)
                grb_4_start = grb_4_start.replace(tzinfo=from_zone)
                grb_4_start = grb_4_start.astimezone(to_zone)
                grb_5_start = grb_5_start.replace(tzinfo=from_zone)
                grb_5_start = grb_5_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                grb_3_end = grb_3_end.replace(tzinfo=from_zone)
                grb_3_end = grb_3_end.astimezone(to_zone)
                grb_4_end = grb_4_end.replace(tzinfo=from_zone)
                grb_4_end = grb_4_end.astimezone(to_zone)
                grb_5_end = grb_5_end.replace(tzinfo=from_zone)
                grb_5_end = grb_5_end.astimezone(to_zone)
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(signature_x_position_4, signature_y_position_4, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= " + str(poor_overnight_recovery_rh_threshold)+"%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %H:00 Local') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %H:00 Local'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        return fig


def plot_maximum_relative_humidity_short_term_forecast_and_trends_filtered(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink, colorbar_pad, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, signature_x_position_1, signature_y_position_1, signature_x_position_2, signature_y_position_2, signature_x_position_3, signature_y_position_3, signature_x_position_4, signature_y_position_4, signature_x_position_5, signature_y_position_5, signature_fontsize, title_fontsize): 

    r'''
    THIS FUNCTION PLOTS THE MAXIMUM TEMPERATURE FORECAST FOR THE FIRST PERIOD, THEN THE MAXIMUM TEMPERATURE FORECAST TRENDS FOR THE NEXT PERIODS. 

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

    temp_scale_warm, temp_scale_cool = parsers.NDFD.get_maximum_temperature_color_scale(directory_name)

    local_time, utc_time = standard.plot_creation_time()
    grid_time_interval = 12
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    cmap = colormaps.relative_humidity_colormap()
    cmap_change = colormaps.relative_humidity_change_filtered_colormap()

    grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, count_of_GRIB_files = da.FTP_Downloads.get_latest_short_term_gridded_data(directory_name, 'ds.maxrh.bin')

    files = count_of_GRIB_files

    
    try:
        if grb_1_vals.all() != None:
            test = True

    except Exception as e:
        test = False

    

    lons = lons_1
    lats = lats_1
   
    if files == 1:

        fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
        fig.text(signature_x_position_1, signature_y_position_1, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

        fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity", fontsize=title_fontsize, fontweight='bold')

        ax = plt.subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.OCEAN, color='blue', zorder=5)
        ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=6)
        ax.add_feature(cfeature.BORDERS, linewidth=7, edgecolor='red', zorder=6)
        ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
        ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

        cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)

            
        cbar = fig.colorbar(cs, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Maximum Relative Humidity (%)", fontweight='bold')

    if files == 2:

        if test == True:

            diff1 = grb_2_vals - grb_1_vals
            diff1_contours = mpcalc.smooth_gaussian(diff1, n=8)

            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(signature_x_position_2, signature_y_position_2, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')
            
            fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity\nSignificant Maximum Relative Humidity Trends (Max RH Trend >= ± 10%)", fontsize=title_fontsize, fontweight='bold')
 
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.OCEAN, color='blue', zorder=5)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=6)
            ax0.add_feature(cfeature.BORDERS, linewidth=8, edgecolor='violet', zorder=6)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
    
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Maximum Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=5)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=6)
            ax1.add_feature(cfeature.BORDERS, linewidth=8, edgecolor='violet', zorder=6)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons, lats, diff1, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)


            cbar1 = fig.colorbar(cs1, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar1.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')    


        else:

            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(signature_x_position_1, signature_y_position_1, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')
    
            fig.suptitle("National Weather Service Short-Term Forecast", fontsize=title_fontsize, fontweight='bold')
    
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=5)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=6)
            ax.add_feature(cfeature.BORDERS, linewidth=7, edgecolor='red', zorder=6)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs = ax.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
    
                
            cbar = fig.colorbar(cs, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Maximum Relative Humidity (%)", fontweight='bold')

    if files == 3:

        if test == True:

            diff1 = grb_2_vals - grb_1_vals
            diff2 = grb_3_vals - grb_2_vals
            diff1_contours = mpcalc.smooth_gaussian(diff1, n=8)
            diff2_contours = mpcalc.smooth_gaussian(diff2, n=8)

            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(signature_x_position_3, signature_y_position_3, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

         
            fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity\nSignificant Maximum Relative Humidity Trends (Max RH Trend >= ± 10%)", fontsize=title_fontsize, fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=4)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
    
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Maximum Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=4)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons, lats, diff1, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)


            cbar1 = fig.colorbar(cs1, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar1.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')    

   
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=4)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons, lats, diff2, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)


            cbar2 = fig.colorbar(cs2, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar2.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')    



        else:
            
            diff1 = grb_3_vals - grb_2_vals
            diff1_contours = mpcalc.smooth_gaussian(diff1, n=8)

            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(signature_x_position_2, signature_y_position_2, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

            
            fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity\nSignificant Maximum Relative Humidity Trends (Max RH Trend >= ± 10%)", fontsize=title_fontsize, fontweight='bold')

            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.OCEAN, color='blue', zorder=5)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=6)
            ax0.add_feature(cfeature.BORDERS, linewidth=8, edgecolor='violet', zorder=6)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
    
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Maximum Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=5)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='red', zorder=6)
            ax1.add_feature(cfeature.BORDERS, linewidth=8, edgecolor='violet', zorder=6)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons, lats, diff1, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)


            cbar1 = fig.colorbar(cs1, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar1.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')    
            

    if files == 4:

        if test == True:

            diff1 = grb_2_vals - grb_1_vals
            diff2 = grb_3_vals - grb_2_vals
            diff3 = grb_4_vals - grb_3_vals
            diff1_contours = mpcalc.smooth_gaussian(diff1, n=8)
            diff2_contours = mpcalc.smooth_gaussian(diff2, n=8)
            diff3_contours = mpcalc.smooth_gaussian(diff3, n=8)

            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(signature_x_position_4, signature_y_position_4, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

            
            fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity\nSignificant Maximum Relative Humidity Trends (Max RH Trend >= ± 10%)", fontsize=title_fontsize, fontweight='bold')

            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
    
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Maximum Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            cs1 = ax1.contourf(lons, lats, diff1, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)
    
            cbar1 = fig.colorbar(cs1, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar1.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')    

            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons, lats, diff2, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)

            cbar2 = fig.colorbar(cs2, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar2.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')   
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs3 = ax3.contourf(lons, lats, diff3, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)

            cbar3 = fig.colorbar(cs3, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar3.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')   

        else:

            diff1 = grb_3_vals - grb_2_vals
            diff2 = grb_4_vals - grb_3_vals
            diff1_contours = mpcalc.smooth_gaussian(diff1, n=8)
            diff2_contours = mpcalc.smooth_gaussian(diff2, n=8)

            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(signature_x_position_3, signature_y_position_3, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

            
            fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity\nSignificant Maximum Relative Humidity Trends (Max RH Trend >= ± 10%)", fontsize=title_fontsize, fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
    
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Maximum Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            cs1 = ax1.contourf(lons, lats, diff1, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)
    
            cbar1 = fig.colorbar(cs1, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar1.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')    

    
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs2 = ax2.contourf(lons, lats, diff2, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)

            cbar2 = fig.colorbar(cs2, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar2.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')   


    if files >= 5:

        if test == True:

            diff1 = grb_2_vals - grb_1_vals
            diff2 = grb_3_vals - grb_2_vals
            diff3 = grb_4_vals - grb_3_vals
            diff4 = grb_5_vals - grb_4_vals
            diff1_contours = mpcalc.smooth_gaussian(diff1, n=8)
            diff2_contours = mpcalc.smooth_gaussian(diff2, n=8)
            diff3_contours = mpcalc.smooth_gaussian(diff3, n=8)
            diff4_contours = mpcalc.smooth_gaussian(diff4, n=8)

            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(signature_x_position_5, signature_y_position_5, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

            
            fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity\nSignificant Maximum Relative Humidity Trends (Max RH Trend >= ± 10%)", fontsize=title_fontsize, fontweight='bold')


            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
    
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Maximum Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            cs1 = ax1.contourf(lons, lats, diff1, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)
    
            cbar1 = fig.colorbar(cs1, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar1.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')   

    
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            cs2 = ax2.contourf(lons, lats, diff2, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)

            cbar2 = fig.colorbar(cs2, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar2.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')       
    
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            cs3 = ax3.contourf(lons, lats, diff3, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)

            cbar3 = fig.colorbar(cs3, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar3.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')       
    
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax4.set_title('Day 5 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            cs4 = ax4.contourf(lons, lats, diff4, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)

            cbar4 = fig.colorbar(cs4, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar4.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')       


        else:

            diff1 = grb_3_vals - grb_2_vals
            diff2 = grb_4_vals - grb_3_vals
            diff3 = grb_5_vals - grb_4_vals
            diff1_contours = mpcalc.smooth_gaussian(diff1, n=8)
            diff2_contours = mpcalc.smooth_gaussian(diff2, n=8)
            diff3_contours = mpcalc.smooth_gaussian(diff3, n=8)

            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(signature_x_position_4, signature_y_position_4, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')
            
            fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity\nSignificant Maximum Relative Humidity Trends (Max RH Trend >= ± 10%)", fontsize=title_fontsize, fontweight='bold')


            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
    
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Maximum Relative Humidity (%)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs1 = ax1.contourf(lons, lats, diff1, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)

            cbar1 = fig.colorbar(cs1, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar1.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')       
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            cs2 = ax2.contourf(lons, lats, diff2, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)

            cbar2 = fig.colorbar(cs2, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar2.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')       
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            cs3 = ax3.contourf(lons, lats, diff3, levels=(-75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75), cmap=cmap_change, transform=datacrs)

            cbar3 = fig.colorbar(cs3, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar3.set_label(label="Maximum Relative Humidity Trend (%)", fontweight='bold')       

    return fig


def plot_minimum_relative_humidity_short_term_forecast_and_trends_filtered(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink, colorbar_pad, first_subplot_aspect_ratio, subsequent_subplot_aspect_ratio, signature_x_position_1, signature_y_position_1, signature_x_position_2, signature_y_position_2, signature_x_position_3, signature_y_position_3, signature_x_position_4, signature_y_position_4, signature_x_position_5, signature_y_position_5, signature_fontsize, title_fontsize, red_tick_x_position_2, red_tick_y_position_2, blue_tick_x_position_2, blue_tick_y_position_2, red_tick_x_position_3, red_tick_y_position_3, blue_tick_x_position_3, blue_tick_y_position_3, red_tick_x_position_4, red_tick_y_position_4, blue_tick_x_position_4, blue_tick_y_position_4, red_tick_x_position_5, red_tick_y_position_5, blue_tick_x_position_5, blue_tick_y_position_5, tick_mark_fontsize, label_fontsize): 

    r'''
    THIS FUNCTION PLOTS THE MAXIMUM TEMPERATURE FORECAST FOR THE FIRST PERIOD, THEN THE MAXIMUM TEMPERATURE FORECAST TRENDS FOR THE NEXT PERIODS. 

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

    temp_scale_warm, temp_scale_cool = parsers.NDFD.get_minimum_temperature_color_scale(directory_name)

    local_time, utc_time = standard.plot_creation_time()
    grid_time_interval = 12
    
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    cmap = colormaps.temperature_colormap()
    cmap_cool = colormaps.cool_temperatures_colormap()
    cmap_warm = colormaps.warm_temperatures_colormap()

    grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, count_of_GRIB_files = da.FTP_Downloads.get_latest_short_term_gridded_data(directory_name, 'ds.mint.bin')

    files = count_of_GRIB_files

    
    try:
        if grb_1_vals.all() != None:
            test = True

    except Exception as e:
        test = False

    

    lons = lons_1
    lats = lats_1
   
    if files == 1:

        fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
        fig.text(signature_x_position_1, signature_y_position_1, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

        fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Temperature", fontsize=title_fontsize, fontweight='bold')

        ax = plt.subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
        ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
        ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
        ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

        if utc_time.month >= 4 and utc_time.month <= 10:
            cs = ax.contourf(lons, lats, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs)

        if utc_time.month >= 11 or utc_time.month <= 3:
            cs = ax.contourf(lons, lats, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs)
            
        cbar = fig.colorbar(cs, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
        cbar.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')

    if files == 2:

        if test == True:

            diff1 = grb_2_vals - grb_1_vals
            diff1 = mpcalc.smooth_gaussian(diff1, n=8)

            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(signature_x_position_2, signature_y_position_2, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

            fig.text(red_tick_x_position_2, red_tick_y_position_2, "RED", fontsize=tick_mark_fontsize, fontweight='bold', color='red')

            red_tick_text_x_position_2 = red_tick_x_position_2 + 0.03

            fig.text(red_tick_text_x_position_2, red_tick_y_position_2, "Shaded Areas Denote Temperature Trend >= +5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 

            fig.text(blue_tick_x_position_2, blue_tick_y_position_2, "BLUE", fontsize=tick_mark_fontsize, fontweight='bold', color='blue')

            blue_tick_text_x_position_2 = blue_tick_x_position_2 + 0.04

            fig.text(blue_tick_text_x_position_2, blue_tick_y_position_2, "Shaded Areas Denote Temperature Trend >= -5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 
            
            fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Temperature & Minimum Temperature Trends", fontsize=title_fontsize, fontweight='bold')
 
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_time.month <= 10:
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs)

            if utc_time.month >= 11 or utc_time.month <= 3:
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            ax1.contourf(lons, lats, diff1, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax1.contourf(lons, lats, diff1, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_1 = ax1.contour(lons, lats, diff1, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_2 = ax1.contour(lons, lats, diff1, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax1.clabel(temp_change_1, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax1.clabel(temp_change_2, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)


        else:

            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(signature_x_position_1, signature_y_position_1, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')
    
            fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Temperature", fontsize=title_fontsize, fontweight='bold')
    
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_time.month <= 10:
                cs = ax.contourf(lons, lats, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs)
    
            if utc_time.month >= 11 or utc_time.month <= 3:
                cs = ax.contourf(lons, lats, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs)
                
            cbar = fig.colorbar(cs, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')

    if files == 3:

        if test == True:

            diff1 = grb_2_vals - grb_1_vals
            diff2 = grb_3_vals - grb_2_vals
            diff1 = mpcalc.smooth_gaussian(diff1, n=8)
            diff2 = mpcalc.smooth_gaussian(diff2, n=8)

            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(signature_x_position_3, signature_y_position_3, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

            fig.text(red_tick_x_position_3, red_tick_y_position_3, "RED", fontsize=tick_mark_fontsize, fontweight='bold', color='red')

            red_tick_text_x_position_3 = red_tick_x_position_3 + 0.03

            fig.text(red_tick_text_x_position_3, red_tick_y_position_3, "Shaded Areas Denote Temperature Trend >= +5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 

            fig.text(blue_tick_x_position_3, blue_tick_y_position_3, "BLUE", fontsize=tick_mark_fontsize, fontweight='bold', color='blue')

            blue_tick_text_x_position_3 = blue_tick_x_position_3 + 0.04

            fig.text(blue_tick_text_x_position_3, blue_tick_y_position_3, "Shaded Areas Denote Temperature Trend >= -5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 
            
            fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Temperature & Minimum Temperature Trends", fontsize=title_fontsize, fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_time.month <= 10:
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs)

            if utc_time.month >= 11 or utc_time.month <= 3:
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            ax1.contourf(lons, lats, diff1, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax1.contourf(lons, lats, diff1, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_1 = ax1.contour(lons, lats, diff1, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_2 = ax1.contour(lons, lats, diff1, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax1.clabel(temp_change_1, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True, colors='black')
            ax1.clabel(temp_change_2, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True, colors='black')
    
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            ax2.contourf(lons, lats, diff2, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax2.contourf(lons, lats, diff2, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_3 = ax2.contour(lons, lats, diff2, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_4 = ax2.contour(lons, lats, diff2, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax2.clabel(temp_change_3, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True, colors='black')
            ax2.clabel(temp_change_4, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True, colors='black')


        else:
            
            diff1 = grb_3_vals - grb_2_vals
            diff1 = mpcalc.smooth_gaussian(diff1, n=8)

            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(signature_x_position_2, signature_y_position_2, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

            fig.text(red_tick_x_position_2, red_tick_y_position_2, "RED", fontsize=tick_mark_fontsize, fontweight='bold', color='red')

            red_tick_text_x_position_2 = red_tick_x_position_2 + 0.03

            fig.text(red_tick_text_x_position_2, red_tick_y_position_2, "Shaded Areas Denote Temperature Trend >= +5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 

            fig.text(blue_tick_x_position_2, blue_tick_y_position_2, "BLUE", fontsize=tick_mark_fontsize, fontweight='bold', color='blue')

            blue_tick_text_x_position_2 = blue_tick_x_position_2 + 0.04

            fig.text(blue_tick_text_x_position_2, blue_tick_y_position_2, "Shaded Areas Denote Temperature Trend >= -5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 
            
            fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Temperature & Minimum Temperature Trends", fontsize=title_fontsize, fontweight='bold')

            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_time.month <= 10:
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs)

            if utc_time.month >= 11 or utc_time.month <= 3:
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            ax1.contourf(lons, lats, diff1, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax1.contourf(lons, lats, diff1, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_1 = ax1.contour(lons, lats, diff1, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_2 = ax1.contour(lons, lats, diff1, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax1.clabel(temp_change_1, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True, colors='black')
            ax1.clabel(temp_change_2, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True, colors='black')
            

    if files == 4:

        if test == True:

            diff1 = grb_2_vals - grb_1_vals
            diff2 = grb_3_vals - grb_2_vals
            diff3 = grb_4_vals - grb_3_vals
            diff1 = mpcalc.smooth_gaussian(diff1, n=8)
            diff2 = mpcalc.smooth_gaussian(diff2, n=8)
            diff3 = mpcalc.smooth_gaussian(diff3, n=8)

            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(signature_x_position_4, signature_y_position_4, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

            fig.text(red_tick_x_position_4, red_tick_y_position_4, "RED", fontsize=tick_mark_fontsize, fontweight='bold', color='red')

            red_tick_text_x_position_4 = red_tick_x_position_4 + 0.03

            fig.text(red_tick_text_x_position_4, red_tick_y_position_4, "Shaded Areas Denote Temperature Trend >= +5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 

            fig.text(blue_tick_x_position_4, blue_tick_y_position_4, "BLUE", fontsize=tick_mark_fontsize, fontweight='bold', color='blue')

            blue_tick_text_x_position_4 = blue_tick_x_position_4 + 0.04

            fig.text(blue_tick_text_x_position_4, blue_tick_y_position_4, "Shaded Areas Denote Temperature Trend >= -5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 
            
            fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Temperature & Minimum Temperature Trends", fontsize=title_fontsize, fontweight='bold')

            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_time.month <= 10:
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs)

            if utc_time.month >= 11 or utc_time.month <= 3:
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            ax1.contourf(lons, lats, diff1, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax1.contourf(lons, lats, diff1, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_1 = ax1.contour(lons, lats, diff1, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_2 = ax1.contour(lons, lats, diff1, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax1.clabel(temp_change_1, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax1.clabel(temp_change_2, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            ax2.contourf(lons, lats, diff2, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax2.contourf(lons, lats, diff2, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_3 = ax2.contour(lons, lats, diff2, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_4 = ax2.contour(lons, lats, diff2, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax2.clabel(temp_change_3, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax2.clabel(temp_change_4, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            ax3.contourf(lons, lats, diff3, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax3.contourf(lons, lats, diff3, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_5 = ax3.contour(lons, lats, diff3, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_6 = ax3.contour(lons, lats, diff3, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax3.clabel(temp_change_5, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax3.clabel(temp_change_6, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)

        else:

            diff1 = grb_3_vals - grb_2_vals
            diff2 = grb_4_vals - grb_3_vals
            diff1 = mpcalc.smooth_gaussian(diff1, n=8)
            diff2 = mpcalc.smooth_gaussian(diff2, n=8)

            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(signature_x_position_3, signature_y_position_3, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

            fig.text(red_tick_x_position_3, red_tick_y_position_3, "RED", fontsize=tick_mark_fontsize, fontweight='bold', color='red')

            red_tick_text_x_position_3 = red_tick_x_position_3 + 0.03

            fig.text(red_tick_text_x_position_3, red_tick_y_position_3, "Shaded Areas Denote Temperature Trend >= +5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 

            fig.text(blue_tick_x_position_3, blue_tick_y_position_3, "BLUE", fontsize=tick_mark_fontsize, fontweight='bold', color='blue')

            blue_tick_text_x_position_3 = blue_tick_x_position_3 + 0.04

            fig.text(blue_tick_text_x_position_3, blue_tick_y_position_3, "Shaded Areas Denote Temperature Trend >= -5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 
            
            fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Temperature & Minimum Temperature Trends", fontsize=title_fontsize, fontweight='bold')

            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_time.month <= 10:
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs)

            if utc_time.month >= 11 or utc_time.month <= 3:
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            ax1.contourf(lons, lats, diff1, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax1.contourf(lons, lats, diff1, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_1 = ax1.contour(lons, lats, diff1, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_2 = ax1.contour(lons, lats, diff1, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax1.clabel(temp_change_1, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax1.clabel(temp_change_2, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
    
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            ax2.contourf(lons, lats, diff2, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax2.contourf(lons, lats, diff2, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_3 = ax2.contour(lons, lats, diff2, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_4 = ax2.contour(lons, lats, diff2, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax2.clabel(temp_change_3, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax2.clabel(temp_change_4, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)

    if files >= 5:

        if test == True:

            diff1 = grb_2_vals - grb_1_vals
            diff2 = grb_3_vals - grb_2_vals
            diff3 = grb_4_vals - grb_3_vals
            diff4 = grb_5_vals - grb_4_vals
            diff1 = mpcalc.smooth_gaussian(diff1, n=8)
            diff2 = mpcalc.smooth_gaussian(diff2, n=8)
            diff3 = mpcalc.smooth_gaussian(diff3, n=8)
            diff4 = mpcalc.smooth_gaussian(diff4, n=8)

            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(signature_x_position_5, signature_y_position_5, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

            fig.text(red_tick_x_position_5, red_tick_y_position_5, "RED", fontsize=tick_mark_fontsize, fontweight='bold', color='red')

            red_tick_text_x_position_5 = red_tick_x_position_5 + 0.03

            fig.text(red_tick_text_x_position_5, red_tick_y_position_5, "Shaded Areas Denote Temperature Trend >= +5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 

            fig.text(blue_tick_x_position_5, blue_tick_y_position_5, "BLUE", fontsize=tick_mark_fontsize, fontweight='bold', color='blue')

            blue_tick_text_x_position_5 = blue_tick_x_position_5 + 0.04

            fig.text(blue_tick_text_x_position_5, blue_tick_y_position_5, "Shaded Areas Denote Temperature Trend >= -5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 
            
            fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Temperature & Minimum Temperature Trends", fontsize=title_fontsize, fontweight='bold')


            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_time.month <= 10:
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs)

            if utc_time.month >= 11 or utc_time.month <= 3:
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            ax1.contourf(lons, lats, diff1, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax1.contourf(lons, lats, diff1, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_1 = ax1.contour(lons, lats, diff1, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_2 = ax1.contour(lons, lats, diff1, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax1.clabel(temp_change_1, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax1.clabel(temp_change_2, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
    
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            ax2.contourf(lons, lats, diff2, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax2.contourf(lons, lats, diff2, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_3 = ax2.contour(lons, lats, diff2, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_4 = ax2.contour(lons, lats, diff2, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax2.clabel(temp_change_3, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax2.clabel(temp_change_4, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
    
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            ax3.contourf(lons, lats, diff3, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax3.contourf(lons, lats, diff3, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_5 = ax3.contour(lons, lats, diff3, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_6 = ax3.contour(lons, lats, diff3, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax3.clabel(temp_change_5, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax3.clabel(temp_change_6, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
    
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax4.set_title('Night 5 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            ax4.contourf(lons, lats, diff4, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax4.contourf(lons, lats, diff4, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_7 = ax4.contour(lons, lats, diff4, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_8 = ax4.contour(lons, lats, diff4, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax4.clabel(temp_change_7, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax4.clabel(temp_change_8, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)


        else:

            diff1 = grb_3_vals - grb_2_vals
            diff2 = grb_4_vals - grb_3_vals
            diff3 = grb_5_vals - grb_4_vals
            diff1 = mpcalc.smooth_gaussian(diff1, n=8)
            diff2 = mpcalc.smooth_gaussian(diff2, n=8)
            diff3 = mpcalc.smooth_gaussian(diff3, n=8)

            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(signature_x_position_4, signature_y_position_4, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontsize=signature_fontsize, fontweight='bold')

            fig.text(red_tick_x_position_4, red_tick_y_position_4, "RED", fontsize=tick_mark_fontsize, fontweight='bold', color='red')

            red_tick_text_x_position_4 = red_tick_x_position_4 + 0.03

            fig.text(red_tick_text_x_position_4, red_tick_y_position_4, "Shaded Areas Denote Temperature Trend >= +5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 

            fig.text(blue_tick_x_position_4, blue_tick_y_position_4, "BLUE", fontsize=tick_mark_fontsize, fontweight='bold', color='blue')

            blue_tick_text_x_position_4 = blue_tick_x_position_4 + 0.04

            fig.text(blue_tick_text_x_position_4, blue_tick_y_position_4, "Shaded Areas Denote Temperature Trend >= -5\N{DEGREE SIGN}F", fontsize=label_fontsize, fontweight='bold') 
            
            fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Temperature & Minimum Temperature Trends", fontsize=title_fontsize, fontweight='bold')


            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            if utc_time.month >= 4 and utc_time.month <= 10:
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=temp_scale_warm, cmap=cmap, transform=datacrs)

            if utc_time.month >= 11 or utc_time.month <= 3:
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=temp_scale_cool, cmap=cmap, transform=datacrs)
                
            cbar0 = fig.colorbar(cs0, location='left', shrink=color_table_shrink, pad=colorbar_pad)
            cbar0.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            ax1.contourf(lons, lats, diff1, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax1.contourf(lons, lats, diff1, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_1 = ax1.contour(lons, lats, diff1, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_2 = ax1.contour(lons, lats, diff1, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax1.clabel(temp_change_1, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax1.clabel(temp_change_2, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
    
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            ax2.contourf(lons, lats, diff2, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax2.contourf(lons, lats, diff2, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_3 = ax2.contour(lons, lats, diff2, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_4 = ax2.contour(lons, lats, diff2, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax2.clabel(temp_change_3, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax2.clabel(temp_change_4, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
    
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='green', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')

            ax3.contourf(lons, lats, diff3, levels=np.arange(-30, -4, 1), cmap=cmap_cool, alpha=0.25, transform=datacrs)

            ax3.contourf(lons, lats, diff3, levels=np.arange(5, 31, 1), cmap=cmap_warm, alpha=0.25, transform=datacrs)

            temp_change_5 = ax3.contour(lons, lats, diff3, levels=np.arange(-30, 0, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)

            temp_change_6 = ax3.contour(lons, lats, diff3, levels=np.arange(5, 35, 5), colors='black', linewidths=2, linestyles='-', transform=datacrs)
                
            ax3.clabel(temp_change_5, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)
            ax3.clabel(temp_change_6, fontsize=12, inline=3, inline_spacing=5, fmt='%i', rightside_up=True)

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
        
        cmap = colormaps.low_relative_humidity_colormap()

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
        
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
     
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.70)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Night 7 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 4 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 5 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Night 6 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax4.set_title('Night 7 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
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
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
     
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
         
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
                
                ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
            
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax4.set_title('Night 5 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
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
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
     
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
         
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Night 7 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 4 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 5 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Night 6 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax4.set_title('Night 7 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
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
        
        cmap = colormaps.low_relative_humidity_colormap()

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
        
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
     
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
         
            if utc_time.hour > 21 or utc_time.hour <= 6:
    
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
                
                ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
    
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
            
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour > 21 or utc_time.hour <= 6:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Day 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour > 21 or utc_time.hour <= 6:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Day 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Day 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax4.set_title('Day 5 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour > 21 or utc_time.hour <= 6:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Day 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Day 4 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
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
        
        cmap = colormaps.low_relative_humidity_colormap()

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
        
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
    
            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
     
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Day 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Day 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Day 7 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 3 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 4 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Day 5 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Day 6 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax4.set_title('Day 7 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
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
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
     
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
         
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
                
                ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
            
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files == 4:
    
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files >= 5:
    
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax4.set_title('Night 5 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
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
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
    
            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
     
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Night 7 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
            cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Night 4 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Night 5 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Night 6 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax4.set_title('Night 7 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
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
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
     
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
         
            if utc_time.hour >= 22 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
                
                ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
            
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 22 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files == 4:

            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 22 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files >= 5:
    
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax4.set_title('Day 5 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 22 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
                ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
                ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
                ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
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
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
    
            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
     
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
         
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Day 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files == 4:

            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Day 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Day 7 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
            cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files >= 5:

            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax0.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax0.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax0.set_title('Day 3 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax1.set_title('Day 4 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax2.set_title('Day 5 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax3.set_title('Day 6 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            ax4.set_title('Day 7 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
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



    r'''
    THIS NESTED CLASS HOSTS THE IMAGES FOR CONUS AKA THE "LOWER-48"
    '''

    def plot_NWS_7_Day_poor_overnight_recovery_relative_humidity_forecast(directory_name, poor_overnight_recovery_rh_threshold, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth, color_table_shrink):

        r'''
        This function plots the latest available NOAA/NWS Poor Overnight Recovery RH Forecast. 

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
        grid_time_interval = 24
        state_linewidth = state_linewidth
        county_linewidth = county_linewidth
        contour_step = contour_step
        poor_overnight_recovery_rh_threshold = poor_overnight_recovery_rh_threshold
        poor_overnight_recovery_rh_thresh = poor_overnight_recovery_rh_threshold + contour_step

        cmap = colormaps.low_relative_humidity_colormap()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'green')
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
            
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        try:
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_7_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_7_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.maxrh.bin')

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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)

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
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
            files = count
            
        except Exception as e:
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.maxrh.bin')

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
            files = count

        
        figs = [] 

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig1.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 1]', fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(GACC, linewidth=2, zorder=5)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax1.add_feature(PSAs, linewidth=1, zorder=4)
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig2.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 2]', fontsize=title_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(GACC, linewidth=2, zorder=5)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax2.add_feature(PSAs, linewidth=1, zorder=4)
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig3.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 3]', fontsize=title_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(GACC, linewidth=2, zorder=5)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax3.add_feature(PSAs, linewidth=1, zorder=4)
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig4.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 4]', fontsize=title_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(GACC, linewidth=2, zorder=5)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax4.add_feature(PSAs, linewidth=1, zorder=4)
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig5.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 5]', fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(GACC, linewidth=2, zorder=5)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax5.add_feature(PSAs, linewidth=1, zorder=4)
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Relative Humidity (%)", fontweight='bold')

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig6.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 6]', fontsize=title_fontsize, fontweight='bold')
        
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(GACC, linewidth=2, zorder=5)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax6.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax6.add_feature(PSAs, linewidth=1, zorder=4)
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
        cbar6.set_label(label="Relative Humidity (%)", fontweight='bold')

        if files == 7:

            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

            fig7.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 7]', fontsize=title_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(GACC, linewidth=2, zorder=5)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax7.add_feature(PSAs, linewidth=1, zorder=4)
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

            cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
            cbar7.set_label(label="Relative Humidity (%)", fontweight='bold')
        
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


    def plot_NWS_7_Day_low_minimum_relative_humidity_forecast(directory_name, low_minimum_rh_threshold, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth, color_table_shrink):

        r'''
        This function plots the latest available NOAA/NWS Poor Overnight Recovery RH Forecast. 

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
        grid_time_interval = 24
        state_linewidth = state_linewidth
        county_linewidth = county_linewidth
        contour_step = contour_step
        low_minimum_rh_threshold = low_minimum_rh_threshold
        low_minimum_rh_thresh = low_minimum_rh_threshold + contour_step

        cmap = colormaps.low_relative_humidity_colormap()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'green')
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
            
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        try:
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_7_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_7_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.minrh.bin')

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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)

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
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
            files = count
            
        except Exception as e:
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.minrh.bin')

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
            files = count

        
        figs = [] 

        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig1.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 1]', fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(GACC, linewidth=2, zorder=5)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax1.add_feature(PSAs, linewidth=1, zorder=4)
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig2.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 2]', fontsize=title_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(GACC, linewidth=2, zorder=5)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax2.add_feature(PSAs, linewidth=1, zorder=4)
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig3.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 3]', fontsize=title_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(GACC, linewidth=2, zorder=5)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax3.add_feature(PSAs, linewidth=1, zorder=4)
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig4.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 4]', fontsize=title_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(GACC, linewidth=2, zorder=5)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax4.add_feature(PSAs, linewidth=1, zorder=4)
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig5.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 5]', fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(GACC, linewidth=2, zorder=5)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax5.add_feature(PSAs, linewidth=1, zorder=4)
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Relative Humidity (%)", fontweight='bold')

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

        fig6.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 6]', fontsize=title_fontsize, fontweight='bold')
        
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(GACC, linewidth=2, zorder=5)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax6.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax6.add_feature(PSAs, linewidth=1, zorder=4)
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
        cbar6.set_label(label="Relative Humidity (%)", fontweight='bold')

        if files == 7:

            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')

            fig7.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 7]', fontsize=title_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(GACC, linewidth=2, zorder=5)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax7.add_feature(PSAs, linewidth=1, zorder=4)
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2)

            cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
            cbar7.set_label(label="Relative Humidity (%)", fontweight='bold')
        
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
        
        cmap = colormaps.low_relative_humidity_colormap()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')


        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
     
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
         
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
                
                ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
            
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=0.70)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax4.add_feature(GACC, linewidth=2.5, zorder=3)
                ax4.set_title('Night 5 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1),cmap=cmap, transform=datacrs)
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
        
        cmap = colormaps.low_relative_humidity_colormap()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
        
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
     
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=0.70)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax3.add_feature(GACC, linewidth=2.5, zorder=3)
            ax3.set_title('Night 7 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nPoor Overnight Relative Humidity Recovery (Max RH <= 30%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 4 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Night 5 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax3.add_feature(GACC, linewidth=2.5, zorder=3)
            ax3.set_title('Night 6 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax4.add_feature(GACC, linewidth=2.5, zorder=3)
            ax4.set_title('Night 7 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 31, 1), cmap=cmap, transform=datacrs)
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

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
        cmap = colormaps.excellent_recovery_colormap()

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
     
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs) 
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
         
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
                
                ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
            
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax4.add_feature(GACC, linewidth=2.5, zorder=3)
                ax4.set_title('Night 5 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Night 4 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
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

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
        cmap = colormaps.excellent_recovery_colormap()

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')
        
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 06Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 18Z'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
     
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
         
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Night 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax3.add_feature(GACC, linewidth=2.5, zorder=3)
            ax3.set_title('Night 7 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nExcellent Overnight Relative Humidity Recovery (Max RH >= 80%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 4 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Night 5 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax3.add_feature(GACC, linewidth=2.5, zorder=3)
            ax3.set_title('Night 6 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(80, 101, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax4.add_feature(GACC, linewidth=2.5, zorder=3)
            ax4.set_title('Night 7 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
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
        
        cmap = colormaps.low_relative_humidity_colormap()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
        
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
     
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
         
            if utc_time.hour > 21 or utc_time.hour <= 6:
    
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
                
                ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
    
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
            
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour > 21 or utc_time.hour <= 6:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Day 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour > 21 or utc_time.hour <= 6:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Day 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Day 3 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Day 4 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax4.add_feature(GACC, linewidth=2.5, zorder=3)
                ax4.set_title('Day 5 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity (%)", fontweight='bold')
    
            if utc_time.hour > 21 or utc_time.hour <= 6:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Day 3 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Day 4 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
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
        
        cmap = colormaps.low_relative_humidity_colormap()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')
        
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
    
            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
     
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Day 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Day 5 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Day 6 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax3.add_feature(GACC, linewidth=2.5, zorder=3)
            ax3.set_title('Day 7 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nRed Flag Warning Minimum Relative Humidity(Min RH <= 15%)", fontweight='bold')
    
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Day 3 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Day 4 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Day 5 Forecast\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax3.add_feature(GACC, linewidth=2.5, zorder=3)
            ax3.set_title('Day 6 Forecast\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax4.add_feature(GACC, linewidth=2.5, zorder=3)
            ax4.set_title('Day 7 Forecast\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs4 = ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 16, 1), cmap=cmap, transform=datacrs)
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

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
        cmap = colormaps.relative_humidity_colormap()
        cmap_change = colormaps.relative_humidity_change_colormap()
    
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')

        lons = lons_1
        lats = lats_1
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
     
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
         
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
                
                ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
            
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files == 4:
    
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files >= 5:
    
            if utc_time.hour >= 18 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax4.add_feature(GACC, linewidth=2.5, zorder=3)
                ax4.set_title('Night 5 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 6 and utc_time.hour < 18:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Night 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Night 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Night 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Night 4 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
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

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
        cmap = colormaps.relative_humidity_colormap()
        cmap_change = colormaps.relative_humidity_change_colormap()
    
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.maxrh.bin')

        lons = lons_1
        lats = lats_1
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
    
            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
     
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Night 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files == 4:
    
            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Night 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax3.add_feature(GACC, linewidth=2.5, zorder=3)
            ax3.set_title('Night 7 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
            cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files >= 5:
    
            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMaximum Relative Humidity & Maximum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Night 3 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Night 4 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Night 5 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax3.add_feature(GACC, linewidth=2.5, zorder=3)
            ax3.set_title('Night 6 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax4.add_feature(GACC, linewidth=2.5, zorder=3)
            ax4.set_title('Night 7 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
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

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')

        cmap = colormaps.relative_humidity_colormap()
        cmap_change = colormaps.relative_humidity_change_colormap()
    
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')

        lons = lons_1
        lats = lats_1
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
            
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
     
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
         
            if utc_time.hour >= 22 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
                
                ax0 = plt.subplot(1, 1, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 3:
            
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 22 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
                fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files == 4:

            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap='BrBG', transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 22 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
                fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
                ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files >= 5:
    
            if utc_time.hour > 6 and utc_time.hour <= 21:
    
                fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
                fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
                cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
                ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax4.add_feature(GACC, linewidth=2.5, zorder=3)
                ax4.set_title('Day 5 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
                cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
            if utc_time.hour >= 22 or utc_time.hour < 6:
    
                fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
                fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
                fig.suptitle("National Weather Service Short-Term Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
                ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
                ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax0.add_feature(GACC, linewidth=2.5, zorder=3)
                ax0.set_title('Day 1 Forecast\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs0 = ax0.contourf(lons, lats, grb_2_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
                cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
                cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
                ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax1.add_feature(GACC, linewidth=2.5, zorder=3)
                ax1.set_title('Day 2 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs1 = ax1.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
                cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax2.add_feature(GACC, linewidth=2.5, zorder=3)
                ax2.set_title('Day 3 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
                cs2 = ax2.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
                cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
                cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
                ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
                ax3.add_feature(GACC, linewidth=2.5, zorder=3)
                ax3.set_title('Day 4 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
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

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')
    
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5 = parsers.NDFD.parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, 'ds.minrh.bin')

        lons = lons_1
        lats = lats_1
       
        if files == 1:
    
            fig = plt.figure(figsize=(fig_x_length_1, fig_y_length_1))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
            
            ax = plt.subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax.add_feature(GACC, linewidth=2.5, zorder=3)
            ax.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
    
            cs = ax.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", fontweight='bold')
    
        if files == 2:
    
            fig = plt.figure(figsize=(fig_x_length_2, fig_y_length_2))
            fig.text(0.13, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
     
            ax0 = plt.subplot(1, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
         
        if files == 3:
    
            fig = plt.figure(figsize=(fig_x_length_3, fig_y_length_3))
            fig.text(0.26, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(1, 3, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 3, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 3, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Day 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files == 4:

            fig = plt.figure(figsize=(fig_x_length_4, fig_y_length_4))
            fig.text(0.17, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(2, 2, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Day 4 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(2, 2, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Day 5 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(2, 2, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Day 6 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax3 = plt.subplot(2, 2, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax3.add_feature(GACC, linewidth=2.5, zorder=3)
            ax3.set_title('Day 7 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink) 
            cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        if files >= 5:

            fig = plt.figure(figsize=(fig_x_length_5, fig_y_length_5))
            fig.text(0.40, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2023 | Data Source: NOAA/NWS/NDFD\n               Image Created: ' + local_time.strftime('%a %m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%a %m/%d/%Y %H:%M UTC'), fontweight='bold')
            fig.suptitle("National Weather Service Extended Forecast\nMinimum Relative Humidity & Minimum Relative Humidity Trend", fontweight='bold')
    
            ax0 = plt.subplot(1, 5, 1, projection=mapcrs)
            ax0.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax0.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax0.add_feature(GACC, linewidth=2.5, zorder=3)
            ax0.set_title('Day 3 Forecast\nStart: ' + grb_1_start.strftime('%a %m/%d/%Y 18Z') + '\nEnd: ' + grb_1_end.strftime('%a %m/%d/%Y 06Z'), fontweight='bold')
        
            cs0 = ax0.contourf(lons, lats, grb_1_vals, levels=np.arange(0, 105, 5), cmap=cmap, transform=datacrs)
            cbar0 = fig.colorbar(cs0, shrink=color_table_shrink)
            cbar0.set_label(label="Relative Humidity (%)", fontweight='bold')
        
            ax1 = plt.subplot(1, 5, 2, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax1.add_feature(GACC, linewidth=2.5, zorder=3)
            ax1.set_title('Day 4 Forecast Trend\nStart: ' + grb_2_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_2_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs1 = ax1.contourf(lons, lats, grb_2_vals - grb_1_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar1 = fig.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax2 = plt.subplot(1, 5, 3, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax2.add_feature(GACC, linewidth=2.5, zorder=3)
            ax2.set_title('Day 5 Forecast Trend\nStart: ' + grb_3_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_3_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs2 = ax2.contourf(lons, lats, grb_3_vals - grb_2_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar2 = fig.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax3 = plt.subplot(1, 5, 4, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax3.add_feature(GACC, linewidth=2.5, zorder=3)
            ax3.set_title('Day 6 Forecast Trend\nStart: ' + grb_4_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_4_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs3 = ax3.contourf(lons, lats, grb_4_vals - grb_3_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar3 = fig.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
        
            ax4 = plt.subplot(1, 5, 5, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
            ax4.add_feature(GACC, linewidth=2.5, zorder=3)
            ax4.set_title('Day 7 Forecast Trend\nStart: ' + grb_5_start.strftime('%a %m/%d/%Y %HZ') + '\nEnd: ' + grb_5_end.strftime('%a %m/%d/%Y %HZ'), fontweight='bold')
        
            cs4 = ax4.contourf(lons, lats, grb_5_vals - grb_4_vals, levels=np.arange(-60, 65, 5), cmap=cmap_change, transform=datacrs)
            cbar4 = fig.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Relative Humidity Trend (%)", fontweight='bold')
    
        return fig

