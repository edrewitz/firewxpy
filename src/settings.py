'''
This file hosts all the functions that return the settings for each plot for each given state or gacc. 


 This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS

'''

import cartopy.crs as ccrs


def check_NDFD_directory_name(directory_name):

    directory_name = directory_name

    if directory_name == 'CONUS' or directory_name == 'US' or directory_name == 'USA' or directory_name == 'conus' or directory_name == 'us' or directory_name == 'usa':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        
    if directory_name == 'Central Great Lakes' or directory_name == 'CGL' or directory_name == 'central great lakes' or directory_name == 'cgl':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/'
        
    if directory_name == 'Central Mississippi Valley' or directory_name == 'central mississippi valley' or directory_name == 'CMV' or directory_name == 'cmv':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/'
    
    if directory_name == 'Central Plains' or directory_name == 'central plains' or directory_name == 'CP' or directory_name == 'cp':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/'

    if directory_name == 'Central Rockies' or directory_name == 'central rockies' or directory_name == 'CR' or directory_name == 'cr':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/'

    if directory_name == 'Eastern Great Lakes' or directory_name == 'eastern great lakes' or directory_name == 'EGL' or directory_name == 'egl':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/'

    if directory_name == 'Mid Atlantic' or directory_name == 'Mid-Atlantic' or directory_name == 'mid atlantic' or directory_name == 'mid-atlantic' or directory_name == 'ma' or directory_name == 'Mid Atl' or directory_name == 'mid atl' or directory_name == 'Mid-Atl' or directory_name == 'mid-atl':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'

    if directory_name == 'Northeast' or directory_name == 'northeast' or directory_name == 'neast' or directory_name == 'NE' or directory_name == 'ne' or directory_name == 'NEAST' or directory_name == 'Neast':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'

    if directory_name == 'Alaska' or directory_name == 'AK' or directory_name == 'ak' or directory_name == 'alaska':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'

    if directory_name == 'GUAM' or directory_name == 'Guam' or directory_name == 'guam' or directory_name == 'GM' or directory_name == 'gm':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/'

    if directory_name == 'Hawaii' or directory_name == 'HAWAII' or directory_name == 'HI' or directory_name == 'hi':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/'

    if directory_name == 'Northern Hemisphere' or directory_name == 'NHemisphere' or directory_name == 'northern hemisphere' or directory_name == 'nhemisphere' or directory_name == 'NH' or directory_name == 'nh':

        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/'

    if directory_name == 'North Pacific Ocean' or directory_name == 'NORTH PACIFIC OCEAN' or directory_name == 'north pacific ocean' or directory_name == 'npo' or directory_name == 'NPO':

        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/'

    if directory_name == 'Northern Plains' or directory_name == 'NORTHERN PLAINS' or directory_name == 'northern plains' or directory_name == 'NP' or directory_name == 'np' or directory_name == 'NPLAINS' or directory_name == 'nplains':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'

    if directory_name == 'Northern Rockies' or directory_name == 'northern rockies' or directory_name == 'NR' or directory_name == 'nr':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'

    if directory_name == 'Oceanic' or directory_name == 'OCEANIC' or directory_name == 'oceanic' or directory_name == 'o' or directory_name == 'O':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/'

    if directory_name == 'Pacific Northwest' or directory_name == 'PACIFIC NORTHWEST' or directory_name == 'pacific northwest' or directory_name == 'PNW' or directory_name == 'pnw' or directory_name == 'PACNW' or directory_name == 'pacnw':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'

    if directory_name == 'Pacific Southwest' or directory_name == 'PACIFIC SOUTHWEST' or directory_name == 'pacific southwest' or directory_name == 'PSW' or directory_name == 'psw' or directory_name == 'PACSW' or directory_name == 'pacsw':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'

    if directory_name == 'Puerto Rico' or directory_name == 'PUERTO RICO' or directory_name == 'puerto rico' or directory_name == 'PR' or directory_name == 'pr':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/'

    if directory_name == 'Southeast' or directory_name == 'SOUTHEAST' or directory_name == 'southeast' or directory_name == 'SEAST' or directory_name == 'seast' or directory_name == 'SE' or directory_name == 'se':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/'

    if directory_name == 'Southern Mississippi Valley' or directory_name == 'southern mississippi valley' or directory_name == 'SMV' or directory_name == 'smv':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'

    if directory_name == 'Southern Plains' or directory_name == 'SOUTHERN PLAINS' or directory_name == 'southern plains' or directory_name == 'SPLAINS' or directory_name == 'splains' or directory_name == 'SP' or directory_name == 'sp':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
        
    if directory_name == 'Southern Rockies' or directory_name == 'southern rockies' or directory_name == 'SR' or directory_name == 'sr':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/'

    if directory_name == 'Upper Mississippi Valley' or directory_name == 'upper mississippi valley' or directory_name == 'UMV' or directory_name == 'umv':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'

    return directory_name


