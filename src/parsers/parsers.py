# THIS SCRIPT HAS FUNCTIONS THAT PARSE THROUGH GRIB FILES THAT CONTAIN WEATHER DATA TO RETURN SORTED AND ORGANIZED DATA ARRAYS FOR GRAPHICAL CREATION/PLOTTING
#
# DEPENDENCIES INCLUDE:
# 1. PYGRIB
# 2. DATETIME
#
#  (C) METEOROLOGIST ERIC J. DREWITZ
#               USDA/USFS

##### IMPORTS NEEDED PYTHON MODULES #######

import pygrib
from datetime import datetime, timedelta

def GRIB_temperature_conversion(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files):

    r'''
    THIS FUNCTION CONVERTS THE TEMPERATURE VALUES FROM KELVIN TO FAHRENHEIT FOR OUR PLOT

    RETURNS: TEMPERATURE VALUES IN FAHRENHEIT

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
    '''

    frac = 9/5
    if count_of_GRIB_files == 1:
        grb_1_vals = first_GRIB_file.values
        celsius = grb_1_vals - 273.15
        fahrenheit = (frac * celsius) + 32
        grb_1_vals = fahrenheit

        grb_2_vals = None
        grb_3_vals = None
        grb_4_vals = None
        grb_5_vals = None
            
        return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals

    if count_of_GRIB_files == 2:
        grb_1_vals = first_GRIB_file.values
        grb_2_vals = second_GRIB_file.values
        
        celsius_1 = grb_1_vals - 273.15
        fahrenheit_1 = (frac * celsius_1) + 32
        grb_1_vals = fahrenheit_1
            
        celsius_2 = grb_2_vals - 273.15
        fahrenheit_2 = (frac * celsius_2) + 32
        grb_2_vals = fahrenheit_2

        grb_3_vals = None
        grb_4_vals = None
        grb_5_vals = None
            
        return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals

    if count_of_GRIB_files == 3:
        grb_1_vals = first_GRIB_file.values
        grb_2_vals = second_GRIB_file.values
        grb_3_vals = third_GRIB_file.values
        
        celsius_1 = grb_1_vals - 273.15
        fahrenheit_1 = (frac * celsius_1) + 32
        grb_1_vals = fahrenheit_1
            
        celsius_2 = grb_2_vals - 273.15
        fahrenheit_2 = (frac * celsius_2) + 32
        grb_2_vals = fahrenheit_2

        celsius_3 = grb_3_vals - 273.15
        fahrenheit_3 = (frac * celsius_3) + 32
        grb_3_vals = fahrenheit_3

        grb_4_vals = None
        grb_5_vals = None

        return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals

    if count_of_GRIB_files == 4:
        grb_1_vals = first_GRIB_file.values
        grb_2_vals = second_GRIB_file.values
        grb_3_vals = third_GRIB_file.values
        grb_4_vals = fourth_GRIB_file.values

        celsius_1 = grb_1_vals - 273.15
        fahrenheit_1 = (frac * celsius_1) + 32
        grb_1_vals = fahrenheit_1
            
        celsius_2 = grb_2_vals - 273.15
        fahrenheit_2 = (frac * celsius_2) + 32
        grb_2_vals = fahrenheit_2

        celsius_3 = grb_3_vals - 273.15
        fahrenheit_3 = (frac * celsius_3) + 32
        grb_3_vals = fahrenheit_3

        celsius_4 = grb_4_vals - 273.15
        fahrenheit_4 = (frac * celsius_4) + 32
        grb_4_vals = fahrenheit_4

        grb_5_vals = None
                
        return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals

    if count_of_GRIB_files >= 5:
        grb_1_vals = first_GRIB_file.values
        grb_2_vals = second_GRIB_file.values
        grb_3_vals = third_GRIB_file.values
        grb_4_vals = fourth_GRIB_file.values
        grb_5_vals = fifth_GRIB_file.values
        
        celsius_1 = grb_1_vals - 273.15
        fahrenheit_1 = (frac * celsius_1) + 32
        grb_1_vals = fahrenheit_1
            
        celsius_2 = grb_2_vals - 273.15
        fahrenheit_2 = (frac * celsius_2) + 32
        grb_2_vals = fahrenheit_2

        celsius_3 = grb_3_vals - 273.15
        fahrenheit_3 = (frac * celsius_3) + 32
        grb_3_vals = fahrenheit_3

        celsius_4 = grb_4_vals - 273.15
        fahrenheit_4 = (frac * celsius_4) + 32
        grb_4_vals = fahrenheit_4

        celsius_5 = grb_5_vals - 273.15
        fahrenheit_5 = (frac * celsius_5) + 32
        grb_5_vals = fahrenheit_5
                
        return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals


