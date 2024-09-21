'''
This file hosts all the functions that return the settings for each plot for each given state or gacc. 


 This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS

'''

import cartopy.crs as ccrs

def get_metar_mask(state=None, gacc_region=None):

    if state != None and gacc_region == None:
        
        if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
            mask = 250000
        if state == 'CA' or state == 'ca':
            mask = 80000

    return mask


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

def get_gridspec_dims(state, gacc_region):

    if state != None and gacc_region == None:

        if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':

            row1 = 0
            row2 = 8 
            col1 = 0
            col2 = 10

            row3 = 5
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 5
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'CA' or state == 'ca':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 7

            row3 = 0
            row4 = 5
            col3 = 6
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 6
            col6 = 10

    return row1, row2, row3, row4, row5, row6, col1, col2, col3, col4, col5, col6 

def get_gridspec_barb_dims(state, gacc_region):

    if state != None and gacc_region == None:

        if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
            barb_fontsize = 10
        if state == 'CA' or state == 'ca':
            barb_fontsize = 8

    return barb_fontsize

def get_quiver_dims(state, gacc_region, gridspec):

    if gridspec == False:

        if state != None and gacc_region == None:
    
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
    
                minshaft=0.000005 
                headlength=5 
                headwidth=3
    
            if state == 'CA' or state == 'ca':
    
                minshaft=0.000005 
                headlength=9 
                headwidth=7

    if gridspec == True:
        
        if state != None and gacc_region == None:
    
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
    
                minshaft=0.000005 
                headlength=5 
                headwidth=3
    
            if state == 'CA' or state == 'ca':
    
                minshaft=0.00000000005 
                headlength=9 
                headwidth=7
        
    return minshaft, headlength, headwidth

def get_label_coords(state, gacc_region):

    if state != None and gacc_region == None:

        if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':

            x_coord = 0.85
            y_coord = 0.9

        if state == 'CA' or state == 'ca':

            x_coord = 0.73
            y_coord = 0.92



        if state == 'NY' or state == 'ny':

            x_coord = 0.845
            y_coord = 0.9

    if state == None and gacc_region != None:

        if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':

            x_coord = 0.82
            y_coord = 0.9     
    
    return x_coord, y_coord
    

def get_sample_point_color_by_state(state, plot_type):

    if plot_type == 'rtma rh':
        color = 'blue'
        if state == 'US' or state == 'us' or state == 'usa' or state == 'USA':
            color = 'red'
        if state == 'NY' or state =='ny':
            color = 'red'

    return color

