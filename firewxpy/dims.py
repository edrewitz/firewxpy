import warnings
from firewxpy.calc import scaling
warnings.filterwarnings('ignore')

def hawaiian_islands_coords(island):

    if island == None:
        western_bound, eastern_bound, southern_bound, northern_bound = -160.3, -154.73, 18.76, 22.28
        decimate = scaling.get_NDFD_decimation_by_state('hi')
    if island == 'Oahu' or island == 'oahu':
        western_bound, eastern_bound, southern_bound, northern_bound = -158.31, -157.62, 21.22, 21.75
        decimate = 75
    if island == 'Hawaii' or island == 'hawaii':
        western_bound, eastern_bound, southern_bound, northern_bound = -156.21, -154.70, 18.83, 20.35
        decimate = 50
    if island == 'Maui' or island == 'maui':
        western_bound, eastern_bound, southern_bound, northern_bound = -156.76, -155.90, 20.37, 21.08
        decimate = 5
    if island == 'Kauai' or island == 'kauai':
        western_bound, eastern_bound, southern_bound, northern_bound = -159.84, -159.25, 21.84, 22.25
        decimate = 5
    if island == 'Molokai' or island == 'molokai':
        western_bound, eastern_bound, southern_bound, northern_bound = -157.5, -156.6, 21.02, 21.24
        decimate = 67
    if island == 'Lanai' or island == 'lanai':
        western_bound, eastern_bound, southern_bound, northern_bound = -157.07, -156.79, 20.71, 20.95
        decimate = 35
    if island == 'Niihau' or island == 'niihau':
        western_bound, eastern_bound, southern_bound, northern_bound = -160.5, -159.75, 21.7, 22.05
        decimate = 5
    

    return western_bound, eastern_bound, southern_bound, northern_bound, decimate

