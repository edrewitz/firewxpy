'''
This file hosts all the plotting functions for the National Weather Service Forecast Graphics.

Each class hosts a variety of plotting functions to analyze a particular weather element. 

Classes in this file:
    1) Relative Humidity 
    2) Temperature

 This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS

'''

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
import colormaps
import os
import xarray as xr
import settings
import standard

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from dateutil import tz
from matplotlib.patheffects import withStroke
from calc import scaling, unit_conversion

class relative_humidity:

    '''
    This class holds all the plotting functions for the National Weather Service Relative Humidity Forecasts:

    1) Poor Overnight Recovery Forecast 

    2) Excellent Overnight Recovery Forecast

    3) Maximum Relative Humidity Forecast

    4) Maximum Relative Humidity Trend Forecast

    5) Low Minimum Relative Humidity Forecast

    6) Minimum Relative Humidity Forecast

    7) Minimum Relative Humidity Trend Forecast


    '''

    def plot_poor_overnight_recovery_relative_humidity_forecast(poor_overnight_recovery_rh_threshold, contour_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None):
    
        r'''
        This function plots the latest available NOAA/NWS Poor Overnight Recovery RH Forecast. 
    
        Required Arguments: 1) poor_overnight_recovery_rh_threshold (Integer) - The relative humidity threshold for 
                               a poor overnight relative humidity recovery. This is the upper bound of values shaded. 
                               (i.e. a value of 30 means all values less than 30% get shaded). 

                            2) contour_step (Integer) - The contour interval. (i.e. a value of 5 means the RH gets contoured every 5%). 

        Optional Arguments: 1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 
    
                            2) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 
    
                            3) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 
    
                            4) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.
              
                            5) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            6) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            7) signature_x_position (Integer or Float) - The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            8) signature_y_position (Integer or Float) - The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            9) color_table_shrink (Integer or Float) - This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." The default setting is None. 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            10) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            11) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            12) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            13) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            14) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers. 
    
                            15) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide state borders. 

                            16) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide county borders. 

                            17) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            17) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            18) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            19) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            20) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            21) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            22) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            23) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            24) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            25) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
        Return: A list of figures for each forecast day. 
        '''
    
    
        local_time, utc_time = standard.plot_creation_time()
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
        contour_step = contour_step
        poor_overnight_recovery_rh_threshold = poor_overnight_recovery_rh_threshold
        poor_overnight_recovery_rh_thresh = poor_overnight_recovery_rh_threshold + contour_step
        file_path = file_path
        ds = data_array
        count_short = count_short
        count_extended = count_extended
        directory_name = directory_name
        state = state
    
    
        contour_step = contour_step
        ds = data_array
    
        cmap = colormaps.low_relative_humidity_colormap()
    
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'poor recovery')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'poor recovery')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxrh.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.maxrh.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.maxrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        else:
            pass    
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'maxrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            mask = (df1['maxrh'] <= poor_overnight_recovery_rh_threshold)
        
            df2 = vals[1]
            mask = (df2['maxrh'] <= poor_overnight_recovery_rh_threshold)    
        
            df3 = vals[2]
            mask = (df3['maxrh'] <= poor_overnight_recovery_rh_threshold)
            
            df4 = vals[3]
            mask = (df4['maxrh'] <= poor_overnight_recovery_rh_threshold)
            
            df5 = vals[4]
            mask = (df5['maxrh'] <= poor_overnight_recovery_rh_threshold)
            
            df6 = vals[5]
            mask = (df6['maxrh'] <= poor_overnight_recovery_rh_threshold)
        
            if test_7 == True:
                df7 = vals[6]
                mask = (df7['maxrh'] <= poor_overnight_recovery_rh_threshold)
            else:
                pass
    
            no_vals = False
        except Exception as e:
            no_vals = True
            
        files = count
    
        figs = [] 
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig1.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 1]', fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn1.plot_parameter('C', df1['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass                                                                 
    
        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig2.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 2]', fontsize=title_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn2.plot_parameter('C', df2['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass   
    
        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig3.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 3]', fontsize=title_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn3.plot_parameter('C', df3['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass   
    
        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig4.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 4]', fontsize=title_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn4.plot_parameter('C', df4['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass   
    
        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig5.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 5]', fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn5.plot_parameter('C', df5['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass   
    
        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig6.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 6]', fontsize=title_fontsize, fontweight='bold')
        
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn6.plot_parameter('C', df6['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass   
    
        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
        cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig7.suptitle('National Weather Service Forecast\nPoor Overnight RH Recovery (Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%) [Night 7]', fontsize=title_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(0, poor_overnight_recovery_rh_thresh, contour_step), cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn7.plot_parameter('C', df7['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
            cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
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
    
    
    
    def plot_excellent_overnight_recovery_relative_humidity_forecast(excellent_overnight_recovery_rh_threshold, contour_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None):
    
        r'''
        This function plots the latest available NOAA/NWS Excellent Overnight Recovery RH Forecast. 
    
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
        state_border_linewidth = state_border_linewidth
        contour_step = contour_step
        excellent_overnight_recovery_rh_threshold = excellent_overnight_recovery_rh_threshold
        file_path = file_path
        ds = data_array
        count_short = count_short
        count_extended = count_extended
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
        cmap = colormaps.excellent_recovery_colormap()
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'excellent recovery')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'excellent recovery')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxrh.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.maxrh.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.maxrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)     
    
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
        else:
            pass
    
        
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'maxrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
        
            df2 = vals[1] 
        
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]
        
        
            if test_7 == True:
                df7 = vals[6]
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
    
        files = count
    
        figs = [] 
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig1.suptitle('National Weather Service Forecast\nExcellent Overnight RH Recovery (Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%) [Night 1]', fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(excellent_overnight_recovery_rh_threshold, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn1.plot_parameter('C', df1['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass     
    
        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig2.suptitle('National Weather Service Forecast\nExcellent Overnight RH Recovery (Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%) [Night 2]', fontsize=title_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(excellent_overnight_recovery_rh_threshold, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn2.plot_parameter('C', df2['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass  
    
        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig3.suptitle('National Weather Service Forecast\nExcellent Overnight RH Recovery (Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%) [Night 3]', fontsize=title_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(excellent_overnight_recovery_rh_threshold, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn3.plot_parameter('C', df3['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass  
    
        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig4.suptitle('National Weather Service Forecast\nExcellent Overnight RH Recovery (Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%) [Night 4]', fontsize=title_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(excellent_overnight_recovery_rh_threshold, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn4.plot_parameter('C', df4['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass  
    
        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig5.suptitle('National Weather Service Forecast\nExcellent Overnight RH Recovery (Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%) [Night 5]', fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(excellent_overnight_recovery_rh_threshold, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn5.plot_parameter('C', df5['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass  
    
        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig6.suptitle('National Weather Service Forecast\nExcellent Overnight RH Recovery (Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%) [Night 6]', fontsize=title_fontsize, fontweight='bold')
        
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(excellent_overnight_recovery_rh_threshold, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn6.plot_parameter('C', df6['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass  
    
        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
        cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig7.suptitle('National Weather Service Forecast\nExcellent Overnight RH Recovery (Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%) [Night 7]', fontsize=title_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(excellent_overnight_recovery_rh_threshold, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
        
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
        
                stn7.plot_parameter('C', df7['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
            else:
                pass  
    
            cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
            cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
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
    
    
    def plot_maximum_relative_humidity_forecast(contour_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None):
    
        r'''
        This function plots the latest available NOAA/NWS Maximum RH Forecast. 
    
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
    
        contour_step = contour_step
        file_path = file_path
        ds = data_array
        count_short = count_short
        count_extended = count_extended
        cmap = colormaps.relative_humidity_colormap()
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'maxrh')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'maxrh')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxrh.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.maxrh.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.maxrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)
            
        if file_path != None:
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)    
    
        
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        
        else:
            pass    
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'maxrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
        
            df2 = vals[1] 
        
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]
        
            if test_7 == True:
                df7 = vals[6]
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
            
        files = count
    
        figs = [] 
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig1.suptitle('National Weather Service Forecast\nMaximum Relative Humidity [Night 1]', fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn1.plot_parameter('C', df1['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass     
    
        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig2.suptitle('National Weather Service Forecast\nMaximum Relative Humidity [Night 2]', fontsize=title_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn2.plot_parameter('C', df2['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass     
    
        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig3.suptitle('National Weather Service Forecast\nMaximum Relative Humidity [Night 3]', fontsize=title_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn3.plot_parameter('C', df3['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass     
    
        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig4.suptitle('National Weather Service Forecast\nMaximum Relative Humidity [Night 4]', fontsize=title_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn4.plot_parameter('C', df4['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass     
    
        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig5.suptitle('National Weather Service Forecast\nMaximum Relative Humidity [Night 5]', fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn5.plot_parameter('C', df5['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass     
    
        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig6.suptitle('National Weather Service Forecast\nMaximum Relative Humidity [Night 6]', fontsize=title_fontsize, fontweight='bold')
        
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn6.plot_parameter('C', df6['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass     
    
        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
        cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig7.suptitle('National Weather Service Forecast\nMaximum Relative Humidity [Night 7]', fontsize=title_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
        
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
        
                stn7.plot_parameter('C', df7['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
            else:
                pass     
    
            cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
            cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
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
    
    
    
    def plot_maximum_relative_humidity_trend_forecast(contour_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None):
    
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
        file_path = file_path
        ds = data_array
        count_short = count_short
        count_extended = count_extended
        contour_step = contour_step
    
        cmap = colormaps.relative_humidity_change_colormap()
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'maxrh trend')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'maxrh trend')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxrh.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.maxrh.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.maxrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)        
    
    
        diff1 = grb_2_vals - grb_1_vals
        diff2 = grb_3_vals - grb_2_vals
        diff3 = grb_4_vals - grb_3_vals
        diff4 = grb_5_vals - grb_4_vals
        diff5 = grb_6_vals - grb_5_vals
    
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
            diff6 = grb_7_vals - grb_6_vals
        else:
            pass
    
        try:    
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'maxrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
        
            df2 = vals[1] 
        
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]
        
            df2['diff'] = df2['maxrh'] - df1['maxrh']
            df3['diff'] = df3['maxrh'] - df2['maxrh']
            df4['diff'] = df4['maxrh'] - df3['maxrh']
            df5['diff'] = df5['maxrh'] - df4['maxrh']
            df6['diff'] = df6['maxrh'] - df5['maxrh']
        
            
            if test_7 == True:
                df7 = vals[6]
                df7['diff'] = df7['maxrh'] - df6['maxrh']
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
            
        files = count
    
        figs = [] 
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig1.suptitle('National Weather Service Forecast\nMaximum Relative Humidity Trend [Night 2]', fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both', alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn1.plot_parameter('C', df2['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass     
    
        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Maximum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig2.suptitle('National Weather Service Forecast\nMaximum Relative Humidity Trend [Night 3]', fontsize=title_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both', alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn2.plot_parameter('C', df3['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass 
    
        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Maximum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig3.suptitle('National Weather Service Forecast\nMaximum Relative Humidity Trend [Night 4]', fontsize=title_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both', alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn3.plot_parameter('C', df4['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass 
    
        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Maximum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig4.suptitle('National Weather Service Forecast\nMaximum Relative Humidity Trend [Night 5]', fontsize=title_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both', alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn4.plot_parameter('C', df5['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass 
    
        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Maximum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig5.suptitle('National Weather Service Forecast\nMaximum Relative Humidity Trend [Night 6]', fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn5.plot_parameter('C', df6['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass 
    
        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Maximum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig7.suptitle('National Weather Service Forecast\nMaximum Relative Humidity Trend [Night 7]', fontsize=title_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both')
    
            if show_sample_points == True and no_vals == False:
        
                stn7 = mpplots.StationPlot(ax7, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
        
                stn7.plot_parameter('C', df7['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
            else:
                pass 
    
            cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
            cbar7.set_label(label="Maximum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
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
    
    def plot_low_minimum_relative_humidity_forecast(low_minimum_rh_threshold, contour_step,  western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None):
    
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
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
        decimate = decimate
        contour_step = contour_step
        low_minimum_rh_threshold = low_minimum_rh_threshold
        low_minimum_rh_thresh = low_minimum_rh_threshold + contour_step
        file_path = file_path  
        ds = data_array
        count_short = count_short
        count_extended = count_extended
    
        cmap = colormaps.low_relative_humidity_colormap()
        
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'low minrh')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'low minrh')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
            
    
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.minrh.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.minrh.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.minrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.minrh.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
            
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        else:
            pass
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'minrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
    
            df2 = vals[1] 
    
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]
    
            if test_7 == True:
                df7 = vals[6]
            else:
                pass
    
    
            no_vals = False
    
        except Exception as ee:
            try:
                vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'unknown', count, True, count_short, count_extended, discard)
                
                df1 = vals[0]
        
                df2 = vals[1]
        
                df3 = vals[2]
                
                df4 = vals[3]
        
                df5 = vals[4]
                
                df6 = vals[5]
        
        
                if test_7 == True:
                    df7 = vals[6]
                else:
                    pass
    
    
                no_vals = False
            except Exception as g:
                no_vals = True
            
        files = count
    
        
        figs = [] 
    
        try:
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 1]', fontsize=title_fontsize, fontweight='bold')
    
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn1.plot_parameter('C', df1['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass     
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 2]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn2.plot_parameter('C', df2['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 3]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn3.plot_parameter('C', df3['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 4]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn4.plot_parameter('C', df4['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn5.plot_parameter('C', df5['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig6.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn6.plot_parameter('C', df6['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
                if show_sample_points == True and no_vals == False:
        
                    stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
        
                    stn7.plot_parameter('C', df7['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                else:
                    pass   
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
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
    
        except Exception as ff:
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 1]', fontsize=title_fontsize, fontweight='bold')
    
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn1.plot_parameter('C', df1['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass     
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 2]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn2.plot_parameter('C', df2['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 3]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn3.plot_parameter('C', df3['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 4]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn4.plot_parameter('C', df4['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn5.plot_parameter('C', df5['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig6.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn6.plot_parameter('C', df6['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nExceptionally Low Minimum RH (Min RH <= ' +str(low_minimum_rh_threshold) + '%) [Day 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(0, low_minimum_rh_thresh, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
                if show_sample_points == True and no_vals == False:
        
                    stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
        
                    stn7.plot_parameter('C', df7['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                else:
                    pass   
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
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
    
    
    def plot_minimum_relative_humidity_forecast(contour_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None):
    
        r'''
        This function plots the latest available NOAA/NWS Minimum RH Forecast. 
    
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
        contour_step = contour_step
        ds = data_array
        cmap = colormaps.relative_humidity_colormap()
    
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'minrh')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'minrh')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
            
        if file_path == None:
            
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.minrh.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.minrh.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.minrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.minrh.bin', 12, False, count_short, count_extended, directory_name)
    
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        else:
            pass
    
        try:
            
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'minrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
    
            df2 = vals[1] 
    
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]   
    
            if test_7 == True:
    
                df7 = vals[6]
    
            else:
                pass
    
            no_vals = False
        except Exception as ee:
            try:
                vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'unknown', count, True, count_short, count_extended, discard)
                
                df1 = vals[0]
        
                df2 = vals[1]
        
                df3 = vals[2]
                
                df4 = vals[3]
        
                df5 = vals[4]
                
                df6 = vals[5]
           
        
                if test_7 == True:
        
                    df7 = vals[6]
        
                else:
                    pass
    
                no_vals = False
            except Exception as g:    
                no_vals = True
        
            
        files = count
    
        figs = [] 
        try:
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 1]', fontsize=title_fontsize, fontweight='bold')
    
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn1.plot_parameter('C', df1['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass     
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 2]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn2.plot_parameter('C', df2['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 3]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn3.plot_parameter('C', df3['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 4]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn4.plot_parameter('C', df4['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn5.plot_parameter('C', df5['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig6.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn6.plot_parameter('C', df6['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
                if show_sample_points == True and no_vals == False:
        
                    stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
        
                    stn7.plot_parameter('C', df7['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                else:
                    pass   
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
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
    
        except Exception as ff:
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig1.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 1]', fontsize=title_fontsize, fontweight='bold')
    
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            mask = (lons_1 <= -110)
                
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn1.plot_parameter('C', df1['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass     
    
            cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
            cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig2.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 2]', fontsize=title_fontsize, fontweight='bold')
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn2.plot_parameter('C', df2['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
            cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig3.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 3]', fontsize=title_fontsize, fontweight='bold')
        
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn3.plot_parameter('C', df3['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
            cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig4.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 4]', fontsize=title_fontsize, fontweight='bold')
            
            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn4.plot_parameter('C', df4['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
            cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig5.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 5]', fontsize=title_fontsize, fontweight='bold')
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn5.plot_parameter('C', df5['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
            cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig6.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 6]', fontsize=title_fontsize, fontweight='bold')
            
            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
                stn6.plot_parameter('C', df6['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
            else:
                pass   
    
            cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
            cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
                fig7.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Forecast [Day 7]', fontsize=title_fontsize, fontweight='bold')
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
                if show_sample_points == True and no_vals == False:
        
                    stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
        
                    stn7.plot_parameter('C', df7['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                else:
                    pass   
    
                cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
                cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
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
    
    
    
    def plot_minimum_relative_humidity_trend_forecast(contour_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None):
    
        r'''
        This function plots the latest available NOAA/NWS Minimum RH Trend Forecast. 
    
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
        contour_step = contour_step
        ds = data_array
    
        cmap = colormaps.relative_humidity_change_colormap()
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'minrh trend')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'minrh trend')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
            
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.minrh.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.minrh.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.minrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.minrh.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended)
    
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False      
        
        diff1 = grb_2_vals - grb_1_vals
        diff2 = grb_3_vals - grb_2_vals
        diff3 = grb_4_vals - grb_3_vals
        diff4 = grb_5_vals - grb_4_vals
        diff5 = grb_6_vals - grb_5_vals
    
    
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
    
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)  
            
            diff6 = grb_7_vals - grb_6_vals
        else:
            pass
    
        
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'minrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
    
            df2 = vals[1] 
    
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]
    
            df2['diff'] = df2['minrh'] - df1['minrh']
            df3['diff'] = df3['minrh'] - df2['minrh']
            df4['diff'] = df4['minrh'] - df3['minrh']
            df5['diff'] = df5['minrh'] - df4['minrh']
            df6['diff'] = df6['minrh'] - df5['minrh']
    
            if test_7 == True:
                df7 = vals[6]
                df7['diff'] = df7['minrh'] - df6['minrh']
            else:
                pass
        
            no_vals = False
        except Exception as ee:
            try:
                vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'unknown', count, True, count_short, count_extended, discard)
                
                df1 = vals[0]
        
                df2 = vals[1]
        
                df3 = vals[2]
                
                df4 = vals[3]
        
                df5 = vals[4]
                
                df6 = vals[5]
        
                diff1 = grb_2_vals - grb_1_vals
                diff2 = grb_3_vals - grb_2_vals
                diff3 = grb_4_vals - grb_3_vals
                diff4 = grb_5_vals - grb_4_vals
                diff5 = grb_6_vals - grb_5_vals
        
                df2['diff'] = df2['unknown'] - df1['unknown']
                df3['diff'] = df3['unknown'] - df2['unknown']
                df4['diff'] = df4['unknown'] - df3['unknown']
                df5['diff'] = df5['unknown'] - df4['unknown']
                df6['diff'] = df6['unknown'] - df5['unknown']
        
                if test_7 == True:
                    df7 = vals[6]
                    df7['diff'] = df7['unknown'] - df6['unknown']
                else:
                    pass
    
                no_vals = False
            except Exception as g:
                no_vals = True
            
        files = count
    
        figs = [] 
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig1.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Trend [Day 2]', fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn1.plot_parameter('C', df2['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass   
    
        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Minimum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig2.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Trend [Day 3]', fontsize=title_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn2.plot_parameter('C', df3['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass   
    
        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Minimum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig3.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Trend [Day 4]', fontsize=title_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn3.plot_parameter('C', df4['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass   
    
        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Minimum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig4.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Trend [Day 5]', fontsize=title_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn4.plot_parameter('C', df5['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass   
    
        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Minimum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig5.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Trend [Day 6]', fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
            stn5.plot_parameter('C', df6['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
        else:
            pass   
    
        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Minimum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig7.suptitle('National Weather Service Forecast\nMinimum Relative Humidity Trend [Day 7]', fontsize=title_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-50, 50 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, extend='both')
    
            if show_sample_points == True and no_vals == False:
        
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
        
                stn7.plot_parameter('C', df7['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
            else:
                pass   
    
            cbar7 = fig7.colorbar(cs7, shrink=color_table_shrink)
            cbar7.set_label(label="Minimum Relative Humidity Trend (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
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

class temperature: 

    r'''
    This class holds all the plotting functions for the National Weather Service Temperature Forecasts:

    1) Extreme Heat Forecast

    2) Extremely Warm Low Temperature Forecast

    3) Frost/Freeze Forecast 

    4) Maximum Temperature Forecast

    5) Minimum Temperature Forecast

    6) Maximum Temperature Trend Forecast

    7) Minimum Temperature Trend Forecast

    '''


    def plot_extreme_heat_forecast(start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None): 
    
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
    
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
        state = state
        gacc_region = gacc_region
        ds = data_array
    
        temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
        temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        local_time, utc_time = standard.plot_creation_time()
    
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'extreme heat')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'extreme heat')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxt.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.maxt.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.maxt.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
        grb_1_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_1_vals)
        grb_2_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_2_vals)
        grb_3_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_3_vals)
        grb_4_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_4_vals)
        grb_5_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_5_vals)
        grb_6_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_6_vals)
        
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
            grb_7_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_7_vals)
        else:
            pass
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmax', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmax'])
        
            df2 = vals[1]
            df2['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmax'])         
        
            df3 = vals[2]
            df3['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmax'])
            
            df4 = vals[3]
            df4['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmax'])
        
            df5 = vals[4]
            df5['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmax'])
            
            df6 = vals[5]
            df6['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmax'])
    
            if test_7 == True:
                df7 = vals[6]
                df7['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmax'])
            else:
                pass
    
            no_vals = False
    
        except Exception as g:
            no_vals = True
            
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
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df1['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
    
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
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
    
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
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
    
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
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
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
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
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
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
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
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
    
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

    def plot_extremely_warm_low_temperature_forecast(start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None): 
    
        r'''
        THIS FUNCTION PLOTS AREAS WHERE THERE IS EXTREME HEAT IN THE FORECAST. DURING THE WARM SEASON (APRIL - OCTOBER) EXTREME HEAT IS DEFINED AS THE Minimum TEMPERATURE >= 120F AND COLD SEASON (NOVEMBER - MARCH) Minimum TEMPERATURE >= 100F AND IS BASED ON THE NATIONAL WEATHER SERVICE FORECAST
    
        IN ORDER FOR THIS FUNCTION TO WORK PROPERLY, USER NEEDS TO MAKE SURE THEIR PARAMETER IS SET TO THE Minimum TEMPERATURE GRIDS
    
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
    
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
        state = state
        gacc_region = gacc_region
        ds = data_array
    
        temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
        temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        local_time, utc_time = standard.plot_creation_time()
    
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'warm lows')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'warm lows')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.mint.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.mint.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.mint.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
        grb_1_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_1_vals)
        grb_2_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_2_vals)
        grb_3_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_3_vals)
        grb_4_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_4_vals)
        grb_5_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_5_vals)
        grb_6_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_6_vals)
        
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
            grb_7_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_7_vals)
        else:
            pass
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmin', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmin'])
        
            df2 = vals[1]
            df2['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmin'])         
        
            df3 = vals[2]
            df3['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmin'])
            
            df4 = vals[3]
            df4['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmin'])
        
            df5 = vals[4]
            df5['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmin'])
            
            df6 = vals[5]
            df6['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmin'])
    
            if test_7 == True:
                df7 = vals[6]
                df7['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmin'])
            else:
                pass
    
            no_vals = False
    
        except Exception as g:
            no_vals = True
            
        files = count
    
        figs = [] 
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            fig1.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 1]", fontsize=title_fontsize, fontweight='bold')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            fig1.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 1]", fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df1['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
    
        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            fig2.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 2]", fontsize=title_fontsize, fontweight='bold')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            fig2.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 2]", fontsize=title_fontsize, fontweight='bold')
    
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
    
        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            fig3.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 3]", fontsize=title_fontsize, fontweight='bold')
    
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            fig3.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 3]", fontsize=title_fontsize, fontweight='bold')
    
        ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
    
        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            fig4.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 4]", fontsize=title_fontsize, fontweight='bold')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            fig4.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 4]", fontsize=title_fontsize, fontweight='bold')
    
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            fig5.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 5]", fontsize=title_fontsize, fontweight='bold')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            fig5.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 5]", fontsize=title_fontsize, fontweight='bold')
    
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            fig6.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F)) [Day 6]", fontsize=title_fontsize, fontweight='bold')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            fig6.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 6]", fontsize=title_fontsize, fontweight='bold')
    
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
        cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                fig7.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F) [Day 7]", fontsize=title_fontsize, fontweight='bold')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                fig7.suptitle("National Weather Service Forecast\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F)) [Day 7]", fontsize=title_fontsize, fontweight='bold')
        
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, transform=datacrs, extend='max')
    
    
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
    
    def plot_frost_freeze_forecast(temperature_bottom_bound, temp_scale_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None): 
    
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
        decimate = decimate
        
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
        state = state
        gacc_region = gacc_region
    
        cmap = colormaps.cool_temperatures_colormap()
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        local_time, utc_time = standard.plot_creation_time()
    
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'frost freeze')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'frost freeze')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.mint.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.mint.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.mint.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
        grb_1_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_1_vals)
        grb_2_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_2_vals)
        grb_3_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_3_vals)
        grb_4_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_4_vals)
        grb_5_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_5_vals)
        grb_6_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_6_vals)
    
    
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)    
    
            grb_7_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_7_vals)
        else:
            pass
            
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmin', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmin'])
        
            df2 = vals[1]
            df2['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmin'])
        
            df3 = vals[2]
            df3['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmin'])
            
            df4 = vals[3]
            df4['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmin'])
            
            df5 = vals[4]
            df5['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmin'])
            
            df6 = vals[5]
            df6['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmin'])
    
    
            if test_7 == True:
                df7 = vals[6]
                df7['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmin'])
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
            
        files = count
    
        figs = [] 
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig1.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 1]", fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df1['tminf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig2.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 2]", fontsize=title_fontsize, fontweight='bold')
    
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['tminf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig3.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 3]", fontsize=title_fontsize, fontweight='bold')
    
        ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['tminf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig4.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 4]", fontsize=title_fontsize, fontweight='bold')
    
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['tminf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig5.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 5]", fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['tminf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig6.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F)) [Night 6]", fontsize=title_fontsize, fontweight='bold')
    
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['tminf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar6 = fig6.colorbar(cs6, shrink=color_table_shrink)
        cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig7.suptitle("National Weather Service Forecast\nFreeze Areas (Minimum Temperature <= 32 (\N{DEGREE SIGN}F) [Night 7]", fontsize=title_fontsize, fontweight='bold')
        
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(temperature_bottom_bound, 32 + temp_scale_step, temp_scale_step), cmap=cmap , transform=datacrs, extend='min')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tminf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
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
    
    
    def plot_maximum_temperature_forecast(start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None): 
    
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
    
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
    
        cmap = colormaps.temperature_colormap()
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        local_time, utc_time = standard.plot_creation_time()
    
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
    
        temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
        temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'maxt')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'maxt')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxt.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.maxt.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.maxt.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
        grb_1_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_1_vals)
        grb_2_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_2_vals)
        grb_3_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_3_vals)
        grb_4_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_4_vals)
        grb_5_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_5_vals)
        grb_6_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_6_vals)
        
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
            grb_7_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_7_vals)
        else:
            pass
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmax', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmax'])
        
            df2 = vals[1]
            df2['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmax'])         
        
            df3 = vals[2]
            df3['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmax'])
            
            df4 = vals[3]
            df4['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmax'])
        
            df5 = vals[4]
            df5['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmax'])
            
            df6 = vals[5]
            df6['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmax'])
    
            if test_7 == True:
                df7 = vals[6]
                df7['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmax'])
            else:
                pass
    
            no_vals = False
    
        except Exception as g:
            no_vals = True
            
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
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df1['tmaxf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['tmaxf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['tmaxf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['tmaxf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['tmaxf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['tmaxf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tmaxf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
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
    
    def plot_minimum_temperature_forecast(start_of_warm_season_month, end_of_warm_season_month, start_of_cool_season_month, end_of_cool_season_month, temp_scale_warm_start, temp_scale_warm_stop, temp_scale_cool_start, temp_scale_cool_stop, temp_scale_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None): 
    
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
    
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
    
        cmap = colormaps.temperature_colormap()
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
        temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
    
        local_time, utc_time = standard.plot_creation_time()
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'mint')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'mint')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.mint.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.mint.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.mint.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
        grb_1_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_1_vals)
        grb_2_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_2_vals)
        grb_3_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_3_vals)
        grb_4_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_4_vals)
        grb_5_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_5_vals)
        grb_6_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_6_vals)
        
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
            grb_7_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_7_vals)
        else:
            pass
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmin', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmin'])
        
            df2 = vals[1]
            df2['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmin'])         
        
            df3 = vals[2]
            df3['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmin'])
            
            df4 = vals[3]
            df4['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmin'])
        
            df5 = vals[4]
            df5['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmin'])
            
            df6 = vals[5]
            df6['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmin'])
    
            if test_7 == True:
                df7 = vals[6]
                df7['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmin'])
            else:
                pass
    
            no_vals = False
    
        except Exception as g:
            no_vals = True
            
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
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df1['tminf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['tminf'][::decimate], color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
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
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
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
    
    
    def plot_minimum_temperature_trend_forecast(contour_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None):
    
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
    
        decimate = decimate
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
    
        cmap = colormaps.relative_humidity_change_colormap()
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
            
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'mint trend')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'mint trend')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.mint.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.mint.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.mint.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
            
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        else:
            pass
    
    
        diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
        diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
        diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
        diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
        diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
        if test_7 == True:
            diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
        else:
            pass
    
        
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmin', count, True, count_short, count_extended, discard)     
            
            df1 = vals[0]
            df1['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmin'])
            
            df2 = vals[1]
            df2['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmin'])
            df2['tdiff'] = df2['tminf'] - df1['tminf']
            
            df3 = vals[2]
            df3['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmin'])
            df3['tdiff'] = df3['tminf'] - df2['tminf']        
            
            df4 = vals[3]
            df4['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmin'])
            df4['tdiff'] = df4['tminf'] - df3['tminf']
            
            df5 = vals[4]
            df5['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmin'])
            df5['tdiff'] = df5['tminf'] - df4['tminf']
            
            df6 = vals[5]
            df6['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmin'])
            df6['tdiff'] = df6['tminf'] - df5['tminf']
    
            if test_7 == True:
                df7 = vals[6]
                df7['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmin'])
                df7['tdiff'] = df7['tminf'] - df6['tminf']
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
    
        files = count
    
        figs = [] 
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig1.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 2]', fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df2['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig2.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 3]', fontsize=title_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df3['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig3.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 4]', fontsize=title_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df4['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig4.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 5]', fontsize=title_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df5['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig5.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 6]', fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df6['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Minimum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig7.suptitle('National Weather Service Forecast\nMinimum Temperature Trend [Night 7]', fontsize=title_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
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
    
    
    def plot_maximum_temperature_trend_forecast(contour_step, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, decimate='default', state='us', gacc_region=None):
    
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
    
        decimate = decimate
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
    
        cmap = colormaps.relative_humidity_change_colormap()
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
            
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None:
    
            fig_x_length = fig_x_length
            fig_y_length = fig_y_length
            signature_x_position = signature_x_position
            signature_y_position = signature_y_position
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
    
        else:
            pass
    
        if state == None and gacc_region == None:
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name)
            else:
                decimate = decimate
        
            directory_name = settings.check_NDFD_directory_name(directory_name)
    
        if state != None and gacc_region == None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_state_data_and_coords(state, True, 'maxt trend')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate
    
        if state == None and gacc_region != None:
            directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, mapcrs, datacrs = settings.get_gacc_region_data_and_coords(gacc_region, True, 'maxt trend')
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate
    
        PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
        GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
        if file_path == None:
    
            try:
    
                grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxt.bin')
    
                print("Downloaded data successfully!")
            except Exception as a:
    
                print("Trying again to download data...")
    
                count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data_test(directory_name, 'ds.maxt.bin')
        
                ds = parsers.NDFD.grib_to_xarray('ds.maxt.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
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
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
            
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        else:
            pass
    
    
        diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
        diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
        diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
        diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
        diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
        if test_7 == True:
            diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
        else:
            pass
    
        
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmax', count, True, count_short, count_extended, discard)     
            
            df1 = vals[0]
            df1['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmax'])
            
            df2 = vals[1]
            df2['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmax'])
            df2['tdiff'] = df2['tmaxf'] - df1['tmaxf']
            
            df3 = vals[2]
            df3['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmax'])
            df3['tdiff'] = df3['tmaxf'] - df2['tmaxf']        
            
            df4 = vals[3]
            df4['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmax'])
            df4['tdiff'] = df4['tmaxf'] - df3['tmaxf']
            
            df5 = vals[4]
            df5['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmax'])
            df5['tdiff'] = df5['tmaxf'] - df4['tmaxf']
            
            df6 = vals[5]
            df6['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmax'])
            df6['tdiff'] = df6['tmaxf'] - df5['tmaxf']
    
            if test_7 == True:
                df7 = vals[6]
                df7['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmax'])
                df7['tdiff'] = df7['tmaxf'] - df6['tmaxf']
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
    
        files = count
    
        figs = [] 
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig1.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Night 2]', fontsize=title_fontsize, fontweight='bold')
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df2['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar1 = fig1.colorbar(cs1, shrink=color_table_shrink)
        cbar1.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig2.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Night 3]', fontsize=title_fontsize, fontweight='bold')
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df3['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar2 = fig2.colorbar(cs2, shrink=color_table_shrink)
        cbar2.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig3.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Night 4]', fontsize=title_fontsize, fontweight='bold')
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df4['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar3 = fig3.colorbar(cs3, shrink=color_table_shrink)
        cbar3.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig4.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Night 5]', fontsize=title_fontsize, fontweight='bold')
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df5['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar4 = fig4.colorbar(cs4, shrink=color_table_shrink)
        cbar4.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
        fig5.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Night 6]', fontsize=title_fontsize, fontweight='bold')
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
        ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df6['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar5 = fig5.colorbar(cs5, shrink=color_table_shrink)
        cbar5.set_label(label="Maximum Temperature Trend (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\n                 Data Source: NOAA/NWS\n         Image Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold')
    
            fig7.suptitle('National Weather Service Forecast\nMaximum Temperature Trend [Night 7]', fontsize=title_fontsize, fontweight='bold')
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
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
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
                
            cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=np.arange(-25, 25 + contour_step, contour_step), cmap='seismic', alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tdiff'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
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








