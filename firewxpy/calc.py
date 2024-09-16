import math
import numpy as np

class unit_conversion:

    r'''
    THIS CLASS HOSTS A VARIETY OF FUNCTIONS TO CONVERT UNITS
    '''

    def meters_per_second_to_mph(rtma_wind):

        return rtma_wind * 2.23694

    def knots_to_mph(wind_speed):

        r'''
        This function converts wind speed from kts to mph
        '''

        mph = wind_speed * 1.15078
        return mph

    def celsius_to_fahrenheit(temperature):

        r'''
        This function converts temperature from celsius to fahrenheit
        '''

        frac = 9/5
        degF = (temperature * frac) + 32
        return degF

    def Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temperature_data_or_dewpoint_data):

        r'''
        THIS FUNCTION TAKES IN THE CURRENT TEMPERATURE OR DEWPOINT DATA ARRAY AND THE TEMPERATURE OR DEWPOINT DATA ARRAY FROM 24 HOURS AGO AND RETURNS THE TEMPERATURE OR DEWPOINT DIFFERENCE. THIS FUNCTION CONVERTS THE DATA FROM KELVIN TO FAHRENHEIT.

        THIS FUNCTION ALSO RETURNS A BLANK PANDAS DATAFRAME IF THERE IS NO DATA AVAILIABLE

        (C) METEOROLOGIST ERIC J. DREWITZ
        '''
        
        degC = temperature_data_or_dewpoint_data - 273.15
        frac = 9/5
        degF = (degC * frac) + 32
        
        return degF


    def Temperature_Data_or_Dewpoint_Data_Kelvin_to_Celsius(temperature_data_or_dewpoint_data):

        r'''
        THIS FUNCTION TAKES IN THE CURRENT TEMPERATURE OR DEWPOINT DATA ARRAY AND THE TEMPERATURE OR DEWPOINT DATA ARRAY FROM 24 HOURS AGO AND RETURNS THE TEMPERATURE OR DEWPOINT DIFFERENCE. THIS FUNCTION CONVERTS THE DATA FROM KELVIN TO FAHRENHEIT.


        (C) METEOROLOGIST ERIC J. DREWITZ
        '''
        
        degC = (temperature_data_or_dewpoint_data - 273.15)

        return degC


    def Temperature_or_Dewpoint_Change_Data_Kelvin_to_Fahrenheit(current_temperature_or_dewpoint_data, temperature_or_dewpoint_data_from_24_hours_ago):

        r'''
        THIS FUNCTION TAKES IN THE CURRENT TEMPERATURE DATA ARRAY AND THE TEMPERATURE DATA ARRAY FROM 24 HOURS AGO AND RETURNS THE TEMPERATURE DIFFERENCE. THIS FUNCTION CONVERTS THE DATA FROM KELVIN TO FAHRENHEIT.

        THIS FUNCTION ALSO RETURNS A BLANK PANDAS DATAFRAME IF THERE IS NO DATA AVAILIABLE

        (C) METEOROLOGIST ERIC J. DREWITZ
        '''
        
        degC = current_temperature_or_dewpoint_data - 273.15
        frac = 9/5
        degF = (degC * frac) + 32
        degC_24 = temperature_or_dewpoint_data_from_24_hours_ago - 273.15
        degF_24 = (degC_24 * frac) + 32
        diff = degF - degF_24
        
        return diff 


    def Temperature_or_Dewpoint_Change_Data_Kelvin_to_Celsius(current_temperature_or_dewpoint_data, temperature_or_dewpoint_data_from_24_hours_ago):

        r'''
        THIS FUNCTION TAKES IN THE CURRENT TEMPERATURE DATA ARRAY AND THE TEMPERATURE DATA ARRAY FROM 24 HOURS AGO AND RETURNS THE TEMPERATURE DIFFERENCE. THIS FUNCTION CONVERTS THE DATA FROM KELVIN TO FAHRENHEIT.

        THIS FUNCTION ALSO RETURNS A BLANK PANDAS DATAFRAME IF THERE IS NO DATA AVAILIABLE

        (C) METEOROLOGIST ERIC J. DREWITZ
        '''
        
        degC = current_temperature_or_dewpoint_data - 273.15
        degC_24 = temperature_or_dewpoint_data_from_24_hours_ago - 273.15
        diff = degC - degC_24
        
        return diff 



    def Temperature_Or_Dewpoint_Change_to_Fahrenheit_24_hour_comparison(current_temperature_or_dewpoint_dataset, temperature_or_dewpoint_dataset_from_24_hours_ago):

        r'''
        THIS FUNCTION PARSES THROUGH THE TEMPERATURE CHANGE AND RETURNS THE TEMPERATURE CHANGE. THIS FUNCTION CONVERTS THE DATA ARRAY FROM KELVIN TO FAHRENHEIT


        (C) METEOROLOGIST ERIC J. DREWITZ

        '''
        
        degF = current_temperature_dataset * 1.8
        degF_24 = temperature_dataset_from_24_hours_ago * 1.8

        return degF, degF_24

    def Temperature_Or_Dewpoint_Change_to_Fahrenheit(current_temperature_or_dewpoint_dataset):

        r'''
        THIS FUNCTION PARSES THROUGH THE TEMPERATURE CHANGE AND RETURNS THE TEMPERATURE CHANGE. THIS FUNCTION CONVERTS THE DATA ARRAY FROM KELVIN TO FAHRENHEIT


        (C) METEOROLOGIST ERIC J. DREWITZ

        '''

        return current_temperature_or_dewpoint_dataset * 1.8


    def longitude_correction(longitude):

        long_diff = longitude - 180

        new_coords = (180 - long_diff) * -1

        return new_coords
        