def get_state_data_and_coords(state, plot_category, gridspec, plot_type=None):

    state = state
    gridspec=gridspec
    plot_category = plot_category
    plot_type = plot_type
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    color_table_shrink = 1
    legend_fontsize = 14
    directory_name = None
    state_border_linewidth=1
    county_border_linewidth=0.5
    title_x_position = 0.5
    aspect=30
    title_fontsize = 8
    subplot_title_fontsize=7

    if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
        western_bound = -126
        eastern_bound = -66
        southern_bound = 24
        northern_bound = 50.5   
        fig_x_length = 14
        fig_y_length = 12
        title_fontsize = 10
        subplot_title_fontsize=9
        signature_fontsize=9
        colorbar_fontsize=12
        legend_fontsize = 20
        sample_point_fontsize=8
        tick = 9
        aspect=40
        if gridspec == True:
            sample_point_fontsize=15
            tick = 8
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.26
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.14
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'CA' or state == 'ca':
        western_bound = -124.61
        eastern_bound = -113.93
        southern_bound = 30
        northern_bound = 42.5
        fig_x_length = 10
        fig_y_length = 10
        color_table_shrink = 0.7
        colorbar_fontsize=12
        sample_point_fontsize=10
        subplot_title_fontsize=6
        title_fontsize = 7
        signature_fontsize=9
        legend_fontsize = 12
        tick = 6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.25
            signature_y_position = 0.26
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize = 7
            signature_x_position = 0.01
            signature_y_position = 0.12
            if plot_type == '24 Hour Dewpoint Comparison':
                title_fontsize = 7
                subplot_title_fontsize = 6 
            if plot_type == '24 Hour RH Comparison':
                title_fontsize = 7
                subplot_title_fontsize = 6    
            if plot_type == '24 Hour Temperature Comparison':
                title_fontsize = 7
                subplot_title_fontsize = 6    
            if plot_type == '24 Hour Total Cloud Cover Comparison':
                title_fontsize = 6
                subplot_title_fontsize = 6    
            if plot_type == '24 Hour Wind Speed & Direction Comparison':
                title_fontsize = 7
                subplot_title_fontsize = 6    
            if plot_type == '24 Hour Wind Speed Comparison':
                title_fontsize = 7
                subplot_title_fontsize = 6   
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
            if plot_type == 'RH & METAR':
                title_fontsize = 6
                subplot_title_fontsize = 6                  
            if plot_type == 'Low RH & METAR':
                title_fontsize = 6
                subplot_title_fontsize = 6             
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.25
            signature_y_position = 0.26
            title_fontsize = 9
            subplot_title_fontsize=8

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
        if plot_category == 'minrh':
            title_fontsize=17 
        if plot_category == 'poor recovery':
            title_fontsize=15 
        if plot_category == 'excellent recovery':
            title_fontsize=14
        if plot_category == 'maxrh':
            title_fontsize=17
        if plot_category == 'maxrh trend' or plot_category == 'minrh trend':
            title_fontsize=15
        if plot_category == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=20 
        signature_fontsize=23
        sample_point_fontsize=12
        colorbar_fontsize=12
        if plot_category == 'maxrh trend' or plot_category == 'minrh trend':
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
        if plot_category == 'minrh':
            title_fontsize=17 
        if plot_category == 'poor recovery':
            title_fontsize=15 
        if plot_category == 'excellent recovery':
            title_fontsize=14
        if plot_category == 'maxrh':
            title_fontsize=17
        if plot_category == 'maxrh trend' or plot_category == 'minrh trend':
            title_fontsize=15
        if plot_category == 'low minrh':
            title_fontsize=15
        subplot_title_fontsize=20 
        signature_fontsize=23
        sample_point_fontsize=12
        colorbar_fontsize=12
        if plot_category == 'maxrh trend' or plot_category == 'minrh trend':
            colorbar_fontsize=8

    if state == 'ME' or state == 'me':       
        western_bound = -71.2
        eastern_bound = -66.75
        southern_bound = 42.2
        northern_bound = 47.6
        fig_x_length = 10
        fig_y_length = 10
        signature_x_position = 0.255
        signature_y_position = 0.25
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        title_fontsize = 8
        subplot_title_fontsize=7
        legend_fontsize = 30
        color_table_shrink = 0.67
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.26
            signature_y_position = 0.26
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.12
            title_fontsize = 6
            subplot_title_fontsize=5
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.26
            signature_y_position = 0.26
            

    if state == 'NH' or state == 'nh':
        western_bound = -72.65
        eastern_bound = -70.60
        southern_bound = 42.35
        northern_bound = 45.36
        fig_x_length = 10
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        signature_fontsize=7
        title_fontsize = 8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.6
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.31
            signature_y_position = 0.255
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'VT' or state == 'vt':
        western_bound = -73.50
        eastern_bound = -71.44
        southern_bound = 42.5
        northern_bound = 45.10
        fig_x_length = 10
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        signature_fontsize=7
        title_fontsize = 8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.6
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.275
            signature_y_position = 0.25
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'MA' or state == 'ma':
        western_bound = -73.55
        eastern_bound = -69.88
        southern_bound = 41.2
        northern_bound = 42.92
        fig_x_length = 10
        fig_y_length = 6
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        signature_fontsize=7
        title_fontsize = 8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 1
        aspect=30
        tick=7
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.15
            signature_y_position = 0.25
        if plot_category == 'rtma':
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_x_position = 0.01
            signature_y_position = 0.135
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'RI' or state == 'ri':
        western_bound = -71.86
        eastern_bound = -71.11
        southern_bound = 41.2
        northern_bound = 42.03
        fig_x_length = 10
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        signature_fontsize=7
        title_fontsize = 8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.75
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.25
            signature_y_position = 0.25
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'CT' or state == 'ct':
        western_bound = -73.74
        eastern_bound = -71.77
        southern_bound = 40.8
        northern_bound = 42.06
        fig_x_length = 10
        fig_y_length = 6
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        signature_fontsize=7
        title_fontsize = 8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.8
        y_loc = 1 
        x_loc = 0.5
        aspect=30
        tick=7
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.23
            signature_y_position = 0.25
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'NJ' or state == 'nj':
        western_bound = -75.60
        eastern_bound = -73.88
        southern_bound = 38.45
        northern_bound = 41.37
        fig_x_length = 10
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=5
        signature_fontsize=7
        title_fontsize = 6
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.5
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.25
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'DE' or state == 'de':
        western_bound = -76
        eastern_bound = -75.0
        southern_bound = 38.2
        northern_bound = 39.9
        fig_x_length = 10
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=6
        signature_fontsize=7
        title_fontsize = 6
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.5
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.34
            signature_y_position = 0.25
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'NY' or state == 'ny':
        western_bound = -79.85
        eastern_bound = -71.85
        southern_bound = 40.3
        northern_bound = 45.08
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.26
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'PA' or state == 'pa':
        western_bound = -80.6
        eastern_bound = -74.6
        southern_bound = 39.25
        northern_bound = 42.32
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
            

    if state == 'OH' or state == 'oh':
        western_bound = -84.9
        eastern_bound = -80.4
        southern_bound = 37.75
        northern_bound = 42.0
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.25
            signature_y_position = 0.248
            color_table_shrink = 0.7
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'MI' or state == 'mi':
        western_bound = -90.5
        eastern_bound = -82.31
        southern_bound = 40.6
        northern_bound = 48.26
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.24
            signature_y_position = 0.248
            color_table_shrink = 0.7
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'MN' or state == 'mn':
        western_bound = -97.45
        eastern_bound = -89.28
        southern_bound = 42.85
        northern_bound = 49.45
        fig_x_length = 10
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        signature_fontsize=7
        title_fontsize = 8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 1
        aspect=30
        tick=7
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.25
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'WI' or state == 'wi':
        western_bound = -93.1
        eastern_bound = -86.68
        southern_bound = 41.8
        northern_bound = 47.11
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
            signature_x_position = 0.2
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'IA' or state == 'ia':
        western_bound = -96.77
        eastern_bound = -90
        southern_bound = 39.9
        northern_bound = 43.7
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'IN' or state == 'in':
        western_bound = -88.19
        eastern_bound = -84.69
        southern_bound = 37.1
        northern_bound = 41.79
        fig_x_length = 10
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        signature_fontsize=7
        title_fontsize = 8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.6
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/'
            signature_x_position = 0.28
            signature_y_position = 0.25
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'MO' or state == 'mo':
        western_bound = -95.9
        eastern_bound = -88.92
        southern_bound = 35.8
        northern_bound = 40.66
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'IL' or state == 'il':
        western_bound = -91.67
        eastern_bound = -87.44
        southern_bound = 36.3
        northern_bound = 42.55
        fig_x_length = 10
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        signature_fontsize=7
        title_fontsize = 7
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.6
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.31
            signature_y_position = 0.25
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'ND' or state == 'nd':
        western_bound = -104.2
        eastern_bound = -96.47
        southern_bound = 45.3
        northern_bound = 49.1
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_x_position = 0.01
            signature_y_position = 0.145
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'SD' or state == 'sd':
        western_bound = -104.14
        eastern_bound = -96.3
        southern_bound = 42.12
        northern_bound = 46
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'NE' or state == 'ne':
        western_bound = -104.14
        eastern_bound = -95.25
        southern_bound = 39.3
        northern_bound = 43.1
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
           

    if state == 'MD' or state == 'md':
        western_bound = -79.52
        eastern_bound = -74.97
        southern_bound = 37.9
        northern_bound = 39.79
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
           

    if state == 'VA' or state == 'va':
        western_bound = -83.77
        eastern_bound = -75.15
        southern_bound = 35.7
        northern_bound = 39.53
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
          

    if state == 'SC' or state == 'sc':
        western_bound = -83.46
        eastern_bound = -78.35
        southern_bound = 31.4
        northern_bound = 35.25
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.16
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
          

    if state == 'KY' or state == 'ky':
        western_bound = -89.64
        eastern_bound = -81.86
        southern_bound = 35.8
        northern_bound = 39.24
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
          

    if state == 'WV' or state == 'wv':
        western_bound = -82.68
        eastern_bound = -77.61
        southern_bound = 36.5
        northern_bound = 40.72
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.21
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
           

    if state == 'NC' or state == 'nc':
        western_bound = -84.4
        eastern_bound = -75.35
        southern_bound = 33
        northern_bound = 37
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'NV' or state == 'nv':
        western_bound = -120.15
        eastern_bound = -113.92
        southern_bound = 34.91
        northern_bound = 42.09
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=8
        title_fontsize = 9
        signature_fontsize=9
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.6
        aspect=30
        tick=7
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.29
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
          

    if state == 'FL' or state == 'fl':
        western_bound = -87.71
        eastern_bound = -79.77
        southern_bound = 24.44
        northern_bound = 31.08
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        color_table_shrink = 0.8
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/'
            signature_x_position = 0.2
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'OR' or state == 'or':
        western_bound = -125
        eastern_bound = -116.25
        southern_bound = 41.3
        northern_bound = 46.36
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
          

    if state == 'WA' or state == 'wa':
        western_bound = -125
        eastern_bound = -116.9
        southern_bound = 44.8
        northern_bound = 49.1
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
         

    if state == 'ID' or state == 'id':
        western_bound = -117.4
        eastern_bound = -110.97
        southern_bound = 41.2
        northern_bound = 49.1
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        title_fontsize = 8
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.55
        aspect=30
        tick=7
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.31
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'GA' or state == 'ga':
        western_bound = -85.8
        eastern_bound = -80.68
        southern_bound = 29.8
        northern_bound = 35.05
        fig_x_length = 10
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        color_table_shrink = 0.8
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=8
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.21
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
          

    if state == 'AL' or state == 'al':
        western_bound = -88.75
        eastern_bound = -84.77
        southern_bound = 29.5
        northern_bound = 35.05
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        title_fontsize = 8
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.5
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.34
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'MS' or state == 'ms':
        western_bound = -91.82
        eastern_bound = -87.95
        southern_bound = 29.65
        northern_bound = 35.05
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        title_fontsize = 8
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.5
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.34
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'LA' or state == 'la':
        western_bound = -94.24
        eastern_bound = -88.85
        southern_bound = 28.4
        northern_bound = 33.13
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.23
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'AR' or state == 'ar':
        western_bound = -94.81
        eastern_bound = -89.48
        southern_bound = 32.4
        northern_bound = 36.58
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.18
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'TX' or state == 'tx':
        western_bound = -106.95
        eastern_bound = -93.28
        southern_bound = 24.9
        northern_bound = 36.71
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
            signature_x_position = 0.21
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'OK' or state == 'ok':
        western_bound = -103.18
        eastern_bound = -94.26
        southern_bound = 33.5
        northern_bound = 37.2
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 9
            subplot_title_fontsize=8
            signature_x_position = 0.01
            signature_y_position = 0.16
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'NM' or state == 'nm':
        western_bound = -109.24
        eastern_bound = -102.89
        southern_bound = 30.3
        northern_bound = 37.1
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        color_table_shrink = 0.65
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.285
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'AZ' or state == 'az':
        western_bound = -115.05
        eastern_bound = -108.94
        southern_bound = 30.7
        northern_bound = 37.1
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=9
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.65
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.26
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'UT' or state == 'ut':
        western_bound = -114.2
        eastern_bound = -108.97
        southern_bound = 36.2
        northern_bound = 42.1
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        title_fontsize = 8
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.6
        aspect=30
        tick=7
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.29
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'CO' or state == 'co':
        western_bound = -109.2
        eastern_bound = -101.93
        southern_bound = 36.4
        northern_bound = 41.1
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        title_fontsize = 8
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'WY' or state == 'wy':
        western_bound = -111.1
        eastern_bound = -103.95
        southern_bound = 40.4
        northern_bound = 45.07
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        title_fontsize = 8
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12


    if state == 'MT' or state == 'mt':
        western_bound = -116.22
        eastern_bound = -103.93
        southern_bound = 43.4
        northern_bound = 49.1
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        title_fontsize = 8
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        

    if state == 'KS' or state == 'ks':
        western_bound = -102.16
        eastern_bound = -94.51
        southern_bound = 36.3
        northern_bound = 40.11
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        title_fontsize = 8
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'TN' or state == 'tn':
        western_bound = -90.37
        eastern_bound = -81.57
        southern_bound = 34.2
        northern_bound = 36.75
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=7
        title_fontsize = 8
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 14
            subplot_title_fontsize=12
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
        
    return directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick
    

