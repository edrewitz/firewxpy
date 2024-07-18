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
from dateutil import tz
from matplotlib.patheffects import withStroke




def plot_NWS_7_Day_poor_overnight_recovery_relative_humidity_forecast(directory_name, poor_overnight_recovery_rh_threshold, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, decimate, first_standard_parallel=30, second_standard_parallel=60, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None):

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
    contour_step = contour_step
    poor_overnight_recovery_rh_threshold = poor_overnight_recovery_rh_threshold
    poor_overnight_recovery_rh_thresh = poor_overnight_recovery_rh_threshold + contour_step
    decimate = decimate
    file_path = file_path
    ds = data_array
    count_short = count_short
    count_extended = count_extended
    directory_name = directory_name

    cmap = colormaps.low_relative_humidity_colormap()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
        
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    if file_path == None and directory_name != None:

        grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxrh.bin')
    
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended)

    if file_path != None and directory_name == None:

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended)

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

        df7 = vals[6]
        mask = (df7['maxrh'] <= poor_overnight_recovery_rh_threshold)

    else:
        pass
        
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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

        if show_sample_points == True:

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



def plot_NWS_7_Day_excellent_overnight_recovery_relative_humidity_forecast(directory_name, excellent_overnight_recovery_rh_threshold, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, decimate, first_standard_parallel=30, second_standard_parallel=60, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None):

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

    cmap = colormaps.excellent_recovery_colormap()
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
        
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    if file_path == None and directory_name != None:
        
        grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxrh.bin')
        
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended)

    if file_path != None and directory_name == None:
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended)        

    vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'maxrh', count, True, count_short, count_extended, discard)
    
    df1 = vals[0]

    df2 = vals[1] 

    df3 = vals[2]
    
    df4 = vals[3]
    
    df5 = vals[4]
    
    df6 = vals[5]

    
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

        df7 = vals[6]

    else:
        pass

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

        if show_sample_points == True:
    
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


def plot_NWS_7_Day_maximum_relative_humidity_forecast(directory_name, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, decimate, first_standard_parallel=30, second_standard_parallel=60, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None):

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
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
        
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    if file_path == None and directory_name != None:
        
        grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxrh.bin')
        
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended)

    if file_path != None and directory_name == None:
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended)        

    vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'maxrh', count, True, count_short, count_extended, discard)
    
    df1 = vals[0]

    df2 = vals[1] 

    df3 = vals[2]
    
    df4 = vals[3]
    
    df5 = vals[4]
    
    df6 = vals[5]

    
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

        df7 = vals[6]

    else:
        pass
        
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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

        if show_sample_points == True:
    
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



def plot_NWS_Nights_2_through_7_maximum_relative_humidity_trends(directory_name, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, decimate, first_standard_parallel=30, second_standard_parallel=60, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None):

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

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
        
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    if file_path == None and directory_name != None:
        
        grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.maxrh.bin')
        
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended)

    if file_path != None and directory_name == None:
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended)        

    vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'maxrh', count, True, count_short, count_extended, discard)

    diff1 = grb_2_vals - grb_1_vals
    diff2 = grb_3_vals - grb_2_vals
    diff3 = grb_4_vals - grb_3_vals
    diff4 = grb_5_vals - grb_4_vals
    diff5 = grb_6_vals - grb_5_vals
    
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
        diff6 = grb_7_vals - grb_6_vals

        df7 = vals[6]
        dff6 = df7['maxrh'] - df6['maxrh']
        df7['diff'] = df7['maxrh'] - df6['maxrh']

    else:
        pass
        
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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

    if show_sample_points == True:

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

        if show_sample_points == True:
    
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

