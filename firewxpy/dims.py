

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
