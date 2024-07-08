import math
import numpy as np

class unit_conversion:

    r'''
    THIS CLASS HOSTS A VARIETY OF FUNCTIONS TO CONVERT UNITS
    '''

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


    def get_thredds_decimation(western_bound, eastern_bound, southern_bound, northern_bound, barbs):

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


        
        






        
