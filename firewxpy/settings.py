'''
This file hosts all the functions that return the settings for each plot for each given state or gacc. 


 This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS

'''

import cartopy.crs as ccrs

def get_sp_dims_and_textbox_coords(region):

    region = region

    if region == 'CONUS & South Canada & North Mexico':
        fontsize = 5
        x = 0.01
        y = 0.97

    elif region == 'CONUS' or region == 'conus':
        fontsize = 5
        x = 0.01
        y = 0.95

    elif region == 'Canada' or region == 'canada':
        fontsize = 5
        x = 0.01
        y = 0.95

    elif region == 'NA' or region == 'na':
        fontsize = 5
        x = 0.01
        y = 0.95

    elif region == 'NY' or region == 'ny':
        fontsize = 6
        x = 0.01
        y = 0.97  

    elif region == 'TN' or region == 'tn' or region == 'VA' or region == 'va' or region == 'NC' or region == 'nc' or region == 'OK' or region == 'ok' or region == 'KS' or region == 'ks' or region == 'NE' or region == 'ne' or region == 'SD' or region == 'sd' or region == 'ND' or region == 'nd' or region == 'MT' or region == 'mt' or region == 'NRCC' or region == 'nrcc' or region == 'SACC' or region == 'sacc' or region == 'EACC' or region == 'eacc':
        fontsize = 6
        x = 0.01
        y = 0.95   

    elif region == 'KY' or region == 'ky' or region == 'MI' or region == 'mi' or region == 'ALU' or region == 'alu' or region == 'AFG' or region == 'afg' or region == 'AJK' or region == 'ajk' or region == 'RMCC' or region == 'rmcc':
        fontsize = 6
        x = 0.01
        y = 0.97  

    elif region == 'ONCC' or region == 'oncc' or region == 'VT' or region == 'vt' or region == 'RI' or region == 'ri' or region == 'MS' or region == 'ms' or region == 'IN' or region == 'in' or region == 'IL' or region == 'il' or region == 'NM' or region == 'nm' or region == 'NV' or region == 'nv' or region == 'UT' or region == 'ut' or region == 'ID' or region == 'id':
        fontsize = 9
        x = 0.01
        y = 0.97      

    elif region == 'NJ' or region == 'nj' or region == 'DE' or region == 'de':
        fontsize = 10
        x = 0.01
        y = 0.97   

    elif region == 'GA' or region == 'ga' or region == 'FL' or region == 'fl' or region == 'MO' or region == 'mo':
        fontsize = 8
        x = 0.85
        y = 0.97   

    elif region == 'AZ' or region == 'az':
        fontsize = 8
        x = 0.01
        y = 0.98 

    elif region == 'OSCC' or region == 'oscc':
        fontsize = 8
        x = 0.01
        y = 0.97   

    else:
        fontsize = 8
        x = 0.01
        y = 0.97     

    return fontsize, x, y