def get_state_data_and_coords(state, ndfd_grids, plot_type):

    state = state
    ndfd_grids = ndfd_grids
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    plot_type = plot_type
    shrink = 0.7

    if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -126
        eastern_bound = -66
        southern_bound = 20
        northern_bound = 55
        fig_x_length = 12
        fig_y_length = 8
        signature_x_position = 0.09
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=20 
        signature_fontsize=20
        sample_point_fontsize=8
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'AK' or state == 'ak':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'
        western_bound = -168.4
        eastern_bound = -129.73
        southern_bound = 54.5
        northern_bound = 71.46
        fig_x_length = 15
        fig_y_length = 8
        signature_x_position = 0.15
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=20 
        signature_fontsize=23
        sample_point_fontsize=12
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'HI' or state == 'hi':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/'
        western_bound = -160.36
        eastern_bound = -154.57
        southern_bound = 18.81
        northern_bound = 22.46
        fig_x_length = 15
        fig_y_length = 10
        signature_x_position = 0.15
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=20 
        signature_fontsize=23
        sample_point_fontsize=12
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'ME' or state == 'me':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
        western_bound = -71.2
        eastern_bound = -66.75
        southern_bound = 42.87
        northern_bound = 47.6
        fig_x_length = 8
        fig_y_length = 8
        signature_x_position = 0.10
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'NH' or state == 'nh':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
        western_bound = -72.65
        eastern_bound = -70.60
        southern_bound = 42.66
        northern_bound = 45.36
        fig_x_length = 8
        fig_y_length = 9
        signature_x_position = 0.10
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'VT' or state == 'vt':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
        western_bound = -73.50
        eastern_bound = -71.44
        southern_bound = 42.66
        northern_bound = 45.10
        fig_x_length = 8
        fig_y_length = 9
        signature_x_position = 0.10
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'MA' or state == 'ma':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
        western_bound = -73.55
        eastern_bound = -69.88
        southern_bound = 41.22
        northern_bound = 42.92
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.10
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=11
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'RI' or state == 'ri':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
        western_bound = -71.86
        eastern_bound = -71.11
        southern_bound = 41.29
        northern_bound = 42.03
        fig_x_length = 8
        fig_y_length = 8
        signature_x_position = 0.10
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'CT' or state == 'ct':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
        western_bound = -73.74
        eastern_bound = -71.77
        southern_bound = 40.97
        northern_bound = 42.06
        fig_x_length = 8
        fig_y_length = 5
        signature_x_position = 0.10
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'NJ' or state == 'nj':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
        western_bound = -75.60
        eastern_bound = -73.88
        southern_bound = 38.91
        northern_bound = 41.37
        fig_x_length = 8
        fig_y_length = 9
        signature_x_position = 0.10
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'DE' or state == 'de':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
        western_bound = -75.855
        eastern_bound = -75.0
        southern_bound = 39.88
        northern_bound = 38.41
        fig_x_length = 7
        fig_y_length = 9
        signature_x_position = 0.10
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'NY' or state == 'ny':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -79.85
        eastern_bound = -71.85
        southern_bound = 40.48
        northern_bound = 45.08
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.10
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=11
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'PA' or state == 'pa':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -80.6
        eastern_bound = -74.6
        southern_bound = 39.65
        northern_bound = 42.32
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.12
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'OH' or state == 'oh':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -84.9
        eastern_bound = -80.4
        southern_bound = 38.35
        northern_bound = 42.0
        fig_x_length = 6
        fig_y_length = 5
        signature_x_position = 0.07
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'MI' or state == 'mi':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -90.5
        eastern_bound = -82.31
        southern_bound = 41.67
        northern_bound = 48.26
        fig_x_length = 7
        fig_y_length = 5
        signature_x_position = 0.13
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'MN' or state == 'mn':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
        western_bound = -97.45
        eastern_bound = -89.28
        southern_bound = 43.46
        northern_bound = 49.45
        fig_x_length = 7
        fig_y_length = 5
        signature_x_position = 0.11
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'WI' or state == 'wi':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
        western_bound = -93.1
        eastern_bound = -86.68
        southern_bound = 42.38
        northern_bound = 47.11
        fig_x_length = 7
        fig_y_length = 5
        signature_x_position = 0.11
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'IA' or state == 'ia':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
        western_bound = -96.77
        eastern_bound = -90
        southern_bound = 40.3
        northern_bound = 43.7
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.11
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'IN' or state == 'in':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/'
        western_bound = -88.19
        eastern_bound = -84.69
        southern_bound = 37.68
        northern_bound = 41.79
        fig_x_length = 7
        fig_y_length = 7
        signature_x_position = 0.11
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'MO' or state == 'mo':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/'
        western_bound = -95.9
        eastern_bound = -88.92
        southern_bound = 35.8
        northern_bound = 40.66
        fig_x_length = 7
        fig_y_length = 5
        signature_x_position = 0.11
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'IL' or state == 'il':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -91.67
        eastern_bound = -87.44
        southern_bound = 36.87
        northern_bound = 42.55
        fig_x_length = 7
        fig_y_length = 7
        signature_x_position = 0.17
        signature_y_position = 0.02
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if state == 'ND' or state == 'nd':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
        western_bound = -104.2
        eastern_bound = -96.47
        southern_bound = 45.8
        northern_bound = 49.1
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.08
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.6

    if state == 'SD' or state == 'sd':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
        western_bound = -104.14
        eastern_bound = -96.3
        southern_bound = 42.45
        northern_bound = 46
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.08
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.6

    if state == 'NE' or state == 'ne':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
        western_bound = -104.14
        eastern_bound = -95.25
        southern_bound = 39.9
        northern_bound = 43.1
        fig_x_length = 7
        fig_y_length = 3
        signature_x_position = 0.09
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=6
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5    

    if state == 'MD' or state == 'md':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -79.52
        eastern_bound = -74.97
        southern_bound = 37.93
        northern_bound = 39.79
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.09
        signature_y_position = 0.06
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5   

    if state == 'VA' or state == 'va':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
        western_bound = -83.77
        eastern_bound = -75.15
        southern_bound = 36.45
        northern_bound = 39.53
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.07
        signature_y_position = 0.06
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5   

    if state == 'SC' or state == 'sc':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
        western_bound = -83.46
        eastern_bound = -78.35
        southern_bound = 31.96
        northern_bound = 35.25
        fig_x_length = 7
        fig_y_length = 5
        signature_x_position = 0.07
        signature_y_position = 0.06
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7   

    if state == 'KY' or state == 'ky':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -89.64
        eastern_bound = -81.86
        southern_bound = 36.42
        northern_bound = 39.24
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.07
        signature_y_position = 0.06
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5   

    if state == 'WV' or state == 'wv':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -82.68
        eastern_bound = -77.61
        southern_bound = 37.15
        northern_bound = 40.72
        fig_x_length = 7
        fig_y_length = 5
        signature_x_position = 0.07
        signature_y_position = 0.04
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5   

    if state == 'NC' or state == 'nc':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
        western_bound = -84.4
        eastern_bound = -75.35
        southern_bound = 33
        northern_bound = 37
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.07
        signature_y_position = 0.06
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5   

    if state == 'CA' or state == 'ca':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -124.61
        eastern_bound = -113.93
        southern_bound = 32.4
        northern_bound = 42.2
        fig_x_length = 7
        fig_y_length = 6
        signature_x_position = 0.07
        signature_y_position = 0.04
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5 

    if state == 'NV' or state == 'nv':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -120.15
        eastern_bound = -113.92
        southern_bound = 34.91
        northern_bound = 42.09
        fig_x_length = 7
        fig_y_length = 7
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5   

    if state == 'FL' or state == 'fl':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/'
        western_bound = -87.71
        eastern_bound = -79.77
        southern_bound = 24.44
        northern_bound = 31.08
        fig_x_length = 7
        fig_y_length = 6
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7   

    if state == 'OR' or state == 'or':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
        western_bound = -125
        eastern_bound = -116.25
        southern_bound = 41.9
        northern_bound = 46.36
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7   

    if state == 'WA' or state == 'wa':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
        western_bound = -125
        eastern_bound = -116.9
        southern_bound = 41.9
        northern_bound = 49.1
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7   

    if state == 'ID' or state == 'id':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
        western_bound = -117.4
        eastern_bound = -110.97
        southern_bound = 41.9
        northern_bound = 49.1
        fig_x_length = 7
        fig_y_length = 7
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=10
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7   

    if state == 'GA' or state == 'ga':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -85.8
        eastern_bound = -80.68
        southern_bound = 30.28
        northern_bound = 35.05
        fig_x_length = 7
        fig_y_length = 6
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=10
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7  

    if state == 'AL' or state == 'al':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -88.75
        eastern_bound = -84.77
        southern_bound = 30.12
        northern_bound = 35.05
        fig_x_length = 7
        fig_y_length = 8
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=10
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7  

    if state == 'MS' or state == 'ms':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
        western_bound = -91.82
        eastern_bound = -87.95
        southern_bound = 30.12
        northern_bound = 35.05
        fig_x_length = 7
        fig_y_length = 8
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=10
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7 

    if state == 'LA' or state == 'la':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
        western_bound = -94.24
        eastern_bound = -88.85
        southern_bound = 28.88
        northern_bound = 33.13
        fig_x_length = 7
        fig_y_length = 6
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=10
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7 

    if state == 'AR' or state == 'ar':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
        western_bound = -94.81
        eastern_bound = -89.48
        southern_bound = 32.96
        northern_bound = 36.58
        fig_x_length = 7
        fig_y_length = 5
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=10
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7 

    if state == 'TX' or state == 'tx':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
        western_bound = -106.95
        eastern_bound = -93.28
        southern_bound = 25.68
        northern_bound = 36.71
        fig_x_length = 7
        fig_y_length = 6
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=10
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7 

    if state == 'OK' or state == 'ok':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
        western_bound = -103.18
        eastern_bound = -94.26
        southern_bound = 33.5
        northern_bound = 37.2
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.07
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=10
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5 

    if state == 'NM' or state == 'nm':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -109.24
        eastern_bound = -102.89
        southern_bound = 31.18
        northern_bound = 37.1
        fig_x_length = 7
        fig_y_length = 6
        signature_x_position = 0.07
        signature_y_position = 0.03
        title_fontsize=18
        subplot_title_fontsize=10
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7 

    if state == 'AZ' or state == 'az':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
        western_bound = -115.05
        eastern_bound = -108.94
        southern_bound = 31.18
        northern_bound = 37.1
        fig_x_length = 7
        fig_y_length = 6
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=10
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7 

    if state == 'UT' or state == 'ut':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
        western_bound = -114.2
        eastern_bound = -108.97
        southern_bound = 36.9
        northern_bound = 42.1
        fig_x_length = 7
        fig_y_length = 6
        signature_x_position = 0.11
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=10
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7 

    if state == 'CO' or state == 'co':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/'
        western_bound = -109.2
        eastern_bound = -101.93
        southern_bound = 36.9
        northern_bound = 41.1
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.14
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7 

    if state == 'WY' or state == 'wy':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
        western_bound = -111.1
        eastern_bound = -103.95
        southern_bound = 40.94
        northern_bound = 45.07
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.14
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7 

    if state == 'MT' or state == 'mt':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
        western_bound = -116.22
        eastern_bound = -103.93
        southern_bound = 44.38
        northern_bound = 49.1
        fig_x_length = 6
        fig_y_length = 3
        signature_x_position = 0.11
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5

    if state == 'KS' or state == 'ks':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/'
        western_bound = -102.16
        eastern_bound = -94.51
        southern_bound = 36.94
        northern_bound = 40.11
        fig_x_length = 6
        fig_y_length = 3
        signature_x_position = 0.11
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5

    if state == 'NE' or state == 'ne':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/'
        western_bound = -104.19
        eastern_bound = -95.15
        southern_bound = 39.92
        northern_bound = 43.11
        fig_x_length = 6
        fig_y_length = 3
        signature_x_position = 0.07
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5
    
        
    return directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, shrink, mapcrs, datacrs
    

