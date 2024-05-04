'''
This file hosts the functions to plot the latest critical fire weather outlook and dry lightning forecast
from the NOAA Storm Prediction Center (SPC). 

This file has 2 classes which are based on the geographical reference perspective:

1) Counties_Perspective: Uses state and county boundaries. 
2) Predictive_Services_Areas_Perspective: Uses Geographic Area Coordination Center (GACC) and 
                                          Predictive Services Areas (PSAs) boundaries. 

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

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from NWS_Generic_Forecast_Graphics import standard
from dateutil import tz

class info:

    def invalid_day():
        error = f"""

        ERROR: You entered an forecast day value out of range. 

        Enter 1 for Day 1. 
        Enter 2 for Day 2
        Enter 3 for Days 3-8
        """
        print(error)


class Counties_Perspective:

    def plot_SPC_7_Day_critical_fire_weather_risk_outlook(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, key_x_position, key_y_position, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth):

        r'''
        This function plots the latest available NOAA/SPC Critical Fire Weather Risk Outlook. 

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
        key_x_position = key_x_position
        key_y_position = key_y_position
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
            
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        try:
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_7_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_7_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.critfireo.bin')

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
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.critfireo.bin')

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
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax1.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax2.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)


        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig3.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax3.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig4.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax4.set_title('Critical Fire Wx Forecast (Day 4)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig5.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax5.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax5.set_title('Critical Fire Wx Forecast (Day 5)\nStart: '+ grb_5_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_5_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig6.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
        ax6.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax6.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        if show_counties == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
        ax6.set_title('Critical Fire Wx Forecast (Day 6)\nStart: '+ grb_6_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_6_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

        if files == 7:

            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig7.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax7.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax7.set_title('Critical Fire Wx Forecast (Day 7)\nStart: '+ grb_7_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_7_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
        
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
    

    def plot_SPC_short_term_critical_fire_weather_risk_outlook(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, key_x_position, key_y_position, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth):
    
        r'''
        This function plots the latest available NOAA/SPC Critical Fire Weather Risk Outlook. 

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
            

        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, count_of_GRIB_files = da.FTP_Downloads.get_latest_short_term_gridded_data(directory_name, 'ds.critfireo.bin')
        
        files = count_of_GRIB_files

        try:
            if grb_1_vals.all() != None:
                test = True

        except Exception as e:
            test = False

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        figs = []
    
        ####################################
        ##### DAY 1 FIGURE #################
        ####################################
        if files == 1:
            
            if test == True:

                grb_1_start = grb_1_start.replace(tzinfo=from_zone)
                grb_1_start = grb_1_start.astimezone(to_zone)
    
                grb_1_end = grb_1_end.replace(tzinfo=from_zone)
                grb_1_end = grb_1_end.astimezone(to_zone)
                
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)

            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
    
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
        ####################################
        ##### DAY 2 FIGURE #################
        ####################################    
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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)

            if test == False: 

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)

                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig1)
            
        ####################################
        ##### DAY 3 FIGURE #################
        ####################################     
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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax2.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)

            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                grb_3_start = grb_3_start.replace(tzinfo=from_zone)
                grb_3_start = grb_3_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                grb_3_end = grb_3_end.replace(tzinfo=from_zone)
                grb_3_end = grb_3_end.astimezone(to_zone)
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

                figs.append(fig)
                figs.append(fig1)
    
        if files > 3:

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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Critical Fire Wx Forecast (Days 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
    
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax2.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig3.set_facecolor('aliceblue')
                fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig3.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax3.set_title('Critical Fire Wx Forecast (Day 4)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)

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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
    
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax2.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)

        return figs


    def plot_SPC_extended_critical_fire_weather_risk_outlook(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, key_x_position, key_y_position, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth):
    
        r'''
        This function plots the latest available NOAA/SPC Critical Fire Weather Risk Outlook. 

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
        '''
        

        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 24
            

        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()


        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, count_of_GRIB_files = da.FTP_Downloads.get_latest_extended_SPC_gridded_data(directory_name, 'ds.critfireo.bin')
        
        files = count_of_GRIB_files

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        figs = []
    
        if files == 4:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Critical Fire Wx Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            

            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Critical Fire Wx Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Critical Fire Wx Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)

        if files == 5:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Critical Fire Wx Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)


            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Critical Fire Wx Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Critical Fire Wx Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)

            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig4.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Critical Fire Wx Forecast (Day 7)\nStart: '+ grb_5_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_5_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)

        if files >= 6:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Critical Fire Wx Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)


            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Critical Fire Wx Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Critical Fire Wx Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig4.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Critical Fire Wx Forecast (Day 7)\nStart: '+ grb_5_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_5_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig5.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Critical Fire Wx Forecast (Day 8)\nStart: '+ grb_6_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_6_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax5.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)

        return figs


    def plot_SPC_short_term_dry_lightning_outlook(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, key_x_position, key_y_position, subplot_title_fontsize, signature_fontsize, key_fontsize, show_counties, show_rivers, state_linewidth, county_linewidth):
    
        r'''
        This function plots the latest available NOAA/SPC Critical Fire Weather Risk Outlook. 

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
        '''
        

        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 24
        state_linewidth = state_linewidth
        county_linewidth = county_linewidth
            

        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, count_of_GRIB_files = da.FTP_Downloads.get_latest_short_term_gridded_data(directory_name, 'ds.dryfireo.bin')
        
        files = count_of_GRIB_files

        try:
            if grb_1_vals.all() != None:
                test = True

        except Exception as e:
            test = False

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        figs = []
    
        ####################################
        ##### DAY 1 FIGURE #################
        ####################################
        if files == 1:
            
            if test == True:

                grb_1_start = grb_1_start.replace(tzinfo=from_zone)
                grb_1_start = grb_1_start.astimezone(to_zone)
    
                grb_1_end = grb_1_end.replace(tzinfo=from_zone)
                grb_1_end = grb_1_end.astimezone(to_zone)
                
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)

            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
    
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
        ####################################
        ##### DAY 2 FIGURE #################
        ####################################    
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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Dry Lightning Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)

            if test == False: 

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)

                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig1)
            
        ####################################
        ##### DAY 3 FIGURE #################
        ####################################     
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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Dry Lightning Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax2.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)

            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                grb_3_start = grb_3_start.replace(tzinfo=from_zone)
                grb_3_start = grb_3_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                grb_3_end = grb_3_end.replace(tzinfo=from_zone)
                grb_3_end = grb_3_end.astimezone(to_zone)
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Dry Lightning Forecast (Day 2)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)

                figs.append(fig)
                figs.append(fig1)
    
        if files > 3:

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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Dry Lightning Forecast (Days 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
    
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax2.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig3.set_facecolor('aliceblue')
                fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig3.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax3.set_title('Dry Lightning Forecast (Day 4)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)

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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax1.set_title('Dry Lightning Forecast (Day 2)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
    
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                if show_counties == True:
                    ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
                ax2.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)

        return figs


    def plot_SPC_extended_dry_lightning_outlook(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, key_x_position, key_y_position, subplot_title_fontsize, signature_fontsize, key_fontsize, show_rivers, show_counties, state_linewidth, county_linewidth):
    
        r'''
        This function plots the latest available NOAA/SPC Critical Fire Weather Risk Outlook. 

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
        '''
        

        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 24
            

        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()


        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, count_of_GRIB_files = da.FTP_Downloads.get_latest_extended_SPC_gridded_data(directory_name, 'ds.dryfireo.bin')
        
        files = count_of_GRIB_files

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        figs = []
    
        if files == 4:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Dry Lightning Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)


            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Dry Lightning Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Dry Lightning Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)

        if files == 5:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Dry Lightning Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)


            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Dry Lightning Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Dry Lightning Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)

            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig4.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Dry Lightning Forecast (Day 7)\nStart: '+ grb_5_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_5_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)

        if files >= 6:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax1.set_title('Dry Lightning Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)


            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax2.set_title('Dry Lightning Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax3.set_title('Dry Lightning Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)

            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig4.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax4.set_title('Dry Lightning Forecast (Day 7)\nStart: '+ grb_5_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_5_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)

            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig5.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.STATES, linewidth=state_linewidth, zorder=5)
            ax5.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            if show_counties == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_linewidth, zorder=4)
            ax5.set_title('Dry Lightning Forecast (Day 8)\nStart: '+ grb_6_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_6_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax5.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)

        return figs
                
        

class Predictive_Services_Areas_Perspective:


    def plot_SPC_7_Day_critical_fire_weather_risk_outlook(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, key_x_position, key_y_position, subplot_title_fontsize, signature_fontsize, key_fontsize, show_rivers):

        r'''
        This function plots the latest available NOAA/SPC Critical Fire Weather Risk Outlook. 

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

                19) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 

        Return: A list of figures for each forecast day.
        '''

        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 24
        key_x_position = key_x_position
        key_y_position = key_y_position
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
            
        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'green')

        try:
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_7_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_7_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.critfireo.bin')

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
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_1_start, grb_2_start, grb_3_start, grb_4_start, grb_5_start, grb_6_start, grb_1_end, grb_2_end, grb_3_end, grb_4_end, grb_5_end, grb_6_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, count = da.FTP_Downloads.get_latest_7_Day_gridded_data(directory_name, 'ds.critfireo.bin')

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
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(GACC, linewidth=2, zorder=5)
        ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax1.add_feature(PSAs, linewidth=1.5, zorder=4)
        ax1.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(GACC, linewidth=2, zorder=5)
        ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax2.add_feature(PSAs, linewidth=1.5, zorder=4)
        ax2.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)


        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig3.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(GACC, linewidth=2, zorder=5)
        ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax3.add_feature(PSAs, linewidth=1.5, zorder=4)
        ax3.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig4.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(GACC, linewidth=2, zorder=5)
        ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax4.add_feature(PSAs, linewidth=1.5, zorder=4)
        ax4.set_title('Critical Fire Wx Forecast (Day 4)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig5.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(GACC, linewidth=2, zorder=5)
        ax5.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax5.add_feature(PSAs, linewidth=1.5, zorder=4)
        ax5.set_title('Critical Fire Wx Forecast (Day 5)\nStart: '+ grb_5_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_5_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
        fig6.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(GACC, linewidth=2, zorder=5)
        ax6.add_feature(cfeature.OCEAN, color='blue', zorder=3)
        ax6.add_feature(cfeature.LAKES, color='blue', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='blue', zorder=3)
        ax6.add_feature(PSAs, linewidth=1.5, zorder=4)
        ax6.set_title('Critical Fire Wx Forecast (Day 6)\nStart: '+ grb_6_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_6_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

        if files == 7:

            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig7.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(GACC, linewidth=2, zorder=5)
            ax7.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax7.add_feature(PSAs, linewidth=1.5, zorder=4)
            ax7.set_title('Critical Fire Wx Forecast (Day 7)\nStart: '+ grb_7_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_7_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
        
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


    def plot_SPC_short_term_critical_fire_weather_risk_outlook(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, key_x_position, key_y_position, subplot_title_fontsize, signature_fontsize, key_fontsize, show_rivers):
    
        r'''
        This function plots the latest available NOAA/SPC Critical Fire Weather Risk Outlook. 

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

                19) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 

        Return: A list of figures for each forecast day.
        '''
        

        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 24
            

        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'green')

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, count_of_GRIB_files = da.FTP_Downloads.get_latest_short_term_gridded_data(directory_name, 'ds.critfireo.bin')
        
        files = count_of_GRIB_files

        try:
            if grb_1_vals.all() != None:
                test = True

        except Exception as e:
            test = False

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        figs = []
    
        ####################################
        ##### DAY 1 FIGURE #################
        ####################################
        if files == 1:
            
            if test == True:

                grb_1_start = grb_1_start.replace(tzinfo=from_zone)
                grb_1_start = grb_1_start.astimezone(to_zone)
    
                grb_1_end = grb_1_end.replace(tzinfo=from_zone)
                grb_1_end = grb_1_end.astimezone(to_zone)
                
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)

            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
    
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
        ####################################
        ##### DAY 2 FIGURE #################
        ####################################    
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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)

            if test == False: 

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)

                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig1)
            
        ####################################
        ##### DAY 3 FIGURE #################
        ####################################     
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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(GACC, linewidth=2, zorder=5)
                ax2.add_feature(PSAs, linewidth=1, zorder=4)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax2.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)

            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                grb_3_start = grb_3_start.replace(tzinfo=from_zone)
                grb_3_start = grb_3_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                grb_3_end = grb_3_end.replace(tzinfo=from_zone)
                grb_3_end = grb_3_end.astimezone(to_zone)
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

                figs.append(fig)
                figs.append(fig1)
    
        if files > 3:

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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Critical Fire Wx Forecast (Days 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
    
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(GACC, linewidth=2, zorder=5)
                ax2.add_feature(PSAs, linewidth=1, zorder=4)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax2.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig3.set_facecolor('aliceblue')
                fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig3.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(GACC, linewidth=2, zorder=5)
                ax3.add_feature(PSAs, linewidth=1, zorder=4)
                ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax3.set_title('Critical Fire Wx Forecast (Day 4)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)

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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Critical Fire Wx Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Critical Fire Wx Forecast (Day 2)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
    
    
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(GACC, linewidth=2, zorder=5)
                ax2.add_feature(PSAs, linewidth=1, zorder=4)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax2.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
                
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)

        return figs


    def plot_SPC_extended_critical_fire_weather_risk_outlook(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, key_x_position, key_y_position, subplot_title_fontsize, signature_fontsize, key_fontsize, show_rivers):
    
        r'''
        This function plots the latest available NOAA/SPC Critical Fire Weather Risk Outlook. 

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

                19) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 

        Return: A list of figures for each forecast day.
        '''
        

        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 24
            

        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'green')

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, count_of_GRIB_files = da.FTP_Downloads.get_latest_extended_SPC_gridded_data(directory_name, 'ds.critfireo.bin')
        
        files = count_of_GRIB_files

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        figs = []
    
        if files == 4:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(GACC, linewidth=2, zorder=5)
            ax.add_feature(PSAs, linewidth=1, zorder=4)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=2, zorder=5)
            ax1.add_feature(PSAs, linewidth=1, zorder=4)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax1.set_title('Critical Fire Wx Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            

            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=2, zorder=5)
            ax2.add_feature(PSAs, linewidth=1, zorder=4)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax2.set_title('Critical Fire Wx Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=2, zorder=5)
            ax3.add_feature(PSAs, linewidth=1, zorder=4)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax3.set_title('Critical Fire Wx Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)

        if files == 5:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(GACC, linewidth=2, zorder=5)
            ax.add_feature(PSAs, linewidth=1, zorder=4)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=2, zorder=5)
            ax1.add_feature(PSAs, linewidth=1, zorder=4)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax1.set_title('Critical Fire Wx Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)


            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=2, zorder=5)
            ax2.add_feature(PSAs, linewidth=1, zorder=4)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax2.set_title('Critical Fire Wx Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=2, zorder=5)
            ax3.add_feature(PSAs, linewidth=1, zorder=4)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax3.set_title('Critical Fire Wx Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)

            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig4.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=2, zorder=5)
            ax4.add_feature(PSAs, linewidth=1, zorder=4)
            ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax4.set_title('Critical Fire Wx Forecast (Day 7)\nStart: '+ grb_5_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_5_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)

        if files >= 6:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(GACC, linewidth=2, zorder=5)
            ax.add_feature(PSAs, linewidth=1, zorder=4)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax.set_title('Critical Fire Wx Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=2, zorder=5)
            ax1.add_feature(PSAs, linewidth=1, zorder=4)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax1.set_title('Critical Fire Wx Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)


            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=2, zorder=5)
            ax2.add_feature(PSAs, linewidth=1, zorder=4)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax2.set_title('Critical Fire Wx Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=2, zorder=5)
            ax3.add_feature(PSAs, linewidth=1, zorder=4)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax3.set_title('Critical Fire Wx Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig4.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=2, zorder=5)
            ax4.add_feature(PSAs, linewidth=1, zorder=4)
            ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax4.set_title('Critical Fire Wx Forecast (Day 7)\nStart: '+ grb_5_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_5_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig5.text(key_x_position, key_y_position, 'Key:\nElevated - Yellow\nCritical - Orange\nExtreme - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=2, zorder=5)
            ax5.add_feature(PSAs, linewidth=1, zorder=4)
            ax5.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax5.set_title('Critical Fire Wx Forecast (Day 8)\nStart: '+ grb_6_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_6_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax5.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(4, 12, 2), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)

        return figs



    def plot_SPC_short_term_dry_lightning_outlook(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, key_x_position, key_y_position, subplot_title_fontsize, signature_fontsize, key_fontsize, show_rivers):
    
        r'''
        This function plots the latest available NOAA/SPC Critical Fire Weather Risk Outlook. 

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

                19) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 

        Return: A list of figures for each forecast day.
        '''
        

        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 24
            

        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'green')

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, count_of_GRIB_files = da.FTP_Downloads.get_latest_short_term_gridded_data(directory_name, 'ds.dryfireo.bin')
        
        files = count_of_GRIB_files

        try:
            if grb_1_vals.all() != None:
                test = True

        except Exception as e:
            test = False

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        figs = []
    
        ####################################
        ##### DAY 1 FIGURE #################
        ####################################
        if files == 1:
            
            if test == True:

                grb_1_start = grb_1_start.replace(tzinfo=from_zone)
                grb_1_start = grb_1_start.astimezone(to_zone)
    
                grb_1_end = grb_1_end.replace(tzinfo=from_zone)
                grb_1_end = grb_1_end.astimezone(to_zone)
                
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)

            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
    
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
        ####################################
        ##### DAY 2 FIGURE #################
        ####################################    
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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Dry Lightning Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)

            if test == False: 

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)

                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig1)
            
        ####################################
        ##### DAY 3 FIGURE #################
        ####################################     
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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Dry Lightning Forecast (Day 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(GACC, linewidth=2, zorder=5)
                ax2.add_feature(PSAs, linewidth=1, zorder=4)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax2.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)

            if test == False:

                grb_2_start = grb_2_start.replace(tzinfo=from_zone)
                grb_2_start = grb_2_start.astimezone(to_zone)
                grb_3_start = grb_3_start.replace(tzinfo=from_zone)
                grb_3_start = grb_3_start.astimezone(to_zone)
                
                grb_2_end = grb_2_end.replace(tzinfo=from_zone)
                grb_2_end = grb_2_end.astimezone(to_zone)
                grb_3_end = grb_3_end.replace(tzinfo=from_zone)
                grb_3_end = grb_3_end.astimezone(to_zone)
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Dry Lightning Forecast (Day 2)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)

                figs.append(fig)
                figs.append(fig1)
    
        if files > 3:

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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Dry Lightning Forecast (Days 2)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
    
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(GACC, linewidth=2, zorder=5)
                ax2.add_feature(PSAs, linewidth=1, zorder=4)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax2.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig3.set_facecolor('aliceblue')
                fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig3.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
                ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax3.add_feature(GACC, linewidth=2, zorder=5)
                ax3.add_feature(PSAs, linewidth=1, zorder=4)
                ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax3.set_title('Dry Lightning Forecast (Day 4)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs3 = ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)

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
    
                fig = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig.set_facecolor('aliceblue')
                fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(GACC, linewidth=2, zorder=5)
                ax.add_feature(PSAs, linewidth=1, zorder=4)
                ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax.set_title('Dry Lightning Forecast (Day 1)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs = ax.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig1.set_facecolor('aliceblue')
                fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
                
                ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
                ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax1.add_feature(GACC, linewidth=2, zorder=5)
                ax1.add_feature(PSAs, linewidth=1, zorder=4)
                ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax1.set_title('Dry Lightning Forecast (Day 2)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs1 = ax1.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
    
    
                fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig2.set_facecolor('aliceblue')
                fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
                fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
                ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
                ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax2.add_feature(GACC, linewidth=2, zorder=5)
                ax2.add_feature(PSAs, linewidth=1, zorder=4)
                ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
                ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
                ax2.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs2 = ax2.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
                
                figs.append(fig)
                figs.append(fig1)
                figs.append(fig2)

        return figs

    def plot_SPC_extended_dry_lightning_outlook(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, signature_x_position, signature_y_position, key_x_position, key_y_position, subplot_title_fontsize, signature_fontsize, key_fontsize, show_rivers):
    
        r'''
        This function plots the latest available NOAA/SPC Critical Fire Weather Risk Outlook. 

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

                19) show_rivers (Boolean) - If set to True, rivers will display. If set to False, rivers will not display. 

        Return: A list of figures for each forecast day.
        '''
        

        local_time, utc_time = standard.plot_creation_time()
        grid_time_interval = 24
            

        mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
        datacrs = ccrs.PlateCarree()

        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'green')

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, count_of_GRIB_files = da.FTP_Downloads.get_latest_extended_SPC_gridded_data(directory_name, 'ds.dryfireo.bin')
        
        files = count_of_GRIB_files

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        figs = []
    
        if files == 4:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(GACC, linewidth=2, zorder=5)
            ax.add_feature(PSAs, linewidth=1, zorder=4)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=2, zorder=5)
            ax1.add_feature(PSAs, linewidth=1, zorder=4)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax1.set_title('Dry Lightning Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)


            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=2, zorder=5)
            ax2.add_feature(PSAs, linewidth=1, zorder=4)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax2.set_title('Dry Lightning Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=2, zorder=5)
            ax3.add_feature(PSAs, linewidth=1, zorder=4)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax3.set_title('Dry Lightning Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)

        if files == 5:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(GACC, linewidth=2, zorder=5)
            ax.add_feature(PSAs, linewidth=1, zorder=4)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=2, zorder=5)
            ax1.add_feature(PSAs, linewidth=1, zorder=4)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax1.set_title('Dry Lightning Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)


            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=2, zorder=5)
            ax2.add_feature(PSAs, linewidth=1, zorder=4)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax2.set_title('Dry Lightning Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=2, zorder=5)
            ax3.add_feature(PSAs, linewidth=1, zorder=4)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax3.set_title('Dry Lightning Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)

            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig4.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=2, zorder=5)
            ax4.add_feature(PSAs, linewidth=1, zorder=4)
            ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax4.set_title('Dry Lightning Forecast (Day 7)\nStart: '+ grb_5_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_5_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(1, 11, 1), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)

        if files >= 6:

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

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig.set_facecolor('aliceblue')
            fig.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(GACC, linewidth=2, zorder=5)
            ax.add_feature(PSAs, linewidth=1, zorder=4)
            ax.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax.set_title('Dry Lightning Forecast (Day 3)\nStart: '+ grb_1_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_1_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
            
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig1.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=2, zorder=5)
            ax1.add_feature(PSAs, linewidth=1, zorder=4)
            ax1.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax1.set_title('Dry Lightning Forecast (Day 4)\nStart: '+ grb_2_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_2_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax1.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)


            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig2.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
        
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=2, zorder=5)
            ax2.add_feature(PSAs, linewidth=1, zorder=4)
            ax2.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax2.set_title('Dry Lightning Forecast (Day 5)\nStart: '+ grb_3_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_3_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax2.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig3.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=2, zorder=5)
            ax3.add_feature(PSAs, linewidth=1, zorder=4)
            ax3.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax3.set_title('Dry Lightning Forecast (Day 6)\nStart: '+ grb_4_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_4_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax3.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)

            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig4.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=2, zorder=5)
            ax4.add_feature(PSAs, linewidth=1, zorder=4)
            ax4.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax4.set_title('Dry Lightning Forecast (Day 7)\nStart: '+ grb_5_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_5_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax4.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)

            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Data Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
            fig5.text(key_x_position, key_y_position, 'Key:\nIsolated - Yellow\nScattered - Red', fontsize=key_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=2, zorder=5)
            ax5.add_feature(PSAs, linewidth=1, zorder=4)
            ax5.add_feature(cfeature.OCEAN, color='blue', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='blue', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='blue', zorder=3)
            ax5.set_title('Dry Lightning Forecast (Day 8)\nStart: '+ grb_6_start.strftime('%m/%d %H:00 Local') + ' | End: '+ grb_6_end.strftime('%m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            ax5.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(4, 10, 2), cmap='YlOrRd', transform=datacrs)

            figs.append(fig)
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)

        return figs