def get_metar_mask(state, gacc_region, rtma_ws=False):

    r'''
    This function returns the value for the METAR mask for a given state and/or gacc region. 

    Required Arguments: 1) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                            If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                            or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                            acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                            changed to None. 

                        2) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                            If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                            None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                            Here is a list of acceptable gacc_region abbreviations:

                            South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                            North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                            Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                            Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                            Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                            Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                            Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                            Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                            Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                            Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

    Optional Arguments: rtma_ws (Boolean) - Default = False. For full METAR plots, set this to False to allow for more spacing between observation
                        sites to allow for the size of the full station plot. For plots where the user only plots the wind barbs of the observed winds,
                        this value is to be set to True to allow for more data points since the wind barbs do not need as much spacing as a full METAR station plot.

    Returns: The value for the mask of the METAR locations. 

    '''

    if rtma_ws == False:
        if state != None and gacc_region == None:
            
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                mask = 250000
            if state == 'CA' or state == 'ca':
                mask = 80000
            if state == 'FL' or state == 'fl':
                mask = 60000
            if state == 'ME' or state == 'me':
                mask = 30000
            if state == 'NH' or state == 'nh':
                mask = 30000
            if state == 'VT' or state == 'vt':
                mask = 30000
            if state == 'MA' or state == 'ma':
                mask = 30000
            if state == 'RI' or state == 'ri':
                mask = 30000
            if state == 'NY' or state == 'ny':
                mask = 30000
            if state == 'CT' or state == 'ct':
                mask = 30000
            if state == 'NJ' or state == 'nj':
                mask = 30000
            if state == 'DE' or state == 'de':
                mask = 30000
            if state == 'PA' or state == 'pa':
                mask = 30000
            if state == 'OH' or state == 'oh':
                mask = 30000
            if state == 'MI' or state == 'mi':
                mask = 50000
            if state == 'MN' or state == 'mn':
                mask = 50000
            if state == 'WI' or state == 'wi':
                mask = 30000
            if state == 'IA' or state == 'ia':
                mask = 30000
            if state == 'IN' or state == 'in':
                mask = 30000
            if state == 'MO' or state == 'mo':
                mask = 30000
            if state == 'IL' or state == 'il':
                mask = 30000
            if state == 'ND' or state == 'nd':
                mask = 30000
            if state == 'SD' or state == 'sd':
                mask = 30000
            if state == 'NE' or state == 'ne':
                mask = 30000
            if state == 'MD' or state == 'md':
                mask = 30000
            if state == 'VA' or state == 'va':
                mask = 30000
            if state == 'SC' or state == 'sc':
                mask = 30000
            if state == 'KY' or state == 'ky':
                mask = 30000
            if state == 'WV' or state == 'wv':
                mask = 30000
            if state == 'NC' or state == 'nc':
                mask = 40000
            if state == 'NV' or state == 'nv':
                mask = 30000
            if state == 'FL' or state == 'fl':
                mask = 30000
            if state == 'OR' or state == 'or':
                mask = 30000
            if state == 'WA' or state == 'wa':
                mask = 30000 
            if state == 'ID' or state == 'id':
                mask = 30000
            if state == 'GA' or state == 'ga':
                mask = 30000
            if state == 'AL' or state == 'al':
                mask = 30000
            if state == 'MS' or state == 'ms':
                mask = 30000
            if state == 'LA' or state == 'la':
                mask = 30000
            if state == 'AR' or state == 'ar':
                mask = 30000
            if state == 'TX' or state == 'tx':
                mask = 70000
            if state == 'OK' or state == 'ok':
                mask = 30000 
            if state == 'NM' or state == 'nm':
                mask = 30000
            if state == 'AZ' or state == 'az':
                mask = 30000 
            if state == 'UT' or state == 'ut':
                mask = 30000 
            if state == 'CO' or state == 'co':
                mask = 30000
            if state == 'WY' or state == 'wy':
                mask = 30000 
            if state == 'MT' or state == 'mt':
                mask = 30000
            if state == 'KS' or state == 'ks':
                mask = 30000 
            if state == 'TN' or state == 'tn':
                mask = 30000

        if state == None and gacc_region != None:
            if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':
                mask = 40000
            if gacc_region == 'ONCC' or gacc_region == 'oncc' or gacc_region == 'NOPS' or gacc_region == 'nops':
                mask = 40000
            if gacc_region == 'GBCC' or gacc_region == 'gbcc' or gacc_region == 'GB' or gacc_region == 'gb':
                mask = 70000
            if gacc_region == 'NRCC' or gacc_region == 'nrcc' or gacc_region == 'NR' or gacc_region == 'nr':
                mask = 70000
            if gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':
                mask = 60000
            if gacc_region == 'SWCC' or gacc_region == 'swcc' or gacc_region == 'SW' or gacc_region == 'sw':
                mask = 30000
            if gacc_region == 'SACC' or gacc_region == 'sacc' or gacc_region == 'SE' or gacc_region == 'se':
                mask = 160000
            if gacc_region == 'EACC' or gacc_region == 'eacc' or gacc_region == 'E' or gacc_region == 'e':
                mask = 160000
            if gacc_region == 'PNW' or gacc_region == 'pnw' or gacc_region == 'NWCC' or gacc_region == 'nwcc' or gacc_region == 'NW' or gacc_region == 'nw':
                mask = 30000

    if rtma_ws == True:
        if state != None and gacc_region == None:
            
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                mask = 100000
            if state == 'CA' or state == 'ca':
                mask = 300
            if state == 'FL' or state == 'fl':
                mask = 300
            if state == 'GA' or state == 'ga':
                mask = 300
            if state == 'TN' or state == 'tn':
                mask = 300
            if state == 'KY' or state == 'ky':
                mask = 300    
            if state == 'ME' or state == 'me':
                mask = 10    
            if state == 'NH' or state == 'nh':
                mask = 10    
            if state == 'VT' or state == 'vt':
                mask = 10    
            if state == 'MA' or state == 'ma':
                mask = 10  
            if state == 'RI' or state == 'ri':
                mask = 10  
            if state == 'CT' or state == 'ct':
                mask = 10  
            if state == 'NJ' or state == 'nj':
                mask = 10  
            if state == 'DE' or state == 'de':
                mask = 10  
            if state == 'PA' or state == 'pa':
                mask = 10  
            if state == 'OH' or state == 'oh':
                mask = 10  
            if state == 'MI' or state == 'mi':
                mask = 10  
            if state == 'MN' or state == 'mn':
                mask = 10  
            if state == 'WI' or state == 'wi':
                mask = 10  
            if state == 'IA' or state == 'ia':
                mask = 10  
            if state == 'IN' or state == 'in':
                mask = 10 
            if state == 'MO' or state == 'mo':
                mask = 10  
            if state == 'IL' or state == 'il':
                mask = 10  
            if state == 'ND' or state == 'nd':
                mask = 10 
            if state == 'SD' or state == 'sd':
                mask = 10 
            if state == 'NE' or state == 'ne':
                mask = 10 
            if state == 'MD' or state == 'md':
                mask = 10 
            if state == 'VA' or state == 'va':
                mask = 10 
            if state == 'SC' or state == 'sc':
                mask = 10 
            if state == 'KY' or state == 'ky':
                mask = 10 
            if state == 'WV' or state == 'wv':
                mask = 10 
            if state == 'NV' or state == 'nv':
                mask = 10 
            if state == 'NC' or state == 'nc':
                mask = 10 
            if state == 'FL' or state == 'fl':
                mask = 10 
            if state == 'OR' or state == 'or':
                mask = 10 
            if state == 'WA' or state == 'wa':
                mask = 10 
            if state == 'ID' or state == 'id':
                mask = 10 
            if state == 'GA' or state == 'ga':
                mask = 10 
            if state == 'AL' or state == 'al':
                mask = 10 
            if state == 'MS' or state == 'ms':
                mask = 10 
            if state == 'LA' or state == 'la':
                mask = 10 
            if state == 'AR' or state == 'ar':
                mask = 10 
            if state == 'TX' or state == 'tx':
                mask = 10 
            if state == 'OK' or state == 'ok':
                mask = 10 
            if state == 'NM' or state == 'nm':
                mask = 10 
            if state == 'AZ' or state == 'az':
                mask = 10 
            if state == 'UT' or state == 'ut':
                mask = 10 
            if state == 'CO' or state == 'co':
                mask = 10 
            if state == 'WY' or state == 'wy':
                mask = 10 
            if state == 'MT' or state == 'mt':
                mask = 10 
            if state == 'KS' or state == 'ks':
                mask = 10 
            if state == 'TN' or state == 'tn':
                mask = 10 
                
        if state == None and gacc_region != None:
            if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':
                mask = 10
            if gacc_region == 'ONCC' or gacc_region == 'oncc' or gacc_region == 'NOPS' or gacc_region == 'nops':
                mask = 10
            if gacc_region == 'GBCC' or gacc_region == 'gbcc' or gacc_region == 'GB' or gacc_region == 'gb':
                mask = 10
            if gacc_region == 'NRCC' or gacc_region == 'nrcc' or gacc_region == 'NR' or gacc_region == 'nr':
                mask = 10
            if gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':
                mask = 10
            if gacc_region == 'SWCC' or gacc_region == 'swcc' or gacc_region == 'SW' or gacc_region == 'sw':
                mask = 10
            if gacc_region == 'SACC' or gacc_region == 'sacc' or gacc_region == 'SE' or gacc_region == 'se':
                mask = 60000
            if gacc_region == 'EACC' or gacc_region == 'eacc' or gacc_region == 'E' or gacc_region == 'e':
                mask = 60000
            if gacc_region == 'PNW' or gacc_region == 'pnw' or gacc_region == 'NWCC' or gacc_region == 'nwcc' or gacc_region == 'NW' or gacc_region == 'nw':
                mask = 10

    return mask