def get_region_info(model, region):

    model = model
    region = region

    if region == 'CONUS' or region == 'conus':
        western_bound = -126
        eastern_bound = -66
        southern_bound = 24
        northern_bound = 50.5  
        shrink = 0.375
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 15
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 7
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 7 
        if model == 'GFS0p50':
            decimate = 7
        if model == 'GFS1p00':
            decimate = 7

    if region == 'CA' or region == 'ca':
        western_bound = -124.61
        eastern_bound = -113.93
        southern_bound = 32.4
        northern_bound = 42.5
        shrink = 0.8
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 3
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'AK' or region == 'ak':
        western_bound = -170
        eastern_bound = -130
        southern_bound = 50
        northern_bound = 75      
        shrink = 0.55
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 15
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 7
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 7 
        if model == 'GFS0p50':
            decimate = 7
        if model == 'GFS1p00':
            decimate = 7

    if region == 'AER' or region == 'aer':
        western_bound = -155
        eastern_bound = -140.75
        southern_bound = 55.5
        northern_bound = 64     
        shrink = 0.5
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 5
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 2
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 2
        if model == 'GFS1p00':
            decimate = 2

    if region == 'ALU' or region == 'alu':
        western_bound = -170
        eastern_bound = -151
        southern_bound = 52
        northern_bound = 63      
        shrink = 0.5
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 5
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 2
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 2
        if model == 'GFS1p00':
            decimate = 2

    if region == 'AJK' or region == 'ajk':
        western_bound = -145
        eastern_bound = -129.5
        southern_bound = 54
        northern_bound = 60.75      
        shrink = 0.375
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 5
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 2
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 2
        if model == 'GFS1p00':
            decimate = 2

    if region == 'AFG' or region == 'afg':
        western_bound = -170
        eastern_bound = -140.75
        southern_bound = 60
        northern_bound = 75      
        shrink = 0.425
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 8
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 3
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 3 
        if model == 'GFS0p50':
            decimate = 3
        if model == 'GFS1p00':
            decimate = 3

    if region == 'HI' or region == 'hi':
        western_bound = -160.3
        eastern_bound = -154.73
        southern_bound = 18.76
        northern_bound = 22.28
        shrink = 0.55
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'ME' or region == 'me':       
        western_bound = -71.2
        eastern_bound = -66.75
        southern_bound = 42.2
        northern_bound = 47.6  
        shrink = 1
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 7
        stamp_fontsize = 6
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'NH' or region == 'nh':
        western_bound = -72.65
        eastern_bound = -70.60
        southern_bound = 42.35
        northern_bound = 45.36
        shrink = 1
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.725, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'VT' or region == 'vt':
        western_bound = -73.50
        eastern_bound = -71.44
        southern_bound = 42.5
        northern_bound = 45.10
        shrink = 1
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.725, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'MA' or region == 'ma':
        western_bound = -73.55
        eastern_bound = -69.88
        southern_bound = 41.3
        northern_bound = 42.92
        shrink = 0.375
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'RI' or region == 'ri':
        western_bound = -71.86
        eastern_bound = -71.11
        southern_bound = 41.2
        northern_bound = 42.03
        shrink = 0.925
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.725, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'CT' or region == 'ct':
        western_bound = -73.74
        eastern_bound = -71.77
        southern_bound = 40.8
        northern_bound = 42.06
        shrink = 0.55
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'NJ' or region == 'nj':
        western_bound = -75.60
        eastern_bound = -73.5
        southern_bound = 38.45
        northern_bound = 41.37
        shrink = 1
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.725, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'DE' or region == 'de':
        western_bound = -76
        eastern_bound = -74.5
        southern_bound = 38.2
        northern_bound = 39.9
        shrink = 0.925
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.725, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'NY' or region == 'ny':
        western_bound = -79.85
        eastern_bound = -71.85
        southern_bound = 40.3
        northern_bound = 45.08
        shrink = 0.5
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'PA' or region == 'pa':
        western_bound = -80.6
        eastern_bound = -74.6
        southern_bound = 39.25
        northern_bound = 42.32
        shrink = 0.45
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'OH' or region == 'oh':
        western_bound = -84.9
        eastern_bound = -80.4
        southern_bound = 37.75
        northern_bound = 42.0
        shrink = 0.8
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'MI' or region == 'mi':
        western_bound = -90.5
        eastern_bound = -82.31
        southern_bound = 40.6
        northern_bound = 48.26
        shrink = 0.8
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'MN' or region == 'mn':
        western_bound = -97.45
        eastern_bound = -89.28
        southern_bound = 42.85
        northern_bound = 49.45
        shrink = 0.7
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'WI' or region == 'wi':
        western_bound = -93.1
        eastern_bound = -86.68
        southern_bound = 41.8
        northern_bound = 47.11
        shrink = 0.7
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'IA' or region == 'ia':
        western_bound = -96.77
        eastern_bound = -90
        southern_bound = 39.9
        northern_bound = 43.7
        shrink = 0.475
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'IN' or region == 'in':
        western_bound = -88.19
        eastern_bound = -84.69
        southern_bound = 37.1
        northern_bound = 41.79
        shrink = 1
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.715, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'MO' or region == 'mo':
        western_bound = -95.9
        eastern_bound = -88.92
        southern_bound = 35.8
        northern_bound = 40.66
        shrink = 0.6
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'IL' or region == 'il':
        western_bound = -91.67
        eastern_bound = -87.44
        southern_bound = 36.3
        northern_bound = 42.55
        shrink = 1
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.725, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'ND' or region == 'nd':
        western_bound = -104.2
        eastern_bound = -96.47
        southern_bound = 45.3
        northern_bound = 49.1
        shrink = 0.425
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'SD' or region == 'sd':
        western_bound = -104.14
        eastern_bound = -96.3
        southern_bound = 42.12
        northern_bound = 46.15
        shrink = 0.45
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'NE' or region == 'ne':
        western_bound = -104.14
        eastern_bound = -95.25
        southern_bound = 39.3
        northern_bound = 43.1
        shrink = 0.375
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'MD' or region == 'md':
        western_bound = -79.52
        eastern_bound = -74.97
        southern_bound = 37.9
        northern_bound = 39.79
        shrink = 0.365
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'VA' or region == 'va':
        western_bound = -83.77
        eastern_bound = -75.15
        southern_bound = 35.7
        northern_bound = 39.53
        shrink = 0.375
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'SC' or region == 'sc':
        western_bound = -83.46
        eastern_bound = -78.35
        southern_bound = 31.4
        northern_bound = 35.25
        shrink = 0.625
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'KY' or region == 'ky':
        western_bound = -89.64
        eastern_bound = -81.86
        southern_bound = 35.8
        northern_bound = 39.24
        shrink = 0.375
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'WV' or region == 'wv':
        western_bound = -82.68
        eastern_bound = -77.61
        southern_bound = 36.5
        northern_bound = 40.72
        shrink = 0.715
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'NC' or region == 'nc':
        western_bound = -84.4
        eastern_bound = -75.35
        southern_bound = 33
        northern_bound = 37
        shrink = 0.375
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'NV' or region == 'nv':
        western_bound = -120.15
        eastern_bound = -113.92
        southern_bound = 34.91
        northern_bound = 42.09
        shrink = 1
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.725, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'FL' or region == 'fl':
        western_bound = -87.71
        eastern_bound = -79.77
        southern_bound = 24.44
        northern_bound = 31.08
        shrink = 0.715
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1
        
    if region == 'OR' or region == 'or':
        western_bound = -125
        eastern_bound = -116.25
        southern_bound = 41.3
        northern_bound = 46.36
        shrink = 0.5
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'WA' or region == 'wa':
        western_bound = -125
        eastern_bound = -116.9
        southern_bound = 44.8
        northern_bound = 49.1
        shrink = 0.45
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'ID' or region == 'id':
        western_bound = -117.4
        eastern_bound = -110.97
        southern_bound = 41.2
        northern_bound = 49.1
        shrink = 1
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.725, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'GA' or region == 'ga':
        western_bound = -85.8
        eastern_bound = -80.68
        southern_bound = 29.8
        northern_bound = 35.05
        shrink = 0.875
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.725, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'AL' or region == 'al':
        western_bound = -88.75
        eastern_bound = -84.77
        southern_bound = 29.5
        northern_bound = 35.05
        shrink = 1
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.69, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'MS' or region == 'ms':
        western_bound = -91.82
        eastern_bound = -87.95
        southern_bound = 29.65
        northern_bound = 35.05
        shrink = 1
        x1, y1 = 0.01, -0.01
        x2, y2 = 0.69, -0.01
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'LA' or region == 'la':
        western_bound = -94.24
        eastern_bound = -88.85
        southern_bound = 28.4
        northern_bound = 33.13
        shrink = 0.715
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'AR' or region == 'ar':
        western_bound = -94.81
        eastern_bound = -89.48
        southern_bound = 32.4
        northern_bound = 36.58
        shrink = 0.675
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'TX' or region == 'tx':
        western_bound = -106.95
        eastern_bound = -93.28
        southern_bound = 24.9
        northern_bound = 36.71
        shrink = 0.715
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 3
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'OK' or region == 'ok':
        western_bound = -103.18
        eastern_bound = -94.26
        southern_bound = 33.5
        northern_bound = 37.2
        shrink = 0.34
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'NM' or region == 'nm':
        western_bound = -109.24
        eastern_bound = -102.89
        southern_bound = 30.3
        northern_bound = 37.1
        shrink = 0.9
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 3
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'AZ' or region == 'az':
        western_bound = -115.05
        eastern_bound = -108.94
        southern_bound = 30.7
        northern_bound = 37.1
        shrink = 0.9
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 3
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'UT' or region == 'ut':
        western_bound = -114.2
        eastern_bound = -108.97
        southern_bound = 36.2
        northern_bound = 42.1
        shrink = 1
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 3
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'CO' or region == 'co':
        western_bound = -109.2
        eastern_bound = -101.93
        southern_bound = 36.4
        northern_bound = 41.1
        shrink = 0.55
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'WY' or region == 'wy':
        western_bound = -111.1
        eastern_bound = -103.95
        southern_bound = 40.4
        northern_bound = 45.07
        shrink = 0.55
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'MT' or region == 'mt':
        western_bound = -116.22
        eastern_bound = -103.93
        southern_bound = 43.4
        northern_bound = 49.1
        shrink = 0.375
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 3
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'KS' or region == 'ks':
        western_bound = -102.16
        eastern_bound = -94.51
        southern_bound = 36.3
        northern_bound = 40.11
        shrink = 0.4
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'TN' or region == 'tn':
        western_bound = -90.37
        eastern_bound = -81.57
        southern_bound = 34.2
        northern_bound = 36.75
        shrink = 0.25
        x1, y1 = 0.01, -0.05
        x2, y2 = 0.725, -0.04
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'OSCC' or region == 'oscc' or region == 'SOPS' or region == 'sops':
        western_bound = -122.1
        eastern_bound = -113.93
        southern_bound = 32.4
        northern_bound = 39.06
        shrink = 0.7
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1
        
    if region == 'ONCC' or region == 'oncc' or region == 'NOPS' or region == 'nops':
        western_bound = -124.8
        eastern_bound = -119.1
        southern_bound = 35.9
        northern_bound = 42.15
        shrink = 0.9
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'GBCC' or region == 'gbcc' or region == 'GB' or region == 'gb':
        western_bound = -120.5
        eastern_bound = -107.47
        southern_bound = 33
        northern_bound = 46.4
        shrink = 0.9
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 3
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'NRCC' or region == 'nrcc' or region == 'NR' or region == 'nr':
        western_bound = -117.7
        eastern_bound = -96
        southern_bound = 41.5
        northern_bound = 50
        shrink = 0.325
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 3
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'RMCC' or region == 'rmcc' or region == 'RM' or region == 'rm':
        western_bound = -111.3
        eastern_bound = -94.2
        southern_bound = 35.2
        northern_bound = 46.8
        shrink = 0.6
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 3
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'SWCC' or region == 'swcc' or region == 'SW' or region == 'sw':
        western_bound = -114.89
        eastern_bound = -101.7
        southern_bound = 30.2
        northern_bound = 38
        shrink = 0.5
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 3
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 2 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'SACC' or region == 'sacc' or region == 'SE' or region == 'se':
        western_bound = -106.88
        eastern_bound = -74.7
        southern_bound = 23.5
        northern_bound = 39.65
        shrink = 0.4
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 6
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 3 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'EACC' or region == 'eacc' or region == 'E' or region == 'e':
        western_bound = -97.35
        eastern_bound = -66.18
        southern_bound = 33.5
        northern_bound = 49.65
        shrink = 0.425
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 6
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 3 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'PNW' or region == 'pnw' or region == 'NWCC' or region == 'nwcc' or region == 'NW' or region == 'nw':
        western_bound = -125
        eastern_bound = -116.25
        southern_bound = 41
        northern_bound = 49.1
        shrink = 0.75
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 2
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 1
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 1 
        if model == 'GFS0p50':
            decimate = 1
        if model == 'GFS1p00':
            decimate = 1

    if region == 'CONUS & South Canada & North Mexico':
        western_bound, eastern_bound, southern_bound, northern_bound = -140, -45, 20, 65
        shrink = 0.4
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 20
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 10
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 10 
        if model == 'GFS0p50':
            decimate = 10
        if model == 'GFS1p00':
            decimate = 10

    if region == 'Canada' or region == 'canada':
        western_bound, eastern_bound, southern_bound, northern_bound = -141.5, -51, 41, 85
        shrink = 0.4
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.725, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 20
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 10
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 10 
        if model == 'GFS0p50':
            decimate = 10
        if model == 'GFS1p00':
            decimate = 10
        
    if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
        western_bound, eastern_bound, southern_bound, northern_bound = -180, -51, 20, 85
        shrink = 0.4
        x1, y1 = 0.01, -0.03
        x2, y2 = 0.68, -0.025
        x3, y3 = 0.01, 0.01
        signature_fontsize = 6
        stamp_fontsize = 5
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
            decimate = 20
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 12
        if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
            decimate = 15 
        if model == 'GFS0p50':
            decimate = 12
        if model == 'GFS1p00':
            decimate = 10
        
    return western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize



def coords_for_forecast_model_data(region, western_bound, eastern_bound, southern_bound, northern_bound):

    if region == 'Custom' or region == 'custom':
        if western_bound < 0:
            western_bound = abs(western_bound)
        else:
            western_bound = western_bound
            
        if eastern_bound < 0:
            eastern_bound = abs(eastern_bound)
        else:
            eastern_bound = eastern_bound
            
        southern_bound = southern_bound
        northern_bound = northern_bound   


    if region == 'CONUS & South Canada & North Mexico':
        western_bound = 140
        eastern_bound = 40
        southern_bound = 13
        northern_bound = 65 

    if region == 'Canada' or region == 'canada':
        western_bound = 142
        eastern_bound = 51
        southern_bound = 41
        northern_bound = 85                

    if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
        western_bound = 180
        eastern_bound = 40
        southern_bound = 20
        northern_bound = 85            

    if region == 'CONUS' or region == 'conus':
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
        western_bound = 200
        eastern_bound = 125
        southern_bound = 50
        northern_bound = 80

    if region == 'AER' or region == 'aer':
        western_bound = 160
        eastern_bound = 140
        southern_bound = 50
        northern_bound = 64

    if region == 'ALU' or region == 'alu':
        western_bound = 170
        eastern_bound = 150
        southern_bound = 50
        northern_bound = 64

    if region == 'AJK' or region == 'ajk':
        western_bound = 147
        eastern_bound = 128
        southern_bound = 50
        northern_bound = 62

    if region == 'AFG' or region == 'afg':
        western_bound = 170
        eastern_bound = 140
        southern_bound = 60
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
        eastern_bound = 74.5
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