def GRIB_parameter_check_temperature(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, parameter):

    r'''
    THIS FUNCTION IS SPECIFICALLY FOR THE CUSTOM GENERIC NWS FORECAST GRAPHIC

    THIS FUNCTION CHECKS TO SEE IF THE PARAMETER BEING USED IS FOR TEMPERATURE SO WE CAN PERFORM THE KELVIN TO FAHRENHEIT CONVERSION IF NEEDED.

    IF THE PARAMETER IS NOT TEMPERATURE, THIS FUNCTION WILL RETURN THE VALUES WITHIN THE GRIB FILE AS THEY ARE

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
    '''

    if parameter == 'ds.maxt.bin' or parameter == 'ds.mint.bin':
        frac = 9/5
        if count_of_GRIB_files == 1:
            grb_1_vals = first_GRIB_file.values
            celsius = grb_1_vals - 273.15
            fahrenheit = (frac * celsius) + 32
            grb_1_vals = fahrenheit
    
            grb_2_vals = None
            grb_3_vals = None
            grb_4_vals = None
            grb_5_vals = None
                
            return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 2:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            
            celsius_1 = grb_1_vals - 273.15
            fahrenheit_1 = (frac * celsius_1) + 32
            grb_1_vals = fahrenheit_1
                
            celsius_2 = grb_2_vals - 273.15
            fahrenheit_2 = (frac * celsius_2) + 32
            grb_2_vals = fahrenheit_2
    
            grb_3_vals = None
            grb_4_vals = None
            grb_5_vals = None
                
            return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 3:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            
            celsius_1 = grb_1_vals - 273.15
            fahrenheit_1 = (frac * celsius_1) + 32
            grb_1_vals = fahrenheit_1
                
            celsius_2 = grb_2_vals - 273.15
            fahrenheit_2 = (frac * celsius_2) + 32
            grb_2_vals = fahrenheit_2
    
            celsius_3 = grb_3_vals - 273.15
            fahrenheit_3 = (frac * celsius_3) + 32
            grb_3_vals = fahrenheit_3
    
            grb_4_vals = None
            grb_5_vals = None
    
            return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 4:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            grb_4_vals = fourth_GRIB_file.values
    
            celsius_1 = grb_1_vals - 273.15
            fahrenheit_1 = (frac * celsius_1) + 32
            grb_1_vals = fahrenheit_1
                
            celsius_2 = grb_2_vals - 273.15
            fahrenheit_2 = (frac * celsius_2) + 32
            grb_2_vals = fahrenheit_2
    
            celsius_3 = grb_3_vals - 273.15
            fahrenheit_3 = (frac * celsius_3) + 32
            grb_3_vals = fahrenheit_3
    
            celsius_4 = grb_4_vals - 273.15
            fahrenheit_4 = (frac * celsius_4) + 32
            grb_4_vals = fahrenheit_4
    
            grb_5_vals = None
                    
            return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals
        
        if count_of_GRIB_files >= 5:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            grb_4_vals = fourth_GRIB_file.values
            grb_5_vals = fifth_GRIB_file.values
            
            celsius_1 = grb_1_vals - 273.15
            fahrenheit_1 = (frac * celsius_1) + 32
            grb_1_vals = fahrenheit_1
                
            celsius_2 = grb_2_vals - 273.15
            fahrenheit_2 = (frac * celsius_2) + 32
            grb_2_vals = fahrenheit_2
    
            celsius_3 = grb_3_vals - 273.15
            fahrenheit_3 = (frac * celsius_3) + 32
            grb_3_vals = fahrenheit_3
    
            celsius_4 = grb_4_vals - 273.15
            fahrenheit_4 = (frac * celsius_4) + 32
            grb_4_vals = fahrenheit_4
    
            celsius_5 = grb_5_vals - 273.15
            fahrenheit_5 = (frac * celsius_5) + 32
            grb_5_vals = fahrenheit_5
                    
            return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals

    else:
        if count_of_GRIB_files == 1:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = None
            grb_3_vals = None
            grb_4_vals = None
            grb_5_vals = None

            return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals
            
        if count_of_GRIB_files == 2:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = None
            grb_4_vals = None
            grb_5_vals = None

            return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals
            
        if count_of_GRIB_files == 3:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            grb_4_vals = None
            grb_5_vals = None

            return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals
            
        if count_of_GRIB_files == 4:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            grb_4_vals = fourth_GRIB_file.values
            grb_5_vals = None

            return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals

        if count_of_GRIB_files >= 5:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            grb_4_vals = fourth_GRIB_file.values
            grb_5_vals = fifth_GRIB_file.values

            return grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals


def parse_SPC_GRIB_data(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files):

    r'''

    THIS FUNCTION PARSES THE SPC DATA AND RETURNS THE DIFFERENT DATA SUCH AS VALUES, VALID DATES/TIMES ETC. NEEDED FOR THE PLOT
    
    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
    '''
    if count_of_GRIB_files == 1:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=24)
            
        grb_2_start = None
        grb_2_end = None
        grb_2_vals = None
            
        grb_3_start = None
        grb_3_end = None
        grb_3_vals = None

    if count_of_GRIB_files == 2:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=24)
        
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=24)
        grb_2_vals = second_GRIB_file.values
        
        grb_3_start = None
        grb_3_end = None
        grb_3_vals = None

    if count_of_GRIB_files == 3:
        grb_1_vals = first_GRIB_file.values
        grb_1_start = first_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=24)
        
        grb_2_vals = second_GRIB_file.values
        grb_2_start = second_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(hours=24)

        grb_3_start = third_GRIB_file.validDate
        grb_3_end = grb_3_start + timedelta(days=7)
        grb_3_vals = third_GRIB_file.values

    if count_of_GRIB_files > 3:
        grb_1_vals = second_GRIB_file.values
        grb_1_start = second_GRIB_file.validDate
        grb_1_end = grb_1_start + timedelta(hours=24)
        
        grb_2_vals = third_GRIB_file.values
        grb_2_start = third_GRIB_file.validDate
        grb_2_end = grb_2_start + timedelta(days=6)

        grb_3_start = None
        grb_3_end = None
        grb_3_vals = None

    return grb_1_start, grb_1_end, grb_1_vals, grb_2_start, grb_2_end, grb_2_vals, grb_3_start, grb_3_end, grb_3_vals
