'''
This file hosts all the functions that return the settings for each plot for each given state or gacc. 


 This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS

'''

import cartopy.crs as ccrs

def coords_for_forecast_model_data(region, western_bound, eastern_bound, southern_bound, northern_bound, dynamic):

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:

        if region == 'Custom' or region == 'custom':
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound        

    else:

        if region == 'CONUS & South Canada & North Mexico':
            
            western_bound = 140
            eastern_bound = 40
            southern_bound = 13
            northern_bound = 65 

        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':

            western_bound = 180
            eastern_bound = 40
            southern_bound = 12
            northern_bound = 85            

        if region == 'CONUS' or region == 'conus':
            if dynamic == False:
                western_bound = 127
                eastern_bound = 65
                southern_bound = 24
                northern_bound = 50  
            if dynamic == True:
                western_bound = 140
                eastern_bound = 50
                southern_bound = 20
                northern_bound = 60                 
    
        if region == 'CA' or region == 'ca':
            western_bound = 125
            eastern_bound = 113
            southern_bound = 30
            northern_bound = 43
    
        if region == 'AK' or region == 'ak':
            if dynamic == False:
                western_bound = 170
                eastern_bound = 129
                southern_bound = 50
                northern_bound = 72
            if dynamic == True:
                western_bound = 200
                eastern_bound = 125
                southern_bound = 50
                northern_bound = 80
    
        if region == 'HI' or region == 'hi':
            western_bound = 161
            eastern_bound = 154
            southern_bound = 18
            northern_bound = 23
    
        if region == 'ME' or region == 'me':       
            western_bound = 72
            eastern_bound = 66
            southern_bound = 41
            northern_bound = 48
    
        if region == 'NH' or region == 'nh':
            western_bound = 73
            eastern_bound = 70
            southern_bound = 42
            northern_bound = 46
    
        if region == 'VT' or region == 'vt':
            western_bound = 74
            eastern_bound = 71
            southern_bound = 42
            northern_bound = 46
    
        if region == 'MA' or region == 'ma':
            western_bound = 74
            eastern_bound = 69
            southern_bound = 41
            northern_bound = 43
    
        if region == 'RI' or region == 'ri':
            western_bound = 72
            eastern_bound = 70
            southern_bound = 41
            northern_bound = 43
    
        if region == 'CT' or region == 'ct':
            western_bound = 74
            eastern_bound = 71
            southern_bound = 40
            northern_bound = 43       
    
        if region == 'NJ' or region == 'nj':
            western_bound = 76
            eastern_bound = 73
            southern_bound = 38
            northern_bound = 42
    
        if region == 'DE' or region == 'de':
            western_bound = 76
            eastern_bound = 75
            southern_bound = 38
            northern_bound = 40
    
        if region == 'NY' or region == 'ny':
            western_bound = 80
            eastern_bound = 71
            southern_bound = 40
            northern_bound = 46
    
        if region == 'PA' or region == 'pa':
            western_bound = 81
            eastern_bound = 74
            southern_bound = 39
            northern_bound = 43
    
        if region == 'OH' or region == 'oh':
            western_bound = 85
            eastern_bound = 80
            southern_bound = 37
            northern_bound = 42
    
        if region == 'MI' or region == 'mi':
            western_bound = 91
            eastern_bound = 82
            southern_bound = 40
            northern_bound = 49
    
        if region == 'MN' or region == 'mn':
            western_bound = 98
            eastern_bound = 89
            southern_bound = 42
            northern_bound = 50
    
        if region == 'WI' or region == 'wi':
            western_bound = 94
            eastern_bound = 86
            southern_bound = 41
            northern_bound = 48
            
        if region == 'IA' or region == 'ia':
            western_bound = 97
            eastern_bound = 89
            southern_bound = 39
            northern_bound = 44
    
        if region == 'IN' or region == 'in':
            western_bound = 89
            eastern_bound = 84
            southern_bound = 37
            northern_bound = 42
    
        if region == 'MO' or region == 'mo':
            western_bound = 96
            eastern_bound = 88
            southern_bound = 35
            northern_bound = 41
    
        if region == 'IL' or region == 'il':
            western_bound = 92
            eastern_bound = 87
            southern_bound = 36
            northern_bound = 43
    
        if region == 'ND' or region == 'nd':
            western_bound = 105
            eastern_bound = 96
            southern_bound = 45
            northern_bound = 50
    
        if region == 'SD' or region == 'sd':
            western_bound = 105
            eastern_bound = 96
            southern_bound = 42
            northern_bound = 47
    
        if region == 'NE' or region == 'ne':
            western_bound = 105
            eastern_bound = 95
            southern_bound = 39
            northern_bound = 44
    
        if region == 'MD' or region == 'md':
            western_bound = 80
            eastern_bound = 74
            southern_bound = 37
            northern_bound = 40
    
        if region == 'VA' or region == 'va':
            western_bound = 84
            eastern_bound = 75
            southern_bound = 35
            northern_bound = 40
    
        if region == 'SC' or region == 'sc':
            western_bound = 84
            eastern_bound = 78
            southern_bound = 31
            northern_bound = 36
    
        if region == 'KY' or region == 'ky':
            western_bound = 90
            eastern_bound = 81
            southern_bound = 35
            northern_bound = 40
    
        if region == 'WV' or region == 'wv':
            western_bound = 83
            eastern_bound = 77
            southern_bound = 36
            northern_bound = 41
    
        if region == 'NC' or region == 'nc':
            western_bound = 85
            eastern_bound = 75
            southern_bound = 33
            northern_bound = 37
    
        if region == 'NV' or region == 'nv':
            western_bound = 121
            eastern_bound = 113
            southern_bound = 34
            northern_bound = 43
    
        if region == 'FL' or region == 'fl':
            western_bound = 88
            eastern_bound = 79
            southern_bound = 24
            northern_bound = 32     
    
        if region == 'OR' or region == 'or':
            western_bound = 125
            eastern_bound = 116
            southern_bound = 41
            northern_bound = 47
    
        if region == 'WA' or region == 'wa':
            western_bound = 125
            eastern_bound = 116
            southern_bound = 44
            northern_bound = 50
    
        if region == 'ID' or region == 'id':
            western_bound = 118
            eastern_bound = 110
            southern_bound = 41
            northern_bound = 50
    
        if region == 'GA' or region == 'ga':
            western_bound = 86
            eastern_bound = 80
            southern_bound = 29
            northern_bound = 36
    
        if region == 'AL' or region == 'al':
            western_bound = 89
            eastern_bound = 84
            southern_bound = 29
            northern_bound = 36
    
        if region == 'MS' or region == 'ms':
            western_bound = 92
            eastern_bound = 87
            southern_bound = 29
            northern_bound = 36
    
        if region == 'LA' or region == 'la':
            western_bound = 95
            eastern_bound = 88
            southern_bound = 28
            northern_bound = 34
    
        if region == 'AR' or region == 'ar':
            western_bound = 95
            eastern_bound = 89
            southern_bound = 32
            northern_bound = 37
    
        if region == 'TX' or region == 'tx':
            western_bound = 107
            eastern_bound = 93
            southern_bound = 24
            northern_bound = 37
    
        if region == 'OK' or region == 'ok':
            western_bound = 104
            eastern_bound = 94
            southern_bound = 33
            northern_bound = 38
    
        if region == 'NM' or region == 'nm':
            western_bound = 110
            eastern_bound = 102
            southern_bound = 30
            northern_bound = 38
    
        if region == 'AZ' or region == 'az':
            western_bound = 116
            eastern_bound = 108
            southern_bound = 30
            northern_bound = 38
    
        if region == 'UT' or region == 'ut':
            western_bound = 115
            eastern_bound = 108
            southern_bound = 36
            northern_bound = 43
    
        if region == 'CO' or region == 'co':
            western_bound = 110
            eastern_bound = 101
            southern_bound = 36
            northern_bound = 42
    
        if region == 'WY' or region == 'wy':
            western_bound = 112
            eastern_bound = 102
            southern_bound = 40
            northern_bound = 45
    
        if region == 'MT' or region == 'mt':
            western_bound = 117
            eastern_bound = 102
            southern_bound = 43
            northern_bound = 50
    
        if region == 'KS' or region == 'ks':
            western_bound = 103
            eastern_bound = 94
            southern_bound = 36
            northern_bound = 41
    
        if region == 'TN' or region == 'tn':
            western_bound = 91
            eastern_bound = 79
            southern_bound = 34
            northern_bound = 37
    
        if region == 'OSCC' or region == 'oscc':
            western_bound = 123
            eastern_bound = 113
            southern_bound = 32
            northern_bound = 40
    
        if region == 'ONCC' or region == 'oncc':
            western_bound = 125
            eastern_bound = 119
            southern_bound = 35
            northern_bound = 43        
    
        if region == 'GBCC' or region == 'gbcc':
            western_bound = 121
            eastern_bound = 107
            southern_bound = 33
            northern_bound = 47
    
        if region == 'NRCC' or region == 'nrcc':
            western_bound = 118
            eastern_bound = 96
            southern_bound = 41
            northern_bound = 50
    
        if region == 'RMCC' or region == 'rmcc':
            western_bound = 112
            eastern_bound = 94
            southern_bound = 35
            northern_bound = 47
    
        if region == 'SWCC' or region == 'swcc':
            western_bound = 115
            eastern_bound = 101
            southern_bound = 30
            northern_bound = 38
    
        if region == 'SACC' or region == 'sacc':
            western_bound = 107
            eastern_bound = 74
            southern_bound = 23
            northern_bound = 40
    
        if region == 'EACC' or region == 'eacc':
            western_bound = 98
            eastern_bound = 66
            southern_bound = 33
            northern_bound = 50
    
        if region == 'NWCC' or region == 'nwcc':
            western_bound = 125
            eastern_bound = 116
            southern_bound = 41
            northern_bound = 50

    return western_bound, eastern_bound, southern_bound, northern_bound


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
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.14                
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
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.12                  
        if plot_category == 'rtma':
            title_fontsize = 6
            subplot_title_fontsize = 6
            signature_x_position = 0.01
            signature_y_position = 0.12  
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                fig_x_length = 12
                fig_y_length = 7    
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.25
            signature_y_position = 0.26
            title_fontsize = 9
            subplot_title_fontsize=8

    if state == 'AK' or state == 'ak':
        western_bound = -170
        eastern_bound = -130
        southern_bound = 50
        northern_bound = 71
        fig_x_length = 12
        fig_y_length = 12
        signature_x_position = 0.255
        signature_y_position = 0.25
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        title_fontsize = 8
        subplot_title_fontsize=7
        legend_fontsize = 12
        color_table_shrink = 1
        aspect=30
        tick=9
        datacrs = ccrs.PlateCarree()
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.65
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'
            signature_x_position = 0.13
            signature_y_position = 0.25
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'
                signature_x_position = 0.01
                signature_y_position = 0.12                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.12
            title_fontsize = 6
            subplot_title_fontsize=5
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
            if plot_type == 'RTMA Wind Speed & Observed Wind Speed':
                title_fontsize = 6
                subplot_title_fontsize = 6                 

    if state == 'HI' or state == 'hi':
        western_bound = -160.3
        eastern_bound = -154.73
        southern_bound = 18.76
        northern_bound = 22.28
        fig_x_length = 12
        fig_y_length = 12
        signature_x_position = 0.255
        signature_y_position = 0.25
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        title_fontsize = 8
        subplot_title_fontsize=7
        legend_fontsize = 12
        color_table_shrink = 1
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/'
            signature_x_position = 0.13
            signature_y_position = 0.25
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/'
                signature_x_position = 0.01
                signature_y_position = 0.12                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.12
            title_fontsize = 6
            subplot_title_fontsize=5
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
            if plot_type == 'RTMA Wind Speed & Observed Wind Speed':
                title_fontsize = 6
                subplot_title_fontsize = 6    

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
        legend_fontsize = 12
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
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.12                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.12
            title_fontsize = 6
            subplot_title_fontsize=5
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
            if plot_type == 'RTMA Wind Speed & Observed Wind Speed':
                title_fontsize = 6
                subplot_title_fontsize = 6                 
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
        subplot_title_fontsize=6
        signature_fontsize=7
        title_fontsize = 7
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.5
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.45
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.31
            signature_y_position = 0.255
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.09                
        if plot_category == 'rtma':
            title_fontsize = 6
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.09
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
            if plot_type == 'Low RH & METAR' or plot_type == 'RH & METAR':
                title_fontsize = 6
                subplot_title_fontsize=5 
            if plot_type == 'RTMA Wind Speed & Observed Wind Speed':
                title_fontsize = 6
                subplot_title_fontsize=6                 
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 7
            subplot_title_fontsize=6

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
        legend_fontsize = 12
        color_table_shrink = 0.6
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.5
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.275
            signature_y_position = 0.25
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.08                
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.08
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
            if plot_type == 'Low RH & METAR':
                title_fontsize = 6
                subplot_title_fontsize=6  
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.26
            title_fontsize = 7
            subplot_title_fontsize=6

    if state == 'MA' or state == 'ma':
        western_bound = -73.55
        eastern_bound = -69.88
        southern_bound = 41.3
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
        legend_fontsize = 14
        color_table_shrink = 1
        aspect=30
        tick=7
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 1
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.15
            signature_y_position = 0.25
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.135                
        if plot_category == 'rtma':
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_x_position = 0.01
            signature_y_position = 0.135
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                fig_x_length = 9
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.15
            signature_y_position = 0.25
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
        legend_fontsize = 12
        color_table_shrink = 0.75
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.25
            signature_y_position = 0.25
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.12
        if plot_category == 'rtma':
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_x_position = 0.01
            signature_y_position = 0.12
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
            if plot_type == 'Low RH & METAR':
                title_fontsize = 6
                subplot_title_fontsize=6  
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.25
            signature_y_position = 0.25
            title_fontsize = 10
            subplot_title_fontsize=8

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
        legend_fontsize = 12
        color_table_shrink = 0.8
        y_loc = 1 
        x_loc = 0.5
        aspect=30
        tick=7
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.23
            signature_y_position = 0.25
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.135                
        if plot_category == 'rtma':
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_x_position = 0.01
            signature_y_position = 0.135
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_x_length = 6
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.23
            signature_y_position = 0.25
            title_fontsize = 10
            subplot_title_fontsize=8

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
        title_fontsize = 5
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 10
        color_table_shrink = 0.45
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.45
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.25
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.08                
        if plot_category == 'rtma':
            title_fontsize = 5
            subplot_title_fontsize=5
            signature_x_position = 0.01
            signature_y_position = 0.08
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 4  
                sample_point_fontsize = 9
                fig_x_length = 9
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.35
            signature_y_position = 0.25
            title_fontsize = 7
            subplot_title_fontsize=6

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
        legend_fontsize = 10
        color_table_shrink = 0.5
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.47
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.34
            signature_y_position = 0.25
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.08                
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.08
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 4  
                sample_point_fontsize = 9
                fig_x_length = 9
            if plot_type == 'Low RH & METAR' or plot_type == 'RH & METAR':
                title_fontsize = 5
                subplot_title_fontsize = 5
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
            signature_x_position = 0.34
            signature_y_position = 0.25
            title_fontsize = 7
            subplot_title_fontsize=6

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
        legend_fontsize = 16
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.26
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.16                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.16
            title_fontsize = 8
            subplot_title_fontsize=7
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.147                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.13
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_fontsize= 8 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.248
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
        legend_fontsize = 12
        color_table_shrink = 0.6
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.25
            signature_y_position = 0.248
            color_table_shrink = 0.7
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.13                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.13
            title_fontsize = 9
            subplot_title_fontsize=7
            signature_fontsize=12
            if plot_type ==  'Low and High RH':
                tick=7
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_x_length = 4
                tick=7
                signature_fontsize=8
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.25
            signature_y_position = 0.248
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
        legend_fontsize = 12
        color_table_shrink = 0.7
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.24
            signature_y_position = 0.248
            color_table_shrink = 0.7
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.13                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.1
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_fontsize=8
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_x_length = 4
                tick=7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.24
            signature_y_position = 0.248
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
        legend_fontsize = 12
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
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.09                
        if plot_category == 'rtma':
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_x_position = 0.01
            signature_y_position = 0.09
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                fig_y_length = 4
                colorbar_fontsize=6
                signature_fontsize=6
                tick = 5
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.25
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
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
            signature_x_position = 0.2
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.115                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.115
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_fontsize=10
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_x_length = 4
                tick=7
                signature_fontsize=6
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
            signature_x_position = 0.2
            signature_y_position = 0.248
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
        legend_fontsize = 16
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.147                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.147
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_fontsize= 8 
            if plot_type ==  'Low and High RH':
                tick=7
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 8
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        signature_fontsize=8
        title_fontsize = 8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.5
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.5
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/'
            signature_x_position = 0.28
            signature_y_position = 0.25
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.09                
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.09
            fig_x_length = 12
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
            if plot_type == 'RH & METAR':
                title_fontsize = 6
                subplot_title_fontsize = 6                
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/'
            signature_x_position = 0.28
            signature_y_position = 0.25
            title_fontsize = 7
            subplot_title_fontsize=6

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
        legend_fontsize = 17
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.8
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.11                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.11
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_fontsize=10
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_y_length = 7
                fig_x_length = 6
                tick=7
                signature_fontsize=6
                signature_y_position = 0.12
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        signature_fontsize=8
        title_fontsize = 7
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.45
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.45
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.31
            signature_y_position = 0.25
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.08                
        if plot_category == 'rtma':
            title_fontsize = 6
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.09
            fig_x_length = 12
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_y_length = 7
            if plot_type == 'RH & METAR':
                title_fontsize = 6
                subplot_title_fontsize=5                
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.31
            signature_y_position = 0.25
            title_fontsize = 7
            subplot_title_fontsize=6

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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.147                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.147
            title_fontsize = 7
            subplot_title_fontsize = 6
            signature_fontsize= 8 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            title_fontsize = 14
            subplot_title_fontsize=12

    if state == 'SD' or state == 'sd':
        western_bound = -104.14
        eastern_bound = -96.3
        southern_bound = 42.12
        northern_bound = 46.15
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 6
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.147                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.147
            title_fontsize = 7
            subplot_title_fontsize = 6
            signature_fontsize= 8 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 6
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.16                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.16
            title_fontsize = 7
            subplot_title_fontsize = 6
            signature_fontsize = 8 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 6
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.17                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.17
            title_fontsize = 7
            subplot_title_fontsize = 6
            signature_fontsize = 8 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 6
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            title_fontsize = 8
            subplot_title_fontsize=7
           

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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 6
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.16                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.16
            title_fontsize = 7
            subplot_title_fontsize = 6
            signature_fontsize = 8 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.8
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.16
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.12                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.12
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_fontsize=10
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_y_length = 7
                fig_x_length = 5
                tick=7
                signature_fontsize=6
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.16
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 6
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.16                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.16
            title_fontsize = 7
            subplot_title_fontsize = 6
            signature_fontsize = 8 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.21
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.12                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.12
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_fontsize=6
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_y_length = 7
                fig_x_length = 4
                tick=7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.21
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 6
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.16                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.16
            title_fontsize = 7
            subplot_title_fontsize = 6
            signature_fontsize = 8 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        color_table_shrink = 0.6
        aspect=30
        tick=7
        if gridspec == True:
            fig_x_length = 13
            fig_y_length = 7
            color_table_shrink = 0.45
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.29
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.1                
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.1
            fig_x_length = 12
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_y_length = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.29
            signature_y_position = 0.248
            title_fontsize = 8
            subplot_title_fontsize=7

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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 12
            fig_y_length = 7
            color_table_shrink = 0.6
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/'
            signature_x_position = 0.2
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.13                
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.13
            fig_x_length = 12
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_y_length = 5
                tick=7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/'
            signature_x_position = 0.2
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.147                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.13
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_fontsize= 8 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 8
                signature_y_position = 0.13
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.147                  
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.137
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_fontsize= 8 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 8
                signature_y_position = 0.147
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        color_table_shrink = 0.55
        aspect=30
        tick=7
        if gridspec == True:
            fig_x_length = 13
            fig_y_length = 7
            color_table_shrink = 0.45
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.31
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.1                
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.08
            fig_x_length = 12
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_y_length = 7
                signature_y_position = 0.08
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.31
            signature_y_position = 0.248
            title_fontsize = 8
            subplot_title_fontsize=7
        

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
        legend_fontsize = 12
        aspect=30
        color_table_shrink = 0.6
        tick=8
        if gridspec == True:
            fig_x_length = 13
            fig_y_length = 7
            color_table_shrink = 0.6
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.21
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.1                
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.1
            fig_x_length = 12
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_y_length = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.21
            signature_y_position = 0.248
            title_fontsize = 8
            subplot_title_fontsize=7
          

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
        legend_fontsize = 12
        color_table_shrink = 0.5
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 13
            fig_y_length = 7
            color_table_shrink = 0.45
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.34
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.1                
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.1
            fig_x_length = 12
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_y_length = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.34
            signature_y_position = 0.248
            title_fontsize = 7
            subplot_title_fontsize=6
        

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
        legend_fontsize = 12
        color_table_shrink = 0.5
        aspect=30
        tick=6
        if gridspec == True:
            fig_x_length = 13
            fig_y_length = 7
            color_table_shrink = 0.45
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.34
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.1                
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.08
            fig_x_length = 12
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_y_length = 7
                signature_y_position = 0.08
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.34
            signature_y_position = 0.248
            title_fontsize = 7
            subplot_title_fontsize=6
        

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
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.23
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.12                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.12
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_fontsize=10
            tick=8
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_y_length = 7
                fig_x_length = 4
                tick=7
                signature_fontsize=6
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.23
            signature_y_position = 0.248
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
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.8
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.18
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.12                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.12
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_fontsize=10
            tick=8
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_y_length = 7
                fig_x_length = 5
                tick=7
                signature_fontsize=6
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
            signature_x_position = 0.18
            signature_y_position = 0.248
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
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
            signature_x_position = 0.21
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.12                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.12
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_fontsize=10
            tick=8
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 5
                subplot_title_fontsize = 5  
                sample_point_fontsize = 9
                fig_y_length = 7
                fig_x_length = 4
                tick=7
                signature_fontsize=6
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
            signature_x_position = 0.21
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.16                
        if plot_category == 'rtma':
            title_fontsize = 9
            subplot_title_fontsize=8
            signature_x_position = 0.01
            signature_y_position = 0.16
            tick=8
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 6
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.285
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.12                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.12
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_fontsize=9
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 8
                subplot_title_fontsize = 7  
                sample_point_fontsize = 9
                fig_y_length = 14
                fig_x_length = 7
                tick=9
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.285
            signature_y_position = 0.248
            title_fontsize = 8
            subplot_title_fontsize=7
        

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
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.65
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.26
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.12                
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.12
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_fontsize=8
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 8
                subplot_title_fontsize = 7  
                sample_point_fontsize = 9
                fig_y_length = 14
                fig_x_length = 7
                tick=9
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.26
            signature_y_position = 0.248
            title_fontsize = 8
            subplot_title_fontsize=7
        

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
        legend_fontsize = 12
        color_table_shrink = 0.6
        aspect=30
        tick=7
        if gridspec == True:
            fig_x_length = 13
            fig_y_length = 7
            color_table_shrink = 0.6
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.29
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.1                
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.1
            fig_x_length = 12
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_y_length = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.29
            signature_y_position = 0.248
            title_fontsize = 8
            subplot_title_fontsize=7
        

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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.147               
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.115
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_fontsize= 10 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 8
                signature_y_position = 0.118
                signature_fontsize= 8
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.12               
        if plot_category == 'rtma':
            signature_x_position = 0.01
            signature_y_position = 0.115
            title_fontsize = 8
            subplot_title_fontsize=7
            signature_fontsize = 10 
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 7
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 8
                signature_y_position = 0.118
                signature_fontsize = 8 
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.16                
        if plot_category == 'rtma':
            title_fontsize = 9
            subplot_title_fontsize=8
            signature_x_position = 0.01
            signature_y_position = 0.16
            tick = 8
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 6
                signature_fontsize=8
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.16                
        if plot_category == 'rtma':
            title_fontsize = 9
            subplot_title_fontsize=8
            signature_x_position = 0.01
            signature_y_position = 0.16
            tick = 8
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 6
                signature_fontsize=8
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/'
            signature_x_position = 0.14
            signature_y_position = 0.248
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
        legend_fontsize = 12
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 0.9
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.24                
        if plot_category == 'rtma':
            title_fontsize = 9
            subplot_title_fontsize=8
            signature_x_position = 0.01
            signature_y_position = 0.24
            tick = 8
            if plot_type == 'Dry and Windy Areas' or plot_type == 'Dry and Gusty Areas':
                title_fontsize = 6
                subplot_title_fontsize = 6  
                sample_point_fontsize = 9
                fig_x_length = 7
                fig_y_length = 4
                signature_fontsize=8
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.14
            signature_y_position = 0.248
            title_fontsize = 14
            subplot_title_fontsize=12
        
    return directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick
    