class Thermodynamics:

    def saturation_vapor_pressure(temperature):

        r'''
        This function calculates the saturation vapor pressure from temperature.
        This function uses the formula from Bolton 1980.         

        '''

        e = 6.112 * np.exp(17.67 * (temperature) / (temperature + 243.5))
        return e


    def relative_humidity_from_temperature_and_dewpoint_celsius(temperature, dewpoint):

        r'''
        This function calculates the relative humidity from temperature and dewpoint. 
        '''

        e = Thermodynamics.saturation_vapor_pressure(dewpoint)
        e_s = Thermodynamics.saturation_vapor_pressure(temperature)
        return (e / e_s) * 100
    def find_mixing_height(temperature, height, df_len):
        temperture = temperature
        height = height
        df_len = df_len - 1
        vals = []
        i = 0
        for i in range(0, df_len):
            if temperature[i+1] >= temperature[i]:
                val = height[i+1]
                vals.append(val)
    
        mixing_height = vals[0]
        return round(mixing_height * 3.28084, 1)

class scaling:

    def get_nomads_decimation(western_bound, eastern_bound, southern_bound, northern_bound, barbs):

        western_bound_init = -122
        eastern_bound_init = -114
        southern_bound_init = 32
        northern_bound_init = 41

        wb_init = abs(western_bound_init)
        eb_init = abs(eastern_bound_init)
        nb_init = abs(northern_bound_init)
        sb_init = abs(southern_bound_init)

        L1_init = wb_init - eb_init
        L2_init = nb_init - sb_init

        A_init = L1_init * L2_init

        wb = abs(western_bound)
        eb = abs(eastern_bound)
        nb = abs(northern_bound)
        sb = abs(southern_bound)

        L1 = wb - eb
        L2 = nb - sb

        A = L1 * L2

        if barbs == False:
            decimate_init = 30

        if barbs == True:
            decimate_init = 40

        decimate = (A * decimate_init) / A_init

        decimate = int(round(decimate, -1))

        if A > A_init:
            decimate = int(round((decimate / 2), 0))
            if decimate > 100:
                decimate = 100
        else:
            decimate = decimate

        return decimate


    def get_rtma_decimation(western_bound, eastern_bound, southern_bound, northern_bound, barbs):

        western_bound_init = -122
        eastern_bound_init = -114
        southern_bound_init = 32
        northern_bound_init = 40

        wb_init = abs(western_bound_init)
        eb_init = abs(eastern_bound_init)
        nb_init = abs(northern_bound_init)
        sb_init = abs(southern_bound_init)

        L1_init = wb_init - eb_init
        L2_init = nb_init - sb_init

        A_init = L1_init * L2_init

        wb = abs(western_bound)
        eb = abs(eastern_bound)
        nb = abs(northern_bound)
        sb = abs(southern_bound)

        L1 = wb - eb
        L2 = nb - sb

        A = L1 * L2

        decimate_init = 1800

        decimate = (A * decimate_init) / A_init

        decimate = int(round(decimate, -2))

        west = 124
        east = 67
        south = 25
        north = 49

        Lwe_conus = west - east
        Lns_conus = north - south
        A_conus = Lwe_conus * Lns_conus

        if A > A_init:
            decimate = (int(round((decimate / 2), 0))) + 200
            if barbs == True:
                decimate = decimate + 800
            if barbs == None:
                Anew = A_init *2.5
                if A > Anew:
                    decimate = decimate + 800
                else:
                    decimate = decimate + 500
                if A >= A_conus:
                    decimate = decimate * 2
                else:
                    decimate = decimate
            else:
                if A >= A_conus:
                    decimate = decimate * 2
                else:
                    decimate = decimate
        elif A < A_init:
            decimate = int(round((decimate / 2), 0))
            if barbs == None:
                Alow = A_init/2
                if A < Alow:
                    decimate = decimate -500

        else:
            decimate = decimate

        return decimate

    def get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, directory_name):

        directory_name = directory_name
        
        western_bound_init = -122
        eastern_bound_init = -114
        southern_bound_init = 32
        northern_bound_init = 40

        wb_init = abs(western_bound_init)
        eb_init = abs(eastern_bound_init)
        nb_init = abs(northern_bound_init)
        sb_init = abs(southern_bound_init)

        L1_init = wb_init - eb_init
        L2_init = nb_init - sb_init

        A_init = L1_init * L2_init

        wb = abs(western_bound)
        eb = abs(eastern_bound)
        nb = abs(northern_bound)
        sb = abs(southern_bound)

        L1 = wb - eb
        L2 = nb - sb

        A = L1 * L2

        if directory_name == 'CONUS':
            decimate_init = 2100
        elif directory_name == 'Northeast' or directory_name == 'northeast' or directory_name == 'neast' or directory_name == 'NE' or directory_name == 'ne' or directory_name == 'NEAST' or directory_name == 'Neast':
            decimate_init = 300

        elif directory_name == 'Central Great Lakes' or directory_name == 'CGL' or directory_name == 'central great lakes' or directory_name == 'cgl':
            decimate_init = 350

        elif directory_name == 'Eastern Great Lakes' or directory_name == 'eastern great lakes' or directory_name == 'EGL' or directory_name == 'egl':
            decimate_init = 250

        elif directory_name == 'Northern Plains' or directory_name == 'NORTHERN PLAINS' or directory_name == 'northern plains' or directory_name == 'NP' or directory_name == 'np' or directory_name == 'NPLAINS' or directory_name == 'nplains':
            decimate_init = 200

        elif directory_name == 'Central Plains' or directory_name == 'central plains' or directory_name == 'CP' or directory_name == 'cp':
            decimate_init = 200

        elif directory_name == 'Central Rockies' or directory_name == 'central rockies' or directory_name == 'CR' or directory_name == 'cr':
            decimate_init = 300

        elif directory_name == 'Northern Rockies' or directory_name == 'northern rockies' or directory_name == 'NR' or directory_name == 'nr':
            decimate_init = 350

        elif directory_name == 'Southern Rockies' or directory_name == 'southern rockies' or directory_name == 'SR' or directory_name == 'sr':
            decimate_init = 200

        elif directory_name == 'Mid Atlantic' or directory_name == 'Mid-Atlantic' or directory_name == 'mid atlantic' or directory_name == 'mid-atlantic' or directory_name == 'ma' or directory_name == 'Mid Atl' or directory_name == 'mid atl' or directory_name == 'Mid-Atl' or directory_name == 'mid-atl':
            decimate_init = 250
        
        else:
            decimate_init = 900

        decimate = (A * decimate_init) / A_init

        decimate = int(round(decimate, -2))

        west = 124
        east = 67
        south = 25
        north = 49

        Lwe_conus = west - east
        Lns_conus = north - south
        A_conus = Lwe_conus * Lns_conus

        if A > A_init:
            decimate = (int(round((decimate / 2), 0))) + 500

            if A >= A_conus:
                decimate = decimate * 2
            else:
                decimate = decimate

        elif A < A_init:
            decimate = int(round((decimate / 2), 0))

        else:
            decimate = decimate

        return decimate

    def get_rtma_decimation_by_state(state):
        
        state = state

        if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
            decimation = 11300
        if state == 'ME' or state =='me':
            decimation = 300
        if state == 'NH' or state =='nh':
            decimation = 300
        if state == 'VT' or state =='vt':
            decimation = 300
        if state == 'MA' or state =='ma':
            decimation = 300
        if state == 'RI' or state =='ri':
            decimation = 100
        if state == 'CT' or state =='ct':
            decimation = 300
        if state == 'NJ' or state =='nj':
            decimation = 300
        if state == 'DE' or state =='de':
            decimation = 100
        if state == 'NY' or state =='ny':
            decimation = 300
        if state == 'PA' or state =='pa':
            decimation = 300

        return decimation
        
    def get_NDFD_decimation_by_state(state):

        state = state
        
        if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
            decimate = 5525
        if state == 'AK' or state == 'ak':
            decimate = 4025           
        if state == 'HI' or state == 'hi':
            decimate = 4025           
        if state == 'ME' or state == 'me':
            decimate = 100
        if state == 'NH' or state == 'nh':
            decimate = 30
        if state == 'VT' or state == 'vt':
            decimate = 30
        if state == 'NY' or state == 'ny':
            decimate = 2100
        if state == 'MA' or state == 'ma':
            decimate = 30
        if state == 'RI' or state == 'ri':
            decimate = 10
        if state == 'CT' or state == 'ct':
            decimate = 30
        if state == 'NJ' or state == 'nj':
            decimate = 30
        if state == 'DE' or state == 'de':
            decimate = 30
        if state == 'PA' or state == 'pa':
            decimate = 2100
        if state == 'OH' or state == 'oh':
            decimate = 2100
        if state == 'MI' or state == 'mi':
            decimate = 2100
        if state == 'MN' or state == 'mn':
            decimate = 225
        if state == 'ND' or state == 'nd':
            decimate = 225
        if state == 'SD' or state == 'sd':
            decimate = 225
        if state == 'NE' or state == 'ne':
            decimate = 225
        if state == 'MD' or state == 'md':
            decimate = 2100
        if state == 'VA' or state == 'va':
            decimate = 125
        if state == 'WV' or state == 'wv':
            decimate = 210
        if state == 'NC' or state == 'nc':
            decimate = 125
        if state == 'SC' or state == 'sc':
            decimate = 125
        if state == 'CA' or state == 'ca':
            decimate = 2100
        if state == 'NV' or state == 'nv':
            decimate = 2100
        if state == 'FL' or state == 'fl':
            decimate = 200
        if state == 'OR' or state == 'or':
            decimate = 200
        if state == 'WA' or state == 'wa':
            decimate = 200
        if state == 'ID' or state == 'id':
            decimate = 200
        if state == 'GA' or state == 'ga':
            decimate = 2100
        if state == 'AL' or state == 'al':
            decimate = 2100
        if state == 'MS' or state == 'ms':
            decimate = 90
        if state == 'LA' or state == 'la':
            decimate = 90
        if state == 'AR' or state == 'ar':
            decimate = 90
        if state == 'TX' or state == 'tx':
            decimate = 300
        if state == 'OK' or state == 'ok':
            decimate = 300
        if state == 'NM' or state == 'nm':
            decimate = 2100
        if state == 'AZ' or state == 'az':
            decimate = 900
        if state == 'UT' or state == 'ut':
            decimate = 600
        if state == 'CO' or state == 'co':
            decimate = 600
        if state == 'WY' or state == 'wy':
            decimate = 125
        if state == 'MT' or state == 'mt':
            decimate = 225
        if state == 'KS' or state == 'ks':
            decimate = 125
        if state == 'WI' or state == 'wi':
            decimate = 100 
        if state == 'IA' or state == 'ia':
            decimate = 100 
        if state == 'IN' or state == 'in':
            decimate = 30 
        if state == 'IL' or state == 'il':
            decimate = 2100
        if state == 'MO' or state == 'mo':
            decimate = 90
        if state == 'KY' or state == 'ky':
            decimate = 2100
        if state == 'TN' or state == 'tn':
            decimate = 2100

        return decimate


    def get_NDFD_decimation_by_gacc_region(gacc_region):

        gacc_region = gacc_region

        if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops':
            decimate = 900

        if gacc_region == 'ONCC' or gacc_region == 'oncc' or gacc_region == 'NOPS' or gacc_region == 'nops':
            decimate = 2100
            
        if gacc_region == 'PNW' or gacc_region == 'pnw' or gacc_region == 'NWCC' or gacc_region == 'nwcc' or gacc_region == 'NW' or gacc_region == 'nw':
            decimate = 200

        if gacc_region == 'GBCC' or gacc_region == 'gbcc' or gacc_region == 'GB' or gacc_region == 'gb':
            decimate = 2100

        if gacc_region == 'NRCC' or gacc_region == 'nrcc' or gacc_region == 'NR' or gacc_region == 'nr':
            decimate = 2100

        if gacc_region == 'SWCC' or gacc_region == 'swcc' or gacc_region == 'SW' or gacc_region == 'sw':
            decimate = 2100

        if gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':
            decimate = 2100

        if gacc_region == 'SACC' or gacc_region == 'sacc' or gacc_region == 'SE' or gacc_region == 'se':
            decimate = 6525

        if gacc_region == 'EACC' or gacc_region == 'eacc' or gacc_region == 'E' or gacc_region == 'e':
            decimate = 6525

        return decimate


class contouring:

    def get_label_levels(start, stop, step):

        start=start
        stop=stop
        step=step

        levels = []

        levels.append(start)
        for i in range(start, stop):
            val = ((start + step) * i) + step
            if val < stop:
                levels.append(val)             

        levels.append(stop)

        return levels

        

        