def get_quiver_dims(state, gacc_region):


    if state != None and gacc_region == None:

        if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':

            minshaft=0.000005 
            headlength=5 
            headwidth=3

        else:

            minshaft=0.000000000000000000000000005  
            headlength=20 
            headwidth=17

    if state == None and gacc_region != None:

            minshaft=0.000000000000000000000000005  
            headlength=20 
            headwidth=17
        
    return minshaft, headlength, headwidth

def get_label_coords(state, gacc_region):

    if state != None and gacc_region == None:

        if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':

            x_coord = 0.91
            y_coord = 0.92

        if state == 'CA' or state == 'ca':

            x_coord = 0.8
            y_coord = 0.94

        if state == 'ME' or state == 'me':

            x_coord = 0.77
            y_coord = 0.93

        if state == 'NH' or state == 'nh':

            x_coord = 0.77
            y_coord = 0.94

        if state == 'VT' or state == 'vt':

            x_coord = 0.77
            y_coord = 0.02

        if state == 'MA' or state == 'ma':

            x_coord = 0.83
            y_coord = 0.9

        if state == 'RI' or state == 'ri':

            x_coord = 0.78
            y_coord = 0.93

        if state == 'CT' or state == 'ct':

            x_coord = 0.78
            y_coord = 0.02

        if state == 'NJ' or state == 'nj':

            x_coord = 0.73
            y_coord = 0.95

        if state == 'PA' or state == 'pa':

            x_coord = 0.85
            y_coord = 0.92

        if state == 'OH' or state == 'oh':

            x_coord = 0.82
            y_coord = 0.02

        if state == 'MI' or state == 'mi':

            x_coord = 0.82
            y_coord = 0.94

        if state == 'MN' or state == 'mn':

            x_coord = 0.85
            y_coord = 0.93

        if state == 'WI' or state == 'wi':

            x_coord = 0.85
            y_coord = 0.94

        if state == 'IA' or state == 'ia':

            x_coord = 0.88
            y_coord = 0.92

        if state == 'IN' or state == 'in':

            x_coord = 0.75
            y_coord = 0.02

        if state == 'MO' or state == 'mo':

            x_coord = 0.88
            y_coord = 0.94

        if state == 'IL' or state == 'il':

            x_coord = 0.01
            y_coord = 0.93

        if state == 'NY' or state == 'ny':

            x_coord = 0.87
            y_coord = 0.93

        if state == 'FL' or state == 'fl':

            x_coord = 0.86
            y_coord = 0.94

        if state == 'ND' or state == 'nd':

            x_coord = 0.88
            y_coord = 0.02

        if state == 'SD' or state == 'sd':

            x_coord = 0.88
            y_coord = 0.02

        if state == 'NE' or state == 'ne':

            x_coord = 0.87
            y_coord = 0.92

        if state == 'MD' or state == 'md':

            x_coord = 0.87
            y_coord = 0.92

        if state == 'VA' or state == 'va':

            x_coord = 0.87
            y_coord = 0.92

        if state == 'SC' or state == 'sc':

            x_coord = 0.86
            y_coord = 0.94

        if state == 'KY' or state == 'ky':

            x_coord = 0.87
            y_coord = 0.92

        if state == 'WV' or state == 'wv':

            x_coord = 0.86
            y_coord = 0.94

        if state == 'NC' or state == 'nc':

            x_coord = 0.87
            y_coord = 0.93

        if state == 'NV' or state == 'nv':

            x_coord = 0.01
            y_coord = 0.15

        if state == 'OR' or state == 'or':

            x_coord = 0.86
            y_coord = 0.94

        if state == 'WA' or state == 'wa':

            x_coord = 0.88
            y_coord = 0.02

        if state == 'ID' or state == 'id':

            x_coord = 0.8
            y_coord = 0.94

        if state == 'GA' or state == 'ga':

            x_coord = 0.81
            y_coord = 0.94

        if state == 'AL' or state == 'al':

            x_coord = 0.75
            y_coord = 0.02

        if state == 'MS' or state == 'ms':

            x_coord = 0.01
            y_coord = 0.94

        if state == 'LA' or state == 'la':

            x_coord = 0.83
            y_coord = 0.94

        if state == 'TX' or state == 'tx':

            x_coord = 0.01
            y_coord = 0.94

        if state == 'OK' or state == 'ok':

            x_coord = 0.01
            y_coord = 0.18

        if state == 'NM' or state == 'nm':

            x_coord = 0.82
            y_coord = 0.02

        if state == 'AZ' or state == 'az':

            x_coord = 0.82
            y_coord = 0.02

        if state == 'UT' or state == 'ut':

            x_coord = 0.82
            y_coord = 0.94

        if state == 'CO' or state == 'co':

            x_coord = 0.85
            y_coord = 0.02

        if state == 'WY' or state == 'wy':

            x_coord = 0.85
            y_coord = 0.02

        if state == 'MT' or state == 'mt':

            x_coord = 0.85
            y_coord = 0.02

        if state == 'KS' or state == 'ks':

            x_coord = 0.85
            y_coord = 0.02

        if state == 'TN' or state == 'tn':

            x_coord = 0.85
            y_coord = 0.02

    if state == None and gacc_region != None:

        if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':

            x_coord = 0.85
            y_coord = 0.93   

        if gacc_region == 'ONCC' or gacc_region == 'oncc' or gacc_region == 'NOPS' or gacc_region == 'nops':

            x_coord = 0.01
            y_coord = 0.12   

        if gacc_region == 'GBCC' or gacc_region == 'gbcc' or gacc_region == 'GB' or gacc_region == 'gb':

            x_coord = 0.84
            y_coord = 0.93  

        if gacc_region == 'NRCC' or gacc_region == 'nrcc' or gacc_region == 'NR' or gacc_region == 'nr':

            x_coord = 0.88
            y_coord = 0.9 

        if gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':

            x_coord = 0.88
            y_coord = 0.9 

        if gacc_region == 'SWCC' or gacc_region == 'swcc' or gacc_region == 'SW' or gacc_region == 'sw':

            x_coord = 0.88
            y_coord = 0.9 

        if gacc_region == 'SACC' or gacc_region == 'sacc' or gacc_region == 'SE' or gacc_region == 'se':

            x_coord = 0.01
            y_coord = 0.15 

        if gacc_region == 'EACC' or gacc_region == 'eacc' or gacc_region == 'E' or gacc_region == 'e':

            x_coord = 0.88
            y_coord = 0.93

        if gacc_region == 'PNW' or gacc_region == 'pnw' or gacc_region == 'NWCC' or gacc_region == 'nwcc' or gacc_region == 'NW' or gacc_region == 'nw':

            x_coord = 0.85
            y_coord = 0.01
    
    return x_coord, y_coord


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

        if state == 'ME' or state == 'me':

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

        if state == 'NH' or state == 'nh':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 9

            row3 = 0
            row4 = 5
            col3 = 6
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 6
            col6 = 10

        if state == 'VT' or state == 'vt':

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

        if state == 'MA' or state == 'ma':

            row1 = 0
            row2 = 7 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'RI' or state == 'ri':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 7

            row3 = 0
            row4 = 5
            col3 = 7
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 7
            col6 = 10

        if state == 'CT' or state == 'ct':

            row1 = 0
            row2 = 6 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'NJ' or state == 'nj':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 9

            row3 = 0
            row4 = 5
            col3 = 6
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 6
            col6 = 10

        if state == 'DE' or state == 'de':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 9

            row3 = 0
            row4 = 5
            col3 = 6
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 6
            col6 = 10

        if state == 'NY' or state == 'ny':

            row1 = 0
            row2 = 6 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'PA' or state == 'pa':

            row1 = 0
            row2 = 8 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'OH' or state == 'oh':

            row1 = 0
            row2 = 6 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'MI' or state == 'mi':

            row1 = 0
            row2 = 6 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'MN' or state == 'mn':

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

        if state == 'WI' or state == 'wi':

            row1 = 0
            row2 = 7 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'IA' or state == 'ia':

            row1 = 0
            row2 = 8 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'IN' or state == 'in':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 9

            row3 = 0
            row4 = 5
            col3 = 6
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 6
            col6 = 10

        if state == 'MO' or state == 'mo':

            row1 = 0
            row2 = 6 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'IL' or state == 'il':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 9

            row3 = 0
            row4 = 5
            col3 = 6
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 6
            col6 = 10

        if state == 'ND' or state == 'nd':

            row1 = 0
            row2 = 8 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'SD' or state == 'sd':

            row1 = 0
            row2 = 8 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'NE' or state == 'ne':

            row1 = 0
            row2 = 9 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'MD' or state == 'md':

            row1 = 0
            row2 = 9 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'VA' or state == 'va':

            row1 = 0
            row2 = 9 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'SC' or state == 'sc':

            row1 = 0
            row2 = 6 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'KY' or state == 'ky':

            row1 = 0
            row2 = 9 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'WV' or state == 'wv':

            row1 = 0
            row2 = 7 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'NC' or state == 'nc':

            row1 = 0
            row2 = 9 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'NV' or state == 'nv':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 8

            row3 = 0
            row4 = 5
            col3 = 6
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 6
            col6 = 10

        if state == 'FL' or state == 'fl':

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

        if state == 'OR' or state == 'or':

            row1 = 0
            row2 = 8 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'WA' or state == 'wa':

            row1 = 0
            row2 = 9 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'ID' or state == 'id':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 8

            row3 = 0
            row4 = 5
            col3 = 6
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 6
            col6 = 10

        if state == 'GA' or state == 'ga':

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

        if state == 'AL' or state == 'al':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 9

            row3 = 0
            row4 = 5
            col3 = 6
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 6
            col6 = 10

        if state == 'MS' or state == 'ms':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 9

            row3 = 0
            row4 = 5
            col3 = 6
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 6
            col6 = 10

        if state == 'LA' or state == 'la':

            row1 = 0
            row2 = 7 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'AR' or state == 'ar':

            row1 = 0
            row2 = 6 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'TX' or state == 'tx':

            row1 = 0
            row2 = 7 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'OK' or state == 'ok':

            row1 = 0
            row2 = 9 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'NM' or state == 'nm':

            row1 = 0
            row2 = 6 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'AZ' or state == 'az':

            row1 = 0
            row2 = 6 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'UT' or state == 'ut':

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

        if state == 'CO' or state == 'co':

            row1 = 0
            row2 = 7 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'WY' or state == 'wy':

            row1 = 0
            row2 = 7 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'MT' or state == 'mt':

            row1 = 0
            row2 = 7 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'KS' or state == 'ks':

            row1 = 0
            row2 = 7 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if state == 'TN' or state == 'tn':

            row1 = 0
            row2 = 9 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

    if state == None and gacc_region != None:

        if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 7

            row3 = 0
            row4 = 5
            col3 = 7
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 7
            col6 = 10

        if gacc_region == 'ONCC' or gacc_region == 'oncc' or gacc_region == 'NOPS' or gacc_region == 'nops':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 7

            row3 = 0
            row4 = 5
            col3 = 7
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 7
            col6 = 10

        if gacc_region == 'GBCC' or gacc_region == 'gbcc' or gacc_region == 'GB' or gacc_region == 'gb':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 7

            row3 = 0
            row4 = 5
            col3 = 7
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 7
            col6 = 10

        if gacc_region == 'NRCC' or gacc_region == 'nrcc' or gacc_region == 'NR' or gacc_region == 'nr':

            row1 = 0
            row2 = 9 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 7

            row3 = 0
            row4 = 5
            col3 = 7
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 7
            col6 = 10

        if gacc_region == 'SWCC' or gacc_region == 'swcc' or gacc_region == 'SW' or gacc_region == 'sw':

            row1 = 0
            row2 = 6 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if gacc_region == 'SACC' or gacc_region == 'sacc' or gacc_region == 'SE' or gacc_region == 'se':

            row1 = 0
            row2 = 9 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if gacc_region == 'EACC' or gacc_region == 'eacc' or gacc_region == 'E' or gacc_region == 'e':

            row1 = 0
            row2 = 9 
            col1 = 0
            col2 = 10

            row3 = 6
            row4 = 10
            col3 = 0
            col4 = 5

            row5 = 6
            row6 = 10
            col5 = 5
            col6 = 10

        if gacc_region == 'PNW' or gacc_region == 'pnw' or gacc_region == 'NWCC' or gacc_region == 'nwcc' or gacc_region == 'NW' or gacc_region == 'nw':

            row1 = 0
            row2 = 10 
            col1 = 0
            col2 = 7

            row3 = 0
            row4 = 5
            col3 = 7
            col4 = 10

            row5 = 5
            row6 = 10
            col5 = 7
            col6 = 10


    return row1, row2, row3, row4, row5, row6, col1, col2, col3, col4, col5, col6 


