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
