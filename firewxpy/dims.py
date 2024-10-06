

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

        if state == 'FL' or state == 'fl':

            x_coord = 0.81
            y_coord = 0.9

    if state == None and gacc_region != None:

        if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':

            x_coord = 0.82
            y_coord = 0.9     
    
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


    return row1, row2, row3, row4, row5, row6, col1, col2, col3, col4, col5, col6 


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

def get_colorbar_coords(state, gacc_region):

    if state != None and gacc_region == None:

        if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':

            x1, x2, y, x_size, fontsize = 0.18, 0.55, 0.25, 0.3, 12

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

    return x1, x2, y, x_size, fontsize
        