def get_colorbar_label_coords(state, gacc_region, plot_type):

    state = state 
    gacc_region = gacc_region

    if state != None and gacc_region == None:

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
                x1 = 0.33
                x2 = 0.585
                x3 = None
                y = 0.205
    
        if state == 'NH' or state == 'nh':
    
            if plot_type == 'critical fire':
                x1 = 0.278
                x2 = 0.46
                x3 = 0.64
                y = 0.207
    
            if plot_type == 'dry lightning':
                x1 = 0.355
                x2 = 0.56
                x3 = None
                y = 0.21
    
        if state == 'VT' or state == 'vt':
    
            if plot_type == 'critical fire':
                x1 = 0.278
                x2 = 0.46
                x3 = 0.64
                y = 0.207
    
            if plot_type == 'dry lightning':
                x1 = 0.34
                x2 = 0.56
                x3 = None
                y = 0.205
    
        if state == 'MA' or state == 'ma':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.18
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.63
                x3 = None
                y = 0.185
    
        if state == 'RI' or state == 'ri':
    
            if plot_type == 'critical fire':
                x1 = 0.26
                x2 = 0.465
                x3 = 0.66
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.325
                x2 = 0.59
                x3 = None
                y = 0.205
    
        if state == 'CT' or state == 'ct':
    
            if plot_type == 'critical fire':
                x1 = 0.25
                x2 = 0.465
                x3 = 0.67
                y = 0.19
    
            if plot_type == 'dry lightning':
                x1 = 0.32
                x2 = 0.59
                x3 = None
                y = 0.1925
    
        if state == 'NJ' or state == 'nj':
    
            if plot_type == 'critical fire':
                x1 = 0.36
                x2 = 0.48
                x3 = 0.59
                y = 0.21
    
            if plot_type == 'dry lightning':
                x1 = 0.38
                x2 = 0.555
                x3 = None
                y = 0.211
    
        if state == 'DE' or state == 'de':
    
            if plot_type == 'critical fire':
                x1 = 0.34
                x2 = 0.48
                x3 = 0.605
                y = 0.21
    
            if plot_type == 'dry lightning':
                x1 = 0.37
                x2 = 0.56
                x3 = None
                y = 0.21
    
        if state == 'NY' or state == 'ny':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'PA' or state == 'pa':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'OH' or state == 'oh':
    
            if plot_type == 'critical fire':
                x1 = 0.32
                x2 = 0.475
                x3 = 0.625
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.35
                x2 = 0.585
                x3 = None
                y = 0.205
    
        if state == 'MI' or state == 'mi':
    
            if plot_type == 'critical fire':
                x1 = 0.285
                x2 = 0.47
                x3 = 0.66
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.35
                x2 = 0.585
                x3 = None
                y = 0.205
    
        if state == 'MN' or state == 'mn':
    
            if plot_type == 'critical fire':
                x1 = 0.21
                x2 = 0.47
                x3 = 0.715
                y = 0.2
                
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.2
    
        if state == 'WI' or state == 'wi':
    
            if plot_type == 'critical fire':
                x1 = 0.27
                x2 = 0.47
                x3 = 0.68
                y = 0.2
                
            if plot_type == 'dry lightning':
                x1 = 0.32
                x2 = 0.61
                x3 = None
                y = 0.2
    
        if state == 'IA' or state == 'ia':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'IN' or state == 'in':
    
            if plot_type == 'critical fire':
                x1 = 0.345
                x2 = 0.48
                x3 = 0.595
                y = 0.21
    
            if plot_type == 'dry lightning':
                x1 = 0.36
                x2 = 0.55
                x3 = None
                y = 0.21
    
        if state == 'MO' or state == 'mo':
    
            if plot_type == 'critical fire':
                x1 = 0.205
                x2 = 0.47
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.28
                x2 = 0.63
                x3 = None
                y = 0.195
    
        if state == 'IL' or state == 'il':
    
            if plot_type == 'critical fire':
                x1 = 0.36
                x2 = 0.475
                x3 = 0.59
                y = 0.21
    
            if plot_type == 'dry lightning':
                x1 = 0.365
                x2 = 0.55
                x3 = None
                y = 0.21
    
        if state == 'ND' or state == 'nd':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'SD' or state == 'sd':
    
            if plot_type == 'critical fire':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'NE' or state == 'ne':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'MD' or state == 'md':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'VA' or state == 'va':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'SC' or state == 'sc':
    
            if plot_type == 'critical fire':
                x1 = 0.26
                x2 = 0.47
                x3 = 0.68
                y = 0.197
    
            if plot_type == 'dry lightning':
                x1 = 0.32
                x2 = 0.61
                x3 = None
                y = 0.197
    
        if state == 'KY' or state == 'ky':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'WV' or state == 'wv':
    
            if plot_type == 'critical fire':
                x1 = 0.26
                x2 = 0.475
                x3 = 0.68
                y = 0.197
    
            if plot_type == 'dry lightning':
                x1 = 0.32
                x2 = 0.61
                x3 = None
                y = 0.197
    
        if state == 'NC' or state == 'nc':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'NV' or state == 'nv':
    
            if plot_type == 'critical fire':
                x1 = 0.32
                x2 = 0.475
                x3 = 0.62
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.35
                x2 = 0.585
                x3 = None
                y = 0.205
    
        if state == 'FL' or state == 'fl':
    
            if plot_type == 'critical fire':
                x1 = 0.26
                x2 = 0.47
                x3 = 0.68
                y = 0.197
    
            if plot_type == 'dry lightning':
                x1 = 0.31
                x2 = 0.61
                x3 = None
                y = 0.197
    
        if state == 'OR' or state == 'or':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'WA' or state == 'wa':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'ID' or state == 'id':
    
            if plot_type == 'critical fire':
                x1 = 0.34
                x2 = 0.47
                x3 = 0.62
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.365
                x2 = 0.57
                x3 = None
                y = 0.205
    
        if state == 'GA' or state == 'ga':
    
            if plot_type == 'critical fire':
                x1 = 0.305
                x2 = 0.47
                x3 = 0.62
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.365
                x2 = 0.55
                x3 = None
                y = 0.205
    
        if state == 'AL' or state == 'al':
    
            if plot_type == 'critical fire':
                x1 = 0.35
                x2 = 0.475
                x3 = 0.61
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.365
                x2 = 0.55
                x3 = None
                y = 0.205
    
        if state == 'MS' or state == 'ms':
    
            if plot_type == 'critical fire':
                x1 = 0.35
                x2 = 0.475
                x3 = 0.61
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.38
                x2 = 0.56
                x3 = None
                y = 0.207
    
        if state == 'LA' or state == 'la':
    
            if plot_type == 'critical fire':
                x1 = 0.26
                x2 = 0.47
                x3 = 0.68
                y = 0.197
    
            if plot_type == 'dry lightning':
                x1 = 0.32
                x2 = 0.61
                x3 = None
                y = 0.197
    
        if state == 'AR' or state == 'ar':
    
            if plot_type == 'critical fire':
                x1 = 0.32
                x2 = 0.61
                x3 = None
                y = 0.197
    
            if plot_type == 'dry lightning':
                x1 = 0.31
                x2 = 0.61
                x3 = None
                y = 0.197
    
        if state == 'TX' or state == 'tx':
    
            if plot_type == 'critical fire':
                x1 = 0.26
                x2 = 0.47
                x3 = 0.68
                y = 0.197
    
            if plot_type == 'dry lightning':
                x1 = 0.325
                x2 = 0.585
                x3 = None
                y = 0.195
    
        if state == 'OK' or state == 'ok':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'NM' or state == 'nm':
    
            if plot_type == 'critical fire':
                x1 = 0.3
                x2 = 0.475
                x3 = 0.64
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.365
                x2 = 0.57
                x3 = None
                y = 0.205
    
        if state == 'AZ' or state == 'az':
    
            if plot_type == 'critical fire':
                x1 = 0.3
                x2 = 0.475
                x3 = 0.64
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.365
                x2 = 0.57
                x3 = None
                y = 0.205
    
        if state == 'UT' or state == 'ut':
    
            if plot_type == 'critical fire':
                x1 = 0.3
                x2 = 0.475
                x3 = 0.64
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.365
                x2 = 0.57
                x3 = None
                y = 0.205
    
        if state == 'CO' or state == 'co':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'WY' or state == 'wy':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'MT' or state == 'mt':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'KS' or state == 'ks':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195
    
        if state == 'TN' or state == 'tn':
    
            if plot_type == 'critical fire':
                x1 = 0.2
                x2 = 0.465
                x3 = 0.72
                y = 0.195
    
            if plot_type == 'dry lightning':
                x1 = 0.27
                x2 = 0.64
                x3 = None
                y = 0.195

    if state == None and gacc_region != None:

        if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':
    
            if plot_type == 'critical fire':
                x1 = 0.26
                x2 = 0.47
                x3 = 0.68
                y = 0.2
    
            if plot_type == 'dry lightning':
                x1 = 0.31
                x2 = 0.62
                x3 = None
                y = 0.2

        if gacc_region == 'ONCC' or gacc_region == 'oncc' or gacc_region == 'NOPS' or gacc_region == 'nops':
    
            if plot_type == 'critical fire':
                x1 = 0.32
                x2 = 0.475
                x3 = 0.63
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.35
                x2 = 0.58
                x3 = None
                y = 0.205

        if gacc_region == 'GBCC' or gacc_region == 'gbcc' or gacc_region == 'GB' or gacc_region == 'gb':
    
            if plot_type == 'critical fire':
                x1 = 0.32
                x2 = 0.475
                x3 = 0.63
                y = 0.205
    
            if plot_type == 'dry lightning':
                x1 = 0.35
                x2 = 0.58
                x3 = None
                y = 0.205

        if gacc_region == 'NRCC' or gacc_region == 'nrcc' or gacc_region == 'NR' or gacc_region == 'nr':
    
            if plot_type == 'critical fire':
                x1 = 0.27
                x2 = 0.475
                x3 = 0.685
                y = 0.192
    
            if plot_type == 'dry lightning':
                x1 = 0.32
                x2 = 0.61
                x3 = None
                y = 0.192

        if gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':
    
            if plot_type == 'critical fire':
                x1 = 0.27
                x2 = 0.475
                x3 = 0.685
                y = 0.198
    
            if plot_type == 'dry lightning':
                x1 = 0.32
                x2 = 0.61
                x3 = None
                y = 0.198

        if gacc_region == 'SWCC' or gacc_region == 'swcc' or gacc_region == 'SW' or gacc_region == 'sw':
    
            if plot_type == 'critical fire':
                x1 = 0.27
                x2 = 0.475
                x3 = 0.685
                y = 0.198
    
            if plot_type == 'dry lightning':
                x1 = 0.32
                x2 = 0.61
                x3 = None
                y = 0.198

        if gacc_region == 'SACC' or gacc_region == 'sacc' or gacc_region == 'SE' or gacc_region == 'se':
    
            if plot_type == 'critical fire':
                x1 = 0.27
                x2 = 0.475
                x3 = 0.685
                y = 0.196
    
            if plot_type == 'dry lightning':
                x1 = 0.32
                x2 = 0.61
                x3 = None
                y = 0.196

        if gacc_region == 'EACC' or gacc_region == 'eacc' or gacc_region == 'E' or gacc_region == 'e':
    
            if plot_type == 'critical fire':
                x1 = 0.27
                x2 = 0.475
                x3 = 0.685
                y = 0.196
    
            if plot_type == 'dry lightning':
                x1 = 0.32
                x2 = 0.61
                x3 = None
                y = 0.196

        if gacc_region == 'PNW' or gacc_region == 'pnw' or gacc_region == 'NWCC' or gacc_region == 'nwcc' or gacc_region == 'NW' or gacc_region == 'nw':
    
            if plot_type == 'critical fire':
                x1 = 0.29
                x2 = 0.475
                x3 = 0.65
                y = 0.202
    
            if plot_type == 'dry lightning':
                x1 = 0.33
                x2 = 0.6
                x3 = None
                y = 0.202

    return x1, x2, x3, y

