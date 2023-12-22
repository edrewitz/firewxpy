
class unit_conversion:

    r'''
    THIS CLASS HOSTS A VARIETY OF FUNCTIONS TO CONVERT UNITS
    '''

    def RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temperature_data_or_dewpoint_data):

        r'''
        THIS FUNCTION TAKES IN THE CURRENT TEMPERATURE OR DEWPOINT DATA ARRAY AND THE TEMPERATURE OR DEWPOINT DATA ARRAY FROM 24 HOURS AGO AND RETURNS THE TEMPERATURE OR DEWPOINT DIFFERENCE. THIS FUNCTION CONVERTS THE DATA FROM KELVIN TO FAHRENHEIT.

        THIS FUNCTION ALSO RETURNS A BLANK PANDAS DATAFRAME IF THERE IS NO DATA AVAILIABLE

        (C) METEOROLOGIST ERIC J. DREWITZ
        '''
        
        degC = temperature_data_or_dewpoint_data - 273.15
        frac = 9/5
        degF = (degC * frac) + 32
        
        return degF


    def RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Celsius(temperature_data_or_dewpoint_data):

        r'''
        THIS FUNCTION TAKES IN THE CURRENT TEMPERATURE OR DEWPOINT DATA ARRAY AND THE TEMPERATURE OR DEWPOINT DATA ARRAY FROM 24 HOURS AGO AND RETURNS THE TEMPERATURE OR DEWPOINT DIFFERENCE. THIS FUNCTION CONVERTS THE DATA FROM KELVIN TO FAHRENHEIT.


        (C) METEOROLOGIST ERIC J. DREWITZ
        '''
        
        degC = (temperature_data_or_dewpoint_data - 273.15)

        return degC


    def RTMA_Temperature_or_Dewpoint_Change_Data_Kelvin_to_Fahrenheit(current_temperature_or_dewpoint_data, temperature_or_dewpoint_data_from_24_hours_ago):

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


    def RTMA_Temperature_or_Dewpoint_Change_Data_Kelvin_to_Celsius(current_temperature_or_dewpoint_data, temperature_or_dewpoint_data_from_24_hours_ago):

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