def get_state_directory(state):

    
    if state == 'CONUS' or state == 'conus':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'CA' or state == 'ca':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'AK' or state == 'ak':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'
    if state == 'HI' or state == 'hi':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/'
    if state == 'ME' or state == 'me':       
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
    if state == 'NH' or state == 'nh':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
    if state == 'VT' or state == 'vt':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
    if state == 'MA' or state == 'ma':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
    if state == 'RI' or state == 'ri':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
    if state == 'CT' or state == 'ct':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
    if state == 'NJ' or state == 'nj':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
    if state == 'DE' or state == 'de':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/'
    if state == 'NY' or state == 'ny':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'PA' or state == 'pa':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'OH' or state == 'oh':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'MI' or state == 'mi':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'MN' or state == 'mn':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'WI' or state == 'wi':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
    if state == 'IA' or state == 'ia':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/'
    if state == 'IN' or state == 'in':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/'
    if state == 'MO' or state == 'mo':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'IL' or state == 'il':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'ND' or state == 'nd':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
    if state == 'SD' or state == 'sd':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
    if state == 'NE' or state == 'ne':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/'
    if state == 'MD' or state == 'md':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'VA' or state == 'va':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
    if state == 'SC' or state == 'sc':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
    if state == 'KY' or state == 'ky':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'WV' or state == 'wv':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'NC' or state == 'nc':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/'
    if state == 'NV' or state == 'nv':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'FL' or state == 'fl':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/'
    if state == 'OR' or state == 'or':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
    if state == 'WA' or state == 'wa':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
    if state == 'ID' or state == 'id':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'
    if state == 'GA' or state == 'ga':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'AL' or state == 'al':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'MS' or state == 'ms':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
    if state == 'LA' or state == 'la':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
    if state == 'AR' or state == 'ar':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/'
    if state == 'TX' or state == 'tx':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
    if state == 'OK' or state == 'ok':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/'
    if state == 'NM' or state == 'nm':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if state == 'AZ' or state == 'az':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
    if state == 'UT' or state == 'ut':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
    if state == 'CO' or state == 'co':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/'
    if state == 'WY' or state == 'wy':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
    if state == 'MT' or state == 'mt':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/'
    if state == 'KS' or state == 'ks':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/'
    if state == 'TN' or state == 'tn':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
            
    return directory_name
    

def get_gacc_region_directory(gacc_region):

    if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'
    if gacc_region == 'ONCC' or gacc_region == 'oncc' or gacc_region == 'NOPS' or gacc_region == 'nops':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if gacc_region == 'GBCC' or gacc_region == 'gbcc' or gacc_region == 'GB' or gacc_region == 'gb':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if gacc_region == 'NRCC' or gacc_region == 'nrcc' or gacc_region == 'NR' or gacc_region == 'nr':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if gacc_region == 'SWCC' or gacc_region == 'swcc' or gacc_region == 'SW' or gacc_region == 'sw':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if gacc_region == 'SACC' or gacc_region == 'sacc' or gacc_region == 'SE' or gacc_region == 'se':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if gacc_region == 'EACC' or gacc_region == 'eacc' or gacc_region == 'E' or gacc_region == 'e':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'
    if gacc_region == 'PNW' or gacc_region == 'pnw' or gacc_region == 'NWCC' or gacc_region == 'nwcc' or gacc_region == 'NW' or gacc_region == 'nw':
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/'

    return directory_name


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



    

    