def get_colorbar_coords(state, gacc_region):

    if state != None and gacc_region == None:

        if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':

            x1, x2, y, x_size, fontsize = 0.18, 0.55, 0.25, 0.45, 12

        if state == 'AK' or state == 'ak':

            x1, x2, y, x_size, fontsize = 0.18, 0.55, 0.28, 0.45, 12

        if state == 'CA' or state == 'ca':

            x1, x2, y, x_size, fontsize = 0.19, 0.54, 0.05, 0.3, 12

        if state == 'ME' or state == 'me':

            x1, x2, y, x_size, fontsize = 0.19, 0.54, 0.05, 0.3, 12

        if state == 'NH' or state == 'nh':

            x1, x2, y, x_size, fontsize = 0.25, 0.53, 0.05, 0.25, 12

        if state == 'VT' or state == 'vt':

            x1, x2, y, x_size, fontsize = 0.25, 0.53, 0.05, 0.25, 12

        if state == 'MA' or state == 'ma':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.15, 0.35, 12

        if state == 'RI' or state == 'ri':

            x1, x2, y, x_size, fontsize = 0.2, 0.55, 0.05, 0.27, 12

        if state == 'CT' or state == 'ct':

            x1, x2, y, x_size, fontsize = 0.18, 0.55, 0.05, 0.3, 12

        if state == 'NJ' or state == 'nj':

            x1, x2, y, x_size, fontsize = 0.29, 0.58, 0.05, 0.15, 7

        if state == 'DE' or state == 'de':

            x1, x2, y, x_size, fontsize = 0.29, 0.58, 0.05, 0.15, 7

        if state == 'NY' or state == 'ny':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.15, 0.35, 12

        if state == 'PA' or state == 'pa':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.2, 0.35, 12

        if state == 'OH' or state == 'oh':

            x1, x2, y, x_size, fontsize = 0.19, 0.54, 0.05, 0.31, 12

        if state == 'MI' or state == 'mi':

            x1, x2, y, x_size, fontsize = 0.19, 0.54, 0.05, 0.33, 12

        if state == 'MN' or state == 'mn':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.15, 0.33, 12

        if state == 'WI' or state == 'wi':

            x1, x2, y, x_size, fontsize = 0.13, 0.54, 0.05, 0.36, 12

        if state == 'IA' or state == 'ia':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.2, 0.35, 12

        if state == 'IN' or state == 'in':

            x1, x2, y, x_size, fontsize = 0.29, 0.53, 0.05, 0.2, 7

        if state == 'MO' or state == 'mo':

            x1, x2, y, x_size, fontsize = 0.14, 0.54, 0.12, 0.36, 12

        if state == 'IL' or state == 'il':

            x1, x2, y, x_size, fontsize = 0.31, 0.53, 0.05, 0.2, 7

        if state == 'ND' or state == 'nd':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.2, 0.35, 12

        if state == 'SD' or state == 'sd':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.2, 0.35, 12

        if state == 'NE' or state == 'ne':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.24, 0.35, 12

        if state == 'MD' or state == 'md':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.24, 0.35, 12

        if state == 'VA' or state == 'va':

            x1, x2, y, x_size, fontsize = 0.14, 0.55, 0.24, 0.35, 12

        if state == 'SC' or state == 'sc':

            x1, x2, y, x_size, fontsize = 0.14, 0.54, 0.12, 0.36, 12

        if state == 'KY' or state == 'ky':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.24, 0.35, 12

        if state == 'WV' or state == 'wv':

            x1, x2, y, x_size, fontsize = 0.12, 0.52, 0.05, 0.36, 12

        if state == 'NC' or state == 'nc':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.24, 0.35, 12

        if state == 'NV' or state == 'nv':

            x1, x2, y, x_size, fontsize = 0.25, 0.53, 0.05, 0.25, 12

        if state == 'FL' or state == 'fl':

            x1, x2, y, x_size, fontsize = 0.14, 0.54, 0.07, 0.36, 12

        if state == 'OR' or state == 'or':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.2, 0.35, 12

        if state == 'WA' or state == 'wa':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.2, 0.35, 12

        if state == 'ID' or state == 'id':

            x1, x2, y, x_size, fontsize = 0.26, 0.52, 0.05, 0.23, 12

        if state == 'GA' or state == 'ga':

            x1, x2, y, x_size, fontsize = 0.25, 0.53, 0.07, 0.25, 12

        if state == 'AL' or state == 'al':

            x1, x2, y, x_size, fontsize = 0.28, 0.54, 0.07, 0.2, 12

        if state == 'MS' or state == 'ms':

            x1, x2, y, x_size, fontsize = 0.29, 0.53, 0.07, 0.18, 12

        if state == 'LA' or state == 'la':

            x1, x2, y, x_size, fontsize = 0.16, 0.53, 0.07, 0.33, 12

        if state == 'AR' or state == 'ar':

            x1, x2, y, x_size, fontsize = 0.16, 0.53, 0.07, 0.34, 12

        if state == 'TX' or state == 'tx':

            x1, x2, y, x_size, fontsize = 0.16, 0.53, 0.07, 0.34, 12

        if state == 'OK' or state == 'ok':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.25, 0.35, 12

        if state == 'NM' or state == 'nm':

            x1, x2, y, x_size, fontsize = 0.22, 0.53, 0.07, 0.25, 12

        if state == 'AZ' or state == 'az':

            x1, x2, y, x_size, fontsize = 0.22, 0.53, 0.07, 0.25, 12

        if state == 'UT' or state == 'ut':

            x1, x2, y, x_size, fontsize = 0.24, 0.53, 0.07, 0.26, 12

        if state == 'CO' or state == 'co':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.15, 0.35, 12

        if state == 'WY' or state == 'wy':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.15, 0.35, 12

        if state == 'MT' or state == 'mt':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.24, 0.35, 12

        if state == 'KS' or state == 'ks':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.24, 0.35, 12

        if state == 'TN' or state == 'tn':

            x1, x2, y, x_size, fontsize = 0.13, 0.55, 0.33, 0.35, 12

    if state == None and gacc_region != None:

        if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':

            x1, x2, y, x_size, fontsize = 0.13, 0.53, 0.07, 0.37, 12

        if gacc_region == 'ONCC' or gacc_region == 'oncc' or gacc_region == 'NOPS' or gacc_region == 'nops':

            x1, x2, y, x_size, fontsize = 0.22, 0.55, 0.07, 0.25, 12

        if gacc_region == 'GBCC' or gacc_region == 'gbcc' or gacc_region == 'GB' or gacc_region == 'gb':

            x1, x2, y, x_size, fontsize = 0.2, 0.53, 0.07, 0.3, 12

        if gacc_region == 'NRCC' or gacc_region == 'nrcc' or gacc_region == 'NR' or gacc_region == 'nr':

            x1, x2, y, x_size, fontsize = 0.13, 0.53, 0.19, 0.36, 12

        if gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':

            x1, x2, y, x_size, fontsize = 0.13, 0.54, 0.15, 0.35, 12

        if gacc_region == 'SWCC' or gacc_region == 'swcc' or gacc_region == 'SW' or gacc_region == 'sw':

            x1, x2, y, x_size, fontsize = 0.13, 0.54, 0.18, 0.35, 12

        if gacc_region == 'SACC' or gacc_region == 'sacc' or gacc_region == 'SE' or gacc_region == 'se':

            x1, x2, y, x_size, fontsize = 0.13, 0.54, 0.18, 0.35, 12

        if gacc_region == 'EACC' or gacc_region == 'eacc' or gacc_region == 'E' or gacc_region == 'e':

            x1, x2, y, x_size, fontsize = 0.13, 0.54, 0.16, 0.35, 12

        if gacc_region == 'PNW' or gacc_region == 'pnw' or gacc_region == 'NWCC' or gacc_region == 'nwcc' or gacc_region == 'NW' or gacc_region == 'nw':

            x1, x2, y, x_size, fontsize = 0.17, 0.54, 0.07, 0.3, 12

    return x1, x2, y, x_size, fontsize
        