def get_gacc_region_data_and_coords(gacc_region, plot_category, gridspec):

    gacc_region = gacc_region
    gridspec = gridspec
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    color_table_shrink = 0.7
    aspect=30
    tick = 9
    fig_x_length = 12
    fig_y_length = 12
    title_fontsize=20 
    subplot_title_fontsize=14 
    signature_fontsize=10 
    sample_point_fontsize=14
    colorbar_fontsize=10 
    legend_fontsize=12          
    title_x_position=0.5 
    directory_name = None
    if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':
        western_bound = -122.1
        eastern_bound = -113.93
        southern_bound = 32.4
        northern_bound = 39.06
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 30
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.25
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if gacc_region == 'ONCC' or gacc_region == 'oncc' or gacc_region == 'NOPS' or gacc_region == 'nops':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -124.8
        eastern_bound = -119.1
        southern_bound = 35.9
        northern_bound = 42.15
        signature_x_position = 0.23
        signature_y_position = 0.255

    if gacc_region == 'GBCC' or gacc_region == 'gbcc' or gacc_region == 'GB' or gacc_region == 'gb':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -120.5
        eastern_bound = -107.47
        southern_bound = 33
        northern_bound = 46.4
        signature_x_position = 0.21
        signature_y_position = 0.255

    if gacc_region == 'NRCC' or gacc_region == 'nrcc' or gacc_region == 'NR' or gacc_region == 'nr':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -117.7
        eastern_bound = -96
        southern_bound = 41.5
        northern_bound = 50
        fig_y_length = 7
        signature_x_position = 0.14
        signature_y_position = 0.255

    if gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -111.3
        eastern_bound = -94.2
        southern_bound = 35.2
        northern_bound = 46.8
        fig_y_length = 10
        signature_x_position = 0.15
        signature_y_position = 0.255

    if gacc_region == 'SWCC' or gacc_region == 'swcc' or gacc_region == 'SW' or gacc_region == 'sw':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -114.89
        eastern_bound = -101.7
        southern_bound = 30.2
        northern_bound = 38
        fig_y_length = 9
        signature_x_position = 0.15
        signature_y_position = 0.255

    if gacc_region == 'SACC' or gacc_region == 'sacc' or gacc_region == 'SE' or gacc_region == 'se':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -106.88
        eastern_bound = -74.7
        southern_bound = 23.5
        northern_bound = 39.65
        fig_y_length = 8
        signature_x_position = 0.15
        signature_y_position = 0.255

    if gacc_region == 'EACC' or gacc_region == 'eacc' or gacc_region == 'E' or gacc_region == 'e':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
        western_bound = -97.35
        eastern_bound = -66.18
        southern_bound = 33.5
        northern_bound = 49.65
        fig_y_length = 8
        signature_x_position = 0.15
        signature_y_position = 0.255

    if gacc_region == 'PNW' or gacc_region == 'pnw' or gacc_region == 'NWCC' or gacc_region == 'nwcc' or gacc_region == 'NW' or gacc_region == 'nw':
        if ndfd_grids == True:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
        western_bound = -125
        eastern_bound = -116.25
        southern_bound = 41
        northern_bound = 49.1
        signature_x_position = 0.17
        signature_y_position = 0.255


    return directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick


def get_colorbar_label_coords(state, plot_type):

    state = state 
    plot_type

    if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
        if plot_type == 'critical fire':
            x1 = 0.2
            x2 = 0.465
            x3 = 0.72
            y = 0.195

        if plot_type == 'dry lightning':
            x1 = 0.25
            x2 = 0.65
            x3 = None
            y = 0.195

    if state == 'CA' or state == 'ca':

        if plot_type == 'critical fire':
            x1 = 0.278
            x2 = 0.46
            x3 = 0.64
            y = 0.207

        if plot_type == 'dry lightning':
            x1 = 0.325
            x2 = 0.585
            x3 = None
            y = 0.205

    if state == 'ME' or state == 'me':

        if plot_type == 'critical fire':
            x1 = 0.278
            x2 = 0.46
            x3 = 0.64
            y = 0.207

        if plot_type == 'dry lightning':
            x1 = 0.325
            x2 = 0.585
            x3 = None
            y = 0.195

    if state == 'NH' or state == 'nh':

        if plot_type == 'critical fire':
            x1 = 0.278
            x2 = 0.46
            x3 = 0.64
            y = 0.207

        if plot_type == 'dry lightning':
            x1 = 0.325
            x2 = 0.585
            x3 = None
            y = 0.195

    if state == 'VT' or state == 'vt':

        if plot_type == 'critical fire':
            x1 = 0.278
            x2 = 0.46
            x3 = 0.64
            y = 0.207

        if plot_type == 'dry lightning':
            x1 = 0.325
            x2 = 0.585
            x3 = None
            y = 0.195

    return x1, x2, x3, y

    