def get_gacc_region_data_and_coords(gacc_region, plot_category, gridspec, plot_type=None):

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
        signature_x_position = 0.1
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 11
            fig_y_length = 6
            colorbar_fontsize = 8
            color_table_shrink = 1
            sample_point_fontsize=12
            signature_fontsize=8
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.195
            signature_y_position = 0.25
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
                signature_x_position = 0.01
                signature_y_position = 0.1
                subplot_title_fontsize=8
                title_fontsize = 9
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.12
            if plot_type == 'Low and High RH':
                tick = 8
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
            signature_x_position = 0.195
            signature_y_position = 0.25
            title_fontsize = 14
            subplot_title_fontsize=12

    if gacc_region == 'ONCC' or gacc_region == 'oncc' or gacc_region == 'NOPS' or gacc_region == 'nops':
        western_bound = -124.8
        eastern_bound = -119.1
        southern_bound = 35.9
        northern_bound = 42.15
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=8
        title_fontsize = 9
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.6
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 1
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.28
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.10
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.28
            signature_y_position = 0.248
            title_fontsize = 9
            subplot_title_fontsize=8

    if gacc_region == 'GBCC' or gacc_region == 'gbcc' or gacc_region == 'GB' or gacc_region == 'gb':
        western_bound = -120.5
        eastern_bound = -107.47
        southern_bound = 33
        northern_bound = 46.4
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.6
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 1
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.26
            signature_y_position = 0.248
            if plot_type == 'Dry and Windy Forecast' or plot_type == 'Dry and Gusty Forecast':
                signature_x_position = 0.01
                signature_y_position = 0.1
                subplot_title_fontsize=8
                title_fontsize = 9
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.10
            if plot_type == 'Low and High RH':
                tick = 7
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.26
            signature_y_position = 0.248
            title_fontsize = 10
            subplot_title_fontsize=9

    if gacc_region == 'NRCC' or gacc_region == 'nrcc' or gacc_region == 'NR' or gacc_region == 'nr':
        western_bound = -117.7
        eastern_bound = -96
        southern_bound = 41.5
        northern_bound = 50
        fig_y_length = 7
        fig_x_length = 12
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 8
            color_table_shrink = 1
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.25
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.18
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.248
            title_fontsize = 14
            subplot_title_fontsize=12

    if gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':
        western_bound = -111.3
        eastern_bound = -94.2
        southern_bound = 35.2
        northern_bound = 46.8
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 4
            color_table_shrink = 1
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.25
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.135
            if plot_type == 'Low and High RH':
                tick = 8
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if gacc_region == 'SWCC' or gacc_region == 'swcc' or gacc_region == 'SW' or gacc_region == 'sw':
        western_bound = -114.89
        eastern_bound = -101.7
        southern_bound = 30.2
        northern_bound = 38
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=10
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 7
            fig_y_length = 7
            color_table_shrink = 0.95
            signature_fontsize = 8
            colorbar_fontsize = 8
            sample_point_fontsize=12
            tick = 7
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.25
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.128
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if gacc_region == 'SACC' or gacc_region == 'sacc' or gacc_region == 'SE' or gacc_region == 'se':
        western_bound = -106.88
        eastern_bound = -74.7
        southern_bound = 23.5
        northern_bound = 39.65
        fig_x_length = 12
        fig_y_length = 8
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 11
            color_table_shrink = 1
            colorbar_fontsize = 8
            sample_point_fontsize=12
            tick = 7
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.25
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.13
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12

    if gacc_region == 'EACC' or gacc_region == 'eacc' or gacc_region == 'E' or gacc_region == 'e':
        western_bound = -97.35
        eastern_bound = -66.18
        southern_bound = 33.5
        northern_bound = 49.65
        fig_x_length = 12
        fig_y_length = 8
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.8
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 11
            color_table_shrink = 0.98
            colorbar_fontsize = 8
            sample_point_fontsize=12
            tick = 7
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.25
            signature_y_position = 0.248
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.11
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            signature_x_position = 0.13
            signature_y_position = 0.245
            title_fontsize = 14
            subplot_title_fontsize=12
    if gacc_region == 'PNW' or gacc_region == 'pnw' or gacc_region == 'NWCC' or gacc_region == 'nwcc' or gacc_region == 'NW' or gacc_region == 'nw':
        western_bound = -125
        eastern_bound = -116.25
        southern_bound = 41
        northern_bound = 49.1
        fig_x_length = 12
        fig_y_length = 10
        signature_x_position = 0.10
        signature_y_position = 0.05
        subplot_title_fontsize=9
        title_fontsize = 11
        signature_fontsize=8
        sample_point_fontsize=10
        colorbar_fontsize=12
        legend_fontsize = 12
        color_table_shrink = 0.7
        aspect=30
        tick=9
        if gridspec == True:
            fig_x_length = 10
            fig_y_length = 7
            color_table_shrink = 1
            colorbar_fontsize = 8
            sample_point_fontsize=12
        if plot_category == 'nws':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.25
            signature_y_position = 0.235
        if plot_category == 'rtma':
            title_fontsize = 7
            subplot_title_fontsize=6
            signature_x_position = 0.01
            signature_y_position = 0.08
            if plot_type == 'Low and High RH':
                tick = 8
        if plot_category == 'spc':
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
            signature_x_position = 0.23
            signature_y_position = 0.25
            title_fontsize = 14
            subplot_title_fontsize=12


    return directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick


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


    