def plot_NWS_7_Day_low_minimum_relative_humidity_forecast(directory_name, low_minimum_rh_threshold, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, decimate, first_standard_parallel=30, second_standard_parallel=60, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None):

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

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
        
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    if file_path == None and directory_name != None:
        grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.minrh.bin')
        
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.minrh.bin', 12, False, count_short, count_extended)

    if file_path != None and directory_name == None:

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended)
    
    try:
        vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'minrh', count, True, count_short, count_extended, discard)
        
        df1 = vals[0]

        df2 = vals[1] 

        df3 = vals[2]
        
        df4 = vals[3]
        
        df5 = vals[4]
        
        df6 = vals[5]

        
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

            df7 = vals[6]

        else:
            pass

    except Exception as ee:
        vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'unknown', count, True, count_short, count_extended, discard)
        
        df1 = vals[0]

        df2 = vals[1]

        df3 = vals[2]
        
        df4 = vals[3]

        df5 = vals[4]
        
        df6 = vals[5]

        
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

            df7 = vals[6]

        else:
            pass
        
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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

            if show_sample_points == True:
    
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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

            if show_sample_points == True:
    
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


def plot_NWS_7_Day_minimum_relative_humidity_forecast(directory_name, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, decimate, first_standard_parallel=30, second_standard_parallel=60, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None):

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
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
        
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()

    if file_path == None:
        grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.minrh.bin')
        
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.minrh.bin', 12, False, count_short, count_extended)

    if file_path != None:

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended)
    
    try:
        vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'minrh', count, True, count_short, count_extended, discard)
        
        df1 = vals[0]

        df2 = vals[1] 

        df3 = vals[2]
        
        df4 = vals[3]
        
        df5 = vals[4]
        
        df6 = vals[5]

        
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

            df7 = vals[6]

        else:
            pass

    except Exception as ee:
        vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'unknown', count, True, count_short, count_extended, discard)
        
        df1 = vals[0]

        df2 = vals[1]

        df3 = vals[2]
        
        df4 = vals[3]

        df5 = vals[4]
        
        df6 = vals[5]

        
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

            df7 = vals[6]

        else:
            pass
        
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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

            if show_sample_points == True:
    
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
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(0, 100 + contour_step, contour_step), cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

        if show_sample_points == True:

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

            if show_sample_points == True:
    
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



def plot_NWS_Days_2_through_7_minimum_relative_humidity_trends(directory_name, contour_step, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, fig_x_length, fig_y_length, signature_x_position, signature_y_position, decimate, first_standard_parallel=30, second_standard_parallel=60, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, show_state_borders=True,  show_county_borders=True, show_gacc_borders=False, show_psa_borders=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None):

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

    PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
    GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black')
        
    mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    datacrs = ccrs.PlateCarree()
    if file_path == None:
        grbs, ds, count_short, count_extended = da.FTP_Downloads.get_NWS_NDFD_7_Day_grid_data(directory_name, 'ds.minrh.bin')
        
        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.minrh.bin', 12, False, count_short, count_extended)

    if file_path != None:

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended)
    
    try:
        vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'minrh', count, True, count_short, count_extended, discard)
        
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

        df2['diff'] = df2['minrh'] - df1['minrh']
        df3['diff'] = df3['minrh'] - df2['minrh']
        df4['diff'] = df4['minrh'] - df3['minrh']
        df5['diff'] = df5['minrh'] - df4['minrh']
        df6['diff'] = df6['minrh'] - df5['minrh']

        
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

            df7 = vals[6]

            diff6 = grb_7_vals - grb_6_vals
            df7['diff'] = df7['minrh'] - df6['minrh']

        else:
            pass

    except Exception as ee:
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

            df7 = vals[6]

            diff6 = grb_7_vals - grb_6_vals
    
            df7['diff'] = df7['unknown'] - df6['unknown']

        else:
            pass
        
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

    if show_sample_points == True:

        stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
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

    if show_sample_points == True:

        stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
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

    if show_sample_points == True:

        stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
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

    if show_sample_points == True:

        stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
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

    if show_sample_points == True:

        stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
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

        if show_sample_points == True:
    
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