def get_gacc_region_data_and_coords(gacc_region, ndfd_grids, plot_type):

    gacc_region = gacc_region
    ndfd_grids = ndfd_grids
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    shrink = 0.7

    if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
        western_bound = -122.1
        eastern_bound = -113.93
        southern_bound = 32.4
        northern_bound = 39.06
        fig_x_length = 7
        fig_y_length = 6
        signature_x_position = 0.09
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if gacc_region == 'ONCC' or gacc_region == 'oncc' or gacc_region == 'NOPS' or gacc_region == 'nops':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -124.8
        eastern_bound = -119.1
        southern_bound = 36.6
        northern_bound = 42.15
        fig_x_length = 7
        fig_y_length = 7
        signature_x_position = 0.09
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if gacc_region == 'GBCC' or gacc_region == 'gbcc' or gacc_region == 'GB' or gacc_region == 'gb':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -120.5
        eastern_bound = -107.47
        southern_bound = 34.9
        northern_bound = 46.4
        fig_x_length = 7
        fig_y_length = 6
        signature_x_position = 0.07
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8

    if gacc_region == 'NRCC' or gacc_region == 'nrcc' or gacc_region == 'NR' or gacc_region == 'nr':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -117.7
        eastern_bound = -96
        southern_bound = 43
        northern_bound = 50
        fig_x_length = 8
        fig_y_length = 4
        signature_x_position = 0.1
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=10
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5

    if gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -111.3
        eastern_bound = -94.2
        southern_bound = 36.2
        northern_bound = 46.8
        fig_x_length = 7
        fig_y_length = 5
        signature_x_position = 0.1
        signature_y_position = 0.06
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=13
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5

    if gacc_region == 'SWCC' or gacc_region == 'swcc' or gacc_region == 'SW' or gacc_region == 'sw':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -114.89
        eastern_bound = -101.7
        southern_bound = 31.22
        northern_bound = 37.14
        fig_x_length = 7
        fig_y_length = 7
        signature_x_position = 0.1
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5

    if gacc_region == 'SACC' or gacc_region == 'sacc' or gacc_region == 'SE' or gacc_region == 'se':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -106.88
        eastern_bound = -74.7
        southern_bound = 25.5
        northern_bound = 39.65
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.07
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.5

    if gacc_region == 'EACC' or gacc_region == 'eacc' or gacc_region == 'E' or gacc_region == 'e':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -97.35
        eastern_bound = -66.18
        southern_bound = 35
        northern_bound = 49.65
        fig_x_length = 7
        fig_y_length = 4
        signature_x_position = 0.1
        signature_y_position = 0.05
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=12 
        signature_fontsize=12
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.6

    if gacc_region == 'PNW' or gacc_region == 'pnw' or gacc_region == 'NWCC' or gacc_region == 'nwcc' or gacc_region == 'NW' or gacc_region == 'nw':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
        western_bound = -125
        eastern_bound = -116.25
        southern_bound = 41
        northern_bound = 49.1
        fig_x_length = 7
        fig_y_length = 6
        signature_x_position = 0.07
        signature_y_position = 0.03
        if plot_type == 'minrh':
            title_fontsize=17 
        if plot_type == 'poor recovery':
            title_fontsize=15 
        if plot_type == 'excellent recovery':
            title_fontsize=14
        if plot_type == 'maxrh':
            title_fontsize=17
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            title_fontsize=15
        if plot_type == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=9
        signature_fontsize=14
        sample_point_fontsize=10
        colorbar_fontsize=12
        if plot_type == 'maxrh trend' or plot_type == 'minrh trend':
            colorbar_fontsize=8
        shrink=0.7   


    return directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, shrink, mapcrs, datacrs
