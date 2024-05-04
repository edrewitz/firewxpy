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
import numpy as np
import data_access as da
import matplotlib.pyplot as plt
import imageio
import os.path, time

from datetime import datetime, timedelta
from metpy.units import units

class NDFD:

    r'''
    THIS CLASS HOSTS A VARIETY OF FUNCTIONS TO PARSE THROUGH THE NWS NDFD GRIB DATA

    '''

    def figure_count(figure_list):
    
        figure_list = figure_list
        for i in figure_list:
            i = i + 1
            return i
    

    def GRIB_temperature_conversion_test(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files):
    
        r'''
        THIS FUNCTION CONVERTS THE TEMPERATURE VALUES FROM KELVIN TO FAHRENHEIT FOR OUR PLOT
    
        RETURNS: TEMPERATURE VALUES IN FAHRENHEIT
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
    
        frac = 9/5
        if count_of_GRIB_files == 1:
            grb_1_vals = first_GRIB_file.values
            grb_1_vals_f = (frac * (grb_1_vals - 273.15)) + 32
    
            grb_2_vals = None
            grb_3_vals = None
            grb_4_vals = None
            grb_5_vals = None
                
            return grb_1_vals_f, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 2:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            
            grb_1_vals_f = (frac * (grb_1_vals - 273.15)) + 32

            grb_2_vals_f = (frac * (grb_2_vals - 273.15)) + 32

            grb_3_vals = None
            grb_4_vals = None
            grb_5_vals = None
                
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 3:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            
            grb_1_vals_f = (frac * (grb_1_vals - 273.15)) + 32

            grb_2_vals_f = (frac * (grb_2_vals - 273.15)) + 32

            grb_3_vals_f = (frac * (grb_3_vals - 273.15)) + 32
    
            grb_4_vals = None
            grb_5_vals = None
    
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals_f, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 4:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            grb_4_vals = fourth_GRIB_file.values
    
            grb_1_vals_f = (frac * (grb_1_vals - 273.15)) + 32

            grb_2_vals_f = (frac * (grb_2_vals - 273.15)) + 32

            grb_3_vals_f = (frac * (grb_3_vals - 273.15)) + 32

            grb_4_vals_f = (frac * (grb_4_vals - 273.15)) + 32

            grb_1_vals_f = units('degF') * grb_1_vals_f
            grb_2_vals_f = units('degF') * grb_2_vals_f
            grb_3_vals_f = units('degF') * grb_3_vals_f
            grb_4_vals_f = units('degF') * grb_4_vals_f

            grb_5_vals = None
                    
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals_f, grb_4_vals_f, grb_5_vals
    
        if count_of_GRIB_files >= 5:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            grb_4_vals = fourth_GRIB_file.values
            grb_5_vals = fifth_GRIB_file.values
            
            grb_1_vals_f = (frac * (grb_1_vals - 273.15)) + 32

            grb_2_vals_f = (frac * (grb_2_vals - 273.15)) + 32

            grb_3_vals_f = (frac * (grb_3_vals - 273.15)) + 32

            grb_4_vals_f = (frac * (grb_4_vals - 273.15)) + 32

            grb_5_vals_f = (frac * (grb_5_vals - 273.15)) + 32          
                    
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals_f, grb_4_vals_f, grb_5_vals_f


    def GRIB_temperature_conversion_test1(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files):
    
        r'''
        THIS FUNCTION CONVERTS THE TEMPERATURE VALUES FROM KELVIN TO FAHRENHEIT FOR OUR PLOT
    
        RETURNS: TEMPERATURE VALUES IN FAHRENHEIT
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
    
        frac = 9/5
        if count_of_GRIB_files == 1:
            grb_1_vals = first_GRIB_file.values
            grb_1_vals_f = (frac * (grb_1_vals - 273.15)) + 32
    
            grb_2_vals = None
            grb_3_vals = None
            grb_4_vals = None
            grb_5_vals = None
                
            return grb_1_vals_f, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 2:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            
            grb_1_vals_k = units('kelvin') * grb_1_vals
            grb_1_vals_f = grb_1_vals_k.to('degF')

            grb_2_vals_k = units('kelvin') * grb_2_vals
            grb_2_vals_f = grb_2_vals_k.to('degF')

            grb_3_vals = None
            grb_4_vals = None
            grb_5_vals = None
                
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 3:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            
            grb_1_vals_f = (frac * (grb_1_vals - 273.15)) + 32

            grb_2_vals_f = (frac * (grb_2_vals - 273.15)) + 32

            grb_3_vals_f = (frac * (grb_3_vals - 273.15)) + 32
    
            grb_4_vals = None
            grb_5_vals = None
    
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals_f, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 4:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            grb_4_vals = fourth_GRIB_file.values
    
            grb_1_vals_k = units('kelvin') * grb_1_vals
            grb_1_vals_f = grb_1_vals_k.to('degF')

            grb_2_vals_k = units('kelvin') * grb_2_vals
            grb_2_vals_f = grb_2_vals_k.to('degF')

            grb_3_vals_k = units('kelvin') * grb_3_vals
            grb_3_vals_f = grb_3_vals_k.to('degF')

            grb_4_vals_k = units('kelvin') * grb_4_vals
            grb_4_vals_f = grb_4_vals_k.to('degF') 

            grb_5_vals = None
                    
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals_f, grb_4_vals_f, grb_5_vals
            
        if count_of_GRIB_files >= 5:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            grb_4_vals = fourth_GRIB_file.values
            grb_5_vals = fifth_GRIB_file.values
            
            grb_1_vals_k = units('kelvin') * grb_1_vals
            grb_1_vals_f = grb_1_vals_k.to('degF')

            grb_2_vals_k = units('kelvin') * grb_2_vals
            grb_2_vals_f = grb_2_vals_k.to('degF')

            grb_3_vals_k = units('kelvin') * grb_3_vals
            grb_3_vals_f = grb_3_vals_k.to('degF')

            grb_4_vals_k = units('kelvin') * grb_4_vals
            grb_4_vals_f = grb_4_vals_k.to('degF')

            grb_5_vals_k = units('kelvin') * grb_5_vals
            grb_5_vals_f = grb_5_vals_k.to('degF')            
                    
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals_f, grb_4_vals_f, grb_5_vals_f


    def GRIB_temperature_conversion(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files):
    
        r'''
        THIS FUNCTION CONVERTS THE TEMPERATURE VALUES FROM KELVIN TO FAHRENHEIT FOR OUR PLOT
    
        RETURNS: TEMPERATURE VALUES IN FAHRENHEIT
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
    
        frac = 9/5
        if count_of_GRIB_files == 1:
            grb_1_vals = first_GRIB_file.values
            grb_1_vals_k = units('kelvin') * grb_1_vals
            grb_1_vals_f = grb_1_vals_k.to('degF')
    
            grb_2_vals = None
            grb_3_vals = None
            grb_4_vals = None
            grb_5_vals = None
                
            return grb_1_vals_f, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 2:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            
            grb_1_vals_k = units('kelvin') * grb_1_vals
            grb_1_vals_f = grb_1_vals_k.to('degF')

            grb_2_vals_k = units('kelvin') * grb_2_vals
            grb_2_vals_f = grb_2_vals_k.to('degF')

            grb_3_vals = None
            grb_4_vals = None
            grb_5_vals = None
                
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 3:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            
            grb_1_vals_k = units('kelvin') * grb_1_vals
            grb_1_vals_f = grb_1_vals_k.to('degF')

            grb_2_vals_k = units('kelvin') * grb_2_vals
            grb_2_vals_f = grb_2_vals_k.to('degF')

            grb_3_vals_k = units('kelvin') * grb_3_vals
            grb_3_vals_f = grb_3_vals_k.to('degF')
    
            grb_4_vals = None
            grb_5_vals = None
    
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals_f, grb_4_vals, grb_5_vals
    
        if count_of_GRIB_files == 4:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            grb_4_vals = fourth_GRIB_file.values
    
            grb_1_vals_k = units('kelvin') * grb_1_vals
            grb_1_vals_f = grb_1_vals_k.to('degF')

            grb_2_vals_k = units('kelvin') * grb_2_vals
            grb_2_vals_f = grb_2_vals_k.to('degF')

            grb_3_vals_k = units('kelvin') * grb_3_vals
            grb_3_vals_f = grb_3_vals_k.to('degF')

            grb_4_vals_k = units('kelvin') * grb_4_vals
            grb_4_vals_f = grb_4_vals_k.to('degF')            
    
            grb_5_vals = None
                    
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals_f, grb_4_vals_f, grb_5_vals
    
        if count_of_GRIB_files >= 5:
            grb_1_vals = first_GRIB_file.values
            grb_2_vals = second_GRIB_file.values
            grb_3_vals = third_GRIB_file.values
            grb_4_vals = fourth_GRIB_file.values
            grb_5_vals = fifth_GRIB_file.values
            
            grb_1_vals_k = units('kelvin') * grb_1_vals
            grb_1_vals_f = grb_1_vals_k.to('degF')

            grb_2_vals_k = units('kelvin') * grb_2_vals
            grb_2_vals_f = grb_2_vals_k.to('degF')

            grb_3_vals_k = units('kelvin') * grb_3_vals
            grb_3_vals_f = grb_3_vals_k.to('degF')

            grb_4_vals_k = units('kelvin') * grb_4_vals
            grb_4_vals_f = grb_4_vals_k.to('degF')

            grb_5_vals_k = units('kelvin') * grb_5_vals
            grb_5_vals_f = grb_5_vals_k.to('degF')            
                    
            return grb_1_vals_f, grb_2_vals_f, grb_3_vals_f, grb_4_vals_f, grb_5_vals_f
    
    
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


    def get_maximum_temperature_color_scale(directory_name):

        r'''
        THIS FUNCTION CREATES THE COLORSCALE FOR THE MAXIMUM TEMPERATURE FORECAST FOR EACH REGION OF THE CONUS FOR BOTH THE WARM AND COLD/COOL SEASON. EACH COLORSCALE IS REFLECTIVE OF EACH REGION SINCE A BROAD COLORSCALE WOULDN'T WORK SINCE FOR EXAMPLE A COLORSCALE FOR SOUTHERN CALIFORNIA WON'T BE VERY REPRESENTATIVE FOR PLOTTING TEMPERATURES IN THE NORTHEAST. THESE FUNCTIONS ALLOW THE CHANGING OF THE COLORSCALE BETWEEN REGIONS AND SEASONS SO USERS WON'T NEED TO WORRY ABOUT IT. 

        (C) METEOROLOGIST ERIC J. DREWITZ 2023

        '''

        dirName = directory_name
        
        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/':
            temp_scale_warm = np.arange(50, 135, 5)
            temp_scale_cool = np.arange(10, 105, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/':
            temp_scale_warm = np.arange(40, 125, 5)
            temp_scale_cool = np.arange(-10, 85, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/':
            temp_scale_warm = np.arange(40, 125, 5)
            temp_scale_cool = np.arange(-30, 75, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/':
            temp_scale_warm = np.arange(45, 135, 5)
            temp_scale_cool = np.arange(-20, 95, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/':
            temp_scale_warm = np.arange(60, 125, 5)
            temp_scale_cool = np.arange(0, 85, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/':
            temp_scale_warm = np.arange(30, 115, 5)
            temp_scale_cool = np.arange(-20, 75, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/':
            temp_scale_warm = np.arange(30, 135, 5)
            temp_scale_cool = np.arange(-30, 105, 5)

        return temp_scale_warm, temp_scale_cool


    def get_minimum_temperature_color_scale(directory_name):

        r'''
        THIS FUNCTION CREATES THE COLORSCALE FOR THE MINIMUM TEMPERATURE FORECAST FOR EACH REGION OF THE CONUS FOR BOTH THE WARM AND COLD/COOL SEASON. EACH COLORSCALE IS REFLECTIVE OF EACH REGION SINCE A BROAD COLORSCALE WOULDN'T WORK SINCE FOR EXAMPLE A COLORSCALE FOR SOUTHERN CALIFORNIA WON'T BE VERY REPRESENTATIVE FOR PLOTTING TEMPERATURES IN THE NORTHEAST. THESE FUNCTIONS ALLOW THE CHANGING OF THE COLORSCALE BETWEEN REGIONS AND SEASONS SO USERS WON'T NEED TO WORRY ABOUT IT. 

        (C) METEOROLOGIST ERIC J. DREWITZ 2023

        '''

        dirName = directory_name
        
        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/':
            temp_scale_warm = np.arange(30, 105, 5)
            temp_scale_cool = np.arange(-10, 75, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/':
            temp_scale_warm = np.arange(20, 95, 5)
            temp_scale_cool = np.arange(-20, 65, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/':
            temp_scale_warm = np.arange(20, 85, 5)
            temp_scale_cool = np.arange(-30, 65, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/':
            temp_scale_warm = np.arange(30, 95, 5)
            temp_scale_cool = np.arange(-20, 65, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/':
            temp_scale_warm = np.arange(50, 95, 5)
            temp_scale_cool = np.arange(-10, 75, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/':
            temp_scale_warm = np.arange(30, 85, 5)
            temp_scale_cool = np.arange(-30, 65, 5)

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/':
            temp_scale_warm = np.arange(20, 105, 5)
            temp_scale_cool = np.arange(-30, 75, 5)

        return temp_scale_warm, temp_scale_cool


    def get_extreme_heat_color_scale(directory_name):

        r'''
        THIS FUNCTION CREATES THE COLORSCALE FOR THE EXTREME HEAT FORECAST FOR EACH REGION OF THE CONUS FOR BOTH THE WARM AND COLD/COOL SEASON. EACH COLORSCALE IS REFLECTIVE OF EACH REGION SINCE A BROAD COLORSCALE WOULDN'T WORK SINCE FOR EXAMPLE A COLORSCALE FOR SOUTHERN CALIFORNIA WON'T BE VERY REPRESENTATIVE FOR PLOTTING TEMPERATURES IN THE NORTHEAST. THESE FUNCTIONS ALLOW THE CHANGING OF THE COLORSCALE BETWEEN REGIONS AND SEASONS SO USERS WON'T NEED TO WORRY ABOUT IT. 

        (C) METEOROLOGIST ERIC J. DREWITZ 2023

        '''

        dirName = directory_name
        
        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/':
            temp_scale_warm = np.arange(120, 140, 1)
            temp_scale_cool = np.arange(100, 125, 1)
            title_warm = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 120 \N{DEGREE SIGN}F)"
            title_cool = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)"

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/':
            temp_scale_warm = np.arange(100, 125, 1)
            temp_scale_cool = np.arange(85, 115, 1)
            title_warm = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)"
            title_cool = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 85 \N{DEGREE SIGN}F)"

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/':
            temp_scale_warm = np.arange(95, 125, 1)
            temp_scale_cool = np.arange(85, 115, 1)
            title_warm = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 95 \N{DEGREE SIGN}F)"
            title_cool = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 85 \N{DEGREE SIGN}F)"

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/':
            temp_scale_warm = np.arange(95, 125, 1)
            temp_scale_cool = np.arange(85, 115, 1)
            title_warm = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 95 \N{DEGREE SIGN}F)"
            title_cool = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 85 \N{DEGREE SIGN}F)"           

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/':
            temp_scale_warm = np.arange(100, 130, 1)
            temp_scale_cool = np.arange(85, 115, 1)
            title_warm = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 100 \N{DEGREE SIGN}F)"
            title_cool = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 85 \N{DEGREE SIGN}F)"

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/' or dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/':
            temp_scale_warm = np.arange(90, 115, 1)
            temp_scale_cool = np.arange(75, 105, 1)
            title_warm = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 90 \N{DEGREE SIGN}F)"
            title_cool = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 75 \N{DEGREE SIGN}F)"

        if dirName == '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/':
            temp_scale_warm = np.arange(95, 140, 1)
            temp_scale_cool = np.arange(85, 125, 1)
            title_warm = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 95 \N{DEGREE SIGN}F)"
            title_cool = "National Weather Service Short-Term Forecast\nExtreme Heat (Maximum Temperature >= 85 \N{DEGREE SIGN}F)"

        return temp_scale_warm, temp_scale_cool, title_warm, title_cool
    
    
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
    
    def sort_GRIB_files(GRIB_File_List, parameter):
        
        r'''
        THIS FUNCTION SORTS AND RETURNS THE INDIVIDUAL GRIB FILES IN THE DOWNLOADED DATASET. 
    
        THIS FUNCTION ALSO RETURNS THE COUNT OF THE NUMBER OF GRIB FILES IN THE DATASET.
    
        THIS FUNCTION IS TO BE USED IN THE PROGRAMMER'S CODE AFTER THE get_NWS_NDFD_grid_data(directory_name, parameter) FUNCTION IS USED
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
        count = 0
        for grb in GRIB_File_List:
            count = count + 1
        if count == 1:
            grb_1 = GRIB_File_List[1]
            grb_2 = None
            grb_3 = None
            grb_4 = None
            grb_5 = None
        
        if count == 2:
            grb_1 = GRIB_File_List[1]
            grb_2 = GRIB_File_List[2]
            grb_3 = None
            grb_4 = None
            grb_5 = None
            
        if count == 3: 
            grb_1 = GRIB_File_List[1]
            grb_2 = GRIB_File_List[2]
            grb_3 = GRIB_File_List[3]
            grb_4 = None
            grb_5 = None
        
        if count == 4: 
            grb_1 = GRIB_File_List[1]
            grb_2 = GRIB_File_List[2]
            grb_3 = GRIB_File_List[3]
            grb_4 = GRIB_File_List[4]
            grb_5 = None
    
        if count == 5: 
            grb_1 = GRIB_File_List[1]
            grb_2 = GRIB_File_List[2]
            grb_3 = GRIB_File_List[3]
            grb_4 = GRIB_File_List[4]
            grb_5 = GRIB_File_List[5]

    
        print("There are " + str(count) + " GRIB files in the " + parameter + " download.")
        return grb_1, grb_2, grb_3, grb_4, grb_5, count


    def sort_extended_GRIB_files(GRIB_File_List, parameter):
        
        r'''
        THIS FUNCTION SORTS AND RETURNS THE INDIVIDUAL GRIB FILES IN THE DOWNLOADED DATASET. 
    
        THIS FUNCTION ALSO RETURNS THE COUNT OF THE NUMBER OF GRIB FILES IN THE DATASET.
    
        THIS FUNCTION IS TO BE USED IN THE PROGRAMMER'S CODE AFTER THE get_NWS_NDFD_grid_data(directory_name, parameter) FUNCTION IS USED
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
        count = 0
        for grb in GRIB_File_List:
            count = count + 1
        if count == 1:
            grb_1 = GRIB_File_List[1]
            grb_2 = None
            grb_3 = None
            grb_4 = None
            grb_5 = None
            grb_6 = None
        
        if count == 2:
            grb_1 = GRIB_File_List[1]
            grb_2 = GRIB_File_List[2]
            grb_3 = None
            grb_4 = None
            grb_5 = None
            grb_6 = None
            
        if count == 3: 
            grb_1 = GRIB_File_List[1]
            grb_2 = GRIB_File_List[2]
            grb_3 = GRIB_File_List[3]
            grb_4 = None
            grb_5 = None
            grb_6 = None
        
        if count == 4: 
            grb_1 = GRIB_File_List[1]
            grb_2 = GRIB_File_List[2]
            grb_3 = GRIB_File_List[3]
            grb_4 = GRIB_File_List[4]
            grb_5 = None
            grb_6 = None
    
        if count == 5: 
            grb_1 = GRIB_File_List[1]
            grb_2 = GRIB_File_List[2]
            grb_3 = GRIB_File_List[3]
            grb_4 = GRIB_File_List[4]
            grb_5 = GRIB_File_List[5]
            grb_6 = None

        if count >= 6: 
            grb_1 = GRIB_File_List[1]
            grb_2 = GRIB_File_List[2]
            grb_3 = GRIB_File_List[3]
            grb_4 = GRIB_File_List[4]
            grb_5 = GRIB_File_List[5]
            grb_6 = GRIB_File_List[6]

    
        print("There are " + str(count) + " GRIB files in the " + parameter + " download.")
        return grb_1, grb_2, grb_3, grb_4, grb_5, grb_6, count
    
    
    def parse_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files, grid_time_interval, parameter):
    
        r'''
        THIS FUNCTION PARSES THROUGH EACH GRIB FILE AND RETURNS THE VALUES OF THE FILE, THE START AND END TIME FOR THE FORECAST VALIDITY, THE LATITUDE AND LONGITUDE COORDINATES CORRESPONDING TO THE VALUES IN THE FILE. 
    
        (C) METEOROLOGIST ERIC J. DREWITZ 2023
    
        '''
    
        
        files = count_of_GRIB_files
        param = parameter

        grid_time_interval = grid_time_interval
    
        if param == 'ds.mint.bin' or param == 'ds.maxt.bin':
            
            grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals = NDFD.GRIB_temperature_conversion_test1(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, count_of_GRIB_files)
            if files == 1:
                grb_1_start = first_GRIB_file.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_start = None
                grb_2_end = None
                grb_3_start = None
                grb_3_end = None
                grb_4_start = None
                grb_4_end = None
                grb_5_start = None
                grb_5_end = None
                          
                lats_1, lons_1 = first_GRIB_file.latlons()
                lats_2, lons_2 = None, None
                lats_3, lons_3 = None, None
                lats_4, lons_4 = None, None
                lats_5, lons_5 = None, None
        
            if files == 2:
                grb_1_start = first_GRIB_file.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_start = second_GRIB_file.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_start = None
                grb_3_end = None
                grb_4_start = None
                grb_4_end = None
                grb_5_start = None
                grb_5_end = None
                          
                lats_1, lons_1 = first_GRIB_file.latlons()
                lats_2, lons_2 = second_GRIB_file.latlons()
                lats_3, lons_3 = None, None
                lats_4, lons_4 = None, None
                lats_5, lons_5 = None, None
        
            if files == 3:
                grb_1_start = first_GRIB_file.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_start = second_GRIB_file.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_start = third_GRIB_file.validDate
                grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                grb_4_start = None
                grb_4_end = None
                grb_5_start = None
                grb_5_end = None
                          
                lats_1, lons_1 = first_GRIB_file.latlons()
                lats_2, lons_2 = second_GRIB_file.latlons()
                lats_3, lons_3 = third_GRIB_file.latlons()
                lats_4, lons_4 = None, None
                lats_5, lons_5 = None, None
        
            if files == 4:
                grb_1_start = first_GRIB_file.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_start = second_GRIB_file.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_start = third_GRIB_file.validDate
                grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                grb_4_start = fourth_GRIB_file.validDate
                grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                grb_5_start = None
                grb_5_end = None
                          
                lats_1, lons_1 = first_GRIB_file.latlons()
                lats_2, lons_2 = second_GRIB_file.latlons()
                lats_3, lons_3 = third_GRIB_file.latlons()
                lats_4, lons_4 = fourth_GRIB_file.latlons()
                lats_5, lons_5 = None, None
            
            
            if files >= 5:
                grb_1_start = first_GRIB_file.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_start = second_GRIB_file.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_start = third_GRIB_file.validDate
                grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                grb_4_start = fourth_GRIB_file.validDate
                grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                grb_5_start = fifth_GRIB_file.validDate
                grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                          
                lats_1, lons_1 = first_GRIB_file.latlons()
                lats_2, lons_2 = second_GRIB_file.latlons()
                lats_3, lons_3 = third_GRIB_file.latlons()
                lats_4, lons_4 = fourth_GRIB_file.latlons()
                lats_5, lons_5 = fifth_GRIB_file.latlons()
        
        else:       
       
            if files == 1:
                grb_1_vals = first_GRIB_file.values
                grb_1_start = first_GRIB_file.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_vals = None
                grb_2_start = None
                grb_2_end = None
                grb_3_vals = None
                grb_3_start = None
                grb_3_end = None
                grb_4_vals = None
                grb_4_start = None
                grb_4_end = None
                grb_5_vals = None
                grb_5_start = None
                grb_5_end = None
                          
                lats_1, lons_1 = first_GRIB_file.latlons()
                lats_2, lons_2 = None, None
                lats_3, lons_3 = None, None
                lats_4, lons_4 = None, None
                lats_5, lons_5 = None, None
        
            if files == 2:
                grb_1_vals = first_GRIB_file.values
                grb_1_start = first_GRIB_file.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_vals = second_GRIB_file.values
                grb_2_start = second_GRIB_file.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_vals = None
                grb_3_start = None
                grb_3_end = None
                grb_4_vals = None
                grb_4_start = None
                grb_4_end = None
                grb_5_vals = None
                grb_5_start = None
                grb_5_end = None
                          
                lats_1, lons_1 = first_GRIB_file.latlons()
                lats_2, lons_2 = second_GRIB_file.latlons()
                lats_3, lons_3 = None, None
                lats_4, lons_4 = None, None
                lats_5, lons_5 = None, None
        
            if files == 3:
                grb_1_vals = first_GRIB_file.values
                grb_1_start = first_GRIB_file.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_vals = second_GRIB_file.values
                grb_2_start = second_GRIB_file.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_vals = third_GRIB_file.values
                grb_3_start = third_GRIB_file.validDate
                grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                grb_4_vals = None
                grb_4_start = None
                grb_4_end = None
                grb_5_vals = None
                grb_5_start = None
                grb_5_end = None
                          
                lats_1, lons_1 = first_GRIB_file.latlons()
                lats_2, lons_2 = second_GRIB_file.latlons()
                lats_3, lons_3 = third_GRIB_file.latlons()
                lats_4, lons_4 = None, None
                lats_5, lons_5 = None, None
        
            if files == 4:
                grb_1_vals = first_GRIB_file.values
                grb_1_start = first_GRIB_file.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_vals = second_GRIB_file.values
                grb_2_start = second_GRIB_file.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_vals = third_GRIB_file.values
                grb_3_start = third_GRIB_file.validDate
                grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                grb_4_vals = fourth_GRIB_file.values
                grb_4_start = fourth_GRIB_file.validDate
                grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                grb_5_vals = None
                grb_5_start = None
                grb_5_end = None
                          
                lats_1, lons_1 = first_GRIB_file.latlons()
                lats_2, lons_2 = second_GRIB_file.latlons()
                lats_3, lons_3 = third_GRIB_file.latlons()
                lats_4, lons_4 = fourth_GRIB_file.latlons()
                lats_5, lons_5 = None, None
            
            
            if files >= 5:
                grb_1_vals = first_GRIB_file.values
                grb_1_start = first_GRIB_file.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_vals = second_GRIB_file.values
                grb_2_start = second_GRIB_file.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_vals = third_GRIB_file.values
                grb_3_start = third_GRIB_file.validDate
                grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                grb_4_vals = fourth_GRIB_file.values
                grb_4_start = fourth_GRIB_file.validDate
                grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                grb_5_vals = fifth_GRIB_file.values
                grb_5_start = fifth_GRIB_file.validDate
                grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                          
                lats_1, lons_1 = first_GRIB_file.latlons()
                lats_2, lons_2 = second_GRIB_file.latlons()
                lats_3, lons_3 = third_GRIB_file.latlons()
                lats_4, lons_4 = fourth_GRIB_file.latlons()
                lats_5, lons_5 = fifth_GRIB_file.latlons()
    
    
        return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5


    def parse_extended_SPC_GRIB_files(first_GRIB_file, second_GRIB_file, third_GRIB_file, fourth_GRIB_file, fifth_GRIB_file, sixth_GRIB_file, count_of_GRIB_files, grid_time_interval, parameter):
    
        r'''
        THIS FUNCTION PARSES THROUGH EACH GRIB FILE AND RETURNS THE VALUES OF THE FILE, THE START AND END TIME FOR THE FORECAST VALIDITY, THE LATITUDE AND LONGITUDE COORDINATES CORRESPONDING TO THE VALUES IN THE FILE. 
    
        (C) METEOROLOGIST ERIC J. DREWITZ 2023
    
        '''
    
        
        files = count_of_GRIB_files
        param = parameter

        if files == 1:
            grb_1_vals = first_GRIB_file.values
            grb_1_start = first_GRIB_file.validDate
            grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
            grb_2_vals = None
            grb_2_start = None
            grb_2_end = None
            grb_3_vals = None
            grb_3_start = None
            grb_3_end = None
            grb_4_vals = None
            grb_4_start = None
            grb_4_end = None
            grb_5_vals = None
            grb_5_start = None
            grb_5_end = None
            grb_6_vals = None
            grb_6_start = None
            grb_6_end = None
                      
            lats_1, lons_1 = first_GRIB_file.latlons()
            lats_2, lons_2 = None, None
            lats_3, lons_3 = None, None
            lats_4, lons_4 = None, None
            lats_5, lons_5 = None, None
            lats_6, lons_6 = None, None
    
        if files == 2:
            grb_1_vals = first_GRIB_file.values
            grb_1_start = first_GRIB_file.validDate
            grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
            grb_2_vals = second_GRIB_file.values
            grb_2_start = second_GRIB_file.validDate
            grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
            grb_3_vals = None
            grb_3_start = None
            grb_3_end = None
            grb_4_vals = None
            grb_4_start = None
            grb_4_end = None
            grb_5_vals = None
            grb_5_start = None
            grb_5_end = None
            grb_6_vals = None
            grb_6_start = None
            grb_6_end = None
                      
            lats_1, lons_1 = first_GRIB_file.latlons()
            lats_2, lons_2 = second_GRIB_file.latlons()
            lats_3, lons_3 = None, None
            lats_4, lons_4 = None, None
            lats_5, lons_5 = None, None
            lats_6, lons_6 = None, None
    
        if files == 3:
            grb_1_vals = first_GRIB_file.values
            grb_1_start = first_GRIB_file.validDate
            grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
            grb_2_vals = second_GRIB_file.values
            grb_2_start = second_GRIB_file.validDate
            grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
            grb_3_vals = third_GRIB_file.values
            grb_3_start = third_GRIB_file.validDate
            grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
            grb_4_vals = None
            grb_4_start = None
            grb_4_end = None
            grb_5_vals = None
            grb_5_start = None
            grb_5_end = None
            grb_6_vals = None
            grb_6_start = None
            grb_6_end = None
                      
            lats_1, lons_1 = first_GRIB_file.latlons()
            lats_2, lons_2 = second_GRIB_file.latlons()
            lats_3, lons_3 = third_GRIB_file.latlons()
            lats_4, lons_4 = None, None
            lats_5, lons_5 = None, None
            lats_6, lons_6 = None, None
    
        if files == 4:
            grb_1_vals = first_GRIB_file.values
            grb_1_start = first_GRIB_file.validDate
            grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
            grb_2_vals = second_GRIB_file.values
            grb_2_start = second_GRIB_file.validDate
            grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
            grb_3_vals = third_GRIB_file.values
            grb_3_start = third_GRIB_file.validDate
            grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
            grb_4_vals = fourth_GRIB_file.values
            grb_4_start = fourth_GRIB_file.validDate
            grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
            grb_5_vals = None
            grb_5_start = None
            grb_5_end = None
            grb_6_vals = None
            grb_6_start = None
            grb_6_end = None
                      
            lats_1, lons_1 = first_GRIB_file.latlons()
            lats_2, lons_2 = second_GRIB_file.latlons()
            lats_3, lons_3 = third_GRIB_file.latlons()
            lats_4, lons_4 = fourth_GRIB_file.latlons()
            lats_5, lons_5 = None, None
            lats_6, lons_6 = None, None
        
        
        if files == 5:
            grb_1_vals = first_GRIB_file.values
            grb_1_start = first_GRIB_file.validDate
            grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
            grb_2_vals = second_GRIB_file.values
            grb_2_start = second_GRIB_file.validDate
            grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
            grb_3_vals = third_GRIB_file.values
            grb_3_start = third_GRIB_file.validDate
            grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
            grb_4_vals = fourth_GRIB_file.values
            grb_4_start = fourth_GRIB_file.validDate
            grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
            grb_5_vals = fifth_GRIB_file.values
            grb_5_start = fifth_GRIB_file.validDate
            grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
            grb_6_vals = None
            grb_6_start = None
            grb_6_end = None
                      
            lats_1, lons_1 = first_GRIB_file.latlons()
            lats_2, lons_2 = second_GRIB_file.latlons()
            lats_3, lons_3 = third_GRIB_file.latlons()
            lats_4, lons_4 = fourth_GRIB_file.latlons()
            lats_5, lons_5 = fifth_GRIB_file.latlons()
            lats_6, lons_6 = None, None

        if files >= 6:
            grb_1_vals = first_GRIB_file.values
            grb_1_start = first_GRIB_file.validDate
            grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
            grb_2_vals = second_GRIB_file.values
            grb_2_start = second_GRIB_file.validDate
            grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
            grb_3_vals = third_GRIB_file.values
            grb_3_start = third_GRIB_file.validDate
            grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
            grb_4_vals = fourth_GRIB_file.values
            grb_4_start = fourth_GRIB_file.validDate
            grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
            grb_5_vals = fifth_GRIB_file.values
            grb_5_start = fifth_GRIB_file.validDate
            grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
            grb_6_vals = sixth_GRIB_file.values
            grb_6_start = sixth_GRIB_file.validDate
            grb_6_end = grb_6_start + timedelta(hours=grid_time_interval)
                      
            lats_1, lons_1 = first_GRIB_file.latlons()
            lats_2, lons_2 = second_GRIB_file.latlons()
            lats_3, lons_3 = third_GRIB_file.latlons()
            lats_4, lons_4 = fourth_GRIB_file.latlons()
            lats_5, lons_5 = fifth_GRIB_file.latlons()
            lats_6, lons_6 = sixth_GRIB_file.latlons()
    
        return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6
    
    def GRIB_file_checker(GRIB_File_List):
        
        r'''
        THIS FUNCTION IS USEFUL WHEN HAVING AUTOMATED DISPLAYS OF THE VARIOUS GRIB FILE DATA
    
        THIS FUNCTION CHECKS TO SEE HOW MANY GRIB FILES ARE RETURNED IN THE LIST WHICH IS HELPFUL FOR GRAPHICS
    
        THIS FUNCTION IS TO BE USED IN THE PROGRAMMER'S CODE AFTER THE get_NWS_NDFD_grid_data(directory_name, parameter) FUNCTION IS USED
    
        THIS FUNCTION WILL RETURN A BOOLEAN VALUE FOR IF OR IF NOT THE FILE EXISTS
    
        USUALLY THERE ARE NOT MORE THAN 5 GRIB FILES IN A DOWNLOAD AT A TIME
    
        IF THE GRIB FILE EXISTS, A BOOLEAN VALUE OF TRUE IS RETURNED AND IF THE GRIB FILE DOESN'T EXIST A BOOLEAN VALUE OF FALSE IS RETURNED. 
    
        THE LOGICAL CHECKS HELPS WHEN THE USER IS MAKING AUTOMATED GRAPHICS TO MAKE SURE THE NUMBER OF SUBPLOTS IS EQUAL TO THE NUMBER OF GRIB FILES
    
        THIS FUNCTION ALSO RETURNS THE COUNT OF THE NUMBER OF GRIB FILES IN THE DATASET.
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
        count = 0
        for grb in GRIB_File_List:
            count = count + 1
        if count == 1:
            grb_1_logic = True
            grb_2_logic = False
            grb_3_logic = False
            grb_4_logic = False
            grb_5_logic = False
        
        if count == 2:
            grb_1_logic = True
            grb_2_logic = True
            grb_3_logic = False
            grb_4_logic = False
            grb_5_logic = False
            
        if count == 3: 
            grb_1_logic = True
            grb_2_logic = True
            grb_3_logic = True
            grb_4_logic = False
            grb_5_logic = False
        
        if count == 4: 
            grb_1_logic = True
            grb_2_logic = True
            grb_3_logic = True
            grb_4_logic = True
            grb_5_logic = False
    
        if count >= 5: 
            grb_1_logic = True
            grb_2_logic = True
            grb_3_logic = True
            grb_4_logic = True
            grb_5_logic = True
    
        return grb_1_logic, grb_2_logic, grb_3_logic, grb_4_logic, grb_5_logic, count
    
    
    
    def get_GRIB_file_values(GRIB_File):
     
        r'''
        THIS FUNCTION RETURNS THE VALUES OF THE DATA INSIDE OF A GRIB FILE. 
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
        return GRIB_File.values
    
    
    def get_GRIB_file_valid_date(GRIB_File):
    
        r'''
        THIS FUNCTION RETURNS THE VALID DATE FOR A GRIB FILE
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
        return GRIB_File.validDate
    
    
    def NDFD_Forecast_Time_Interval(GRIB_File, hours): 
       
        r'''
        THIS FUNCTION WILL RETURN THE TIME THE FORECAST PERIOD ENDS BASED ON HOW LONG THE FORECAST PERIOD IS VALID FOR
        THE VALID DATE FOR A GRIB FILE CORRESPONDS TO THE START OF THE FORECAST PERIOD. 
        (I.E. THE NDFD MAXIMUM RELATIVE HUMIDITY GRIDS ARE A TIME LENGTH OF 12HRS, THEREFORE THE ENDING TIME OF THE FORECAST PERIOD IS 12HRS AFTER THE VALID DATE OF THE GRIB FILE. 
    
        PYTHON MODULE DEPENDENCIES:
        1. DATETIME
    
        COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
        '''
    
        return GRIB_File.validDate + timedelta(hours=hours)

class checks:

    r'''

    THIS CLASS HOSTS FUNCTIONS TO CHECK TO MAKE SURE WE ARE COMPARING DATASETS FOR THE SAME TIME

    '''

    def wind_direction_number_to_abbreviation(wind_direction):

        r'''
        This function takes the numerical wind direction and assigns an abbreviation (i.e. N vs. NW) to the value

        Inputs:
                1) wind_direction (Integer or Float)

        Returns:
                1) wind_direction (String)

        '''
        wind_direction = wind_direction
        
        if wind_direction >= 358 or wind_direction <= 2:
            wind_dir = 'N'
        if wind_direction > 2 and wind_direction <= 30:
            wind_dir = 'NNE'
        if wind_direction > 30 and wind_direction <= 60:
            wind_dir = 'NE'
        if wind_direction > 60 and wind_direction < 88:
            wind_dir = 'ENE'
        if wind_direction >= 88 and wind_direction <= 92:
            wind_dir = 'E'
        if wind_direction > 92 and wind_direction <= 120:
            wind_dir = 'ESE'
        if wind_direction > 120 and wind_direction <= 150:
            wind_dir = 'SE'
        if wind_direction > 150 and wind_direction < 178:
            wind_dir = 'SSE'
        if wind_direction >= 178 and wind_direction <= 182:
            wind_dir = 'S'
        if wind_direction > 182 and wind_direction <= 210:
            wind_dir = 'SSW'
        if wind_direction > 210 and wind_direction <= 240:
            wind_dir = 'SW'
        if wind_direction > 240 and wind_direction < 268:
            wind_dir = 'WSW'
        if wind_direction >= 268 and wind_direction <= 272:
            wind_dir = 'W'
        if wind_direction > 272 and wind_direction <= 300:
            wind_dir = 'WNW'
        if wind_direction > 300 and wind_direction <= 330:
            wind_dir = 'NW'
        if wind_direction > 330 and wind_direction < 358:
            wind_dir = 'NNW'

        return wind_dir
    

    def check_RTMA_vs_METAR_Times(real_time_mesoscale_analysis_time, metar_observation_time):

        r'''
        THIS FUNCTION MAKES SURE THE TIMES MATCH BETWEEN THE RTMA DATA AND METAR DATA. A LOT OF TIMES, THE METAR DATA IS 1-2 HOURS AHEAD OF THE RTMA DATA. THE FUNCTION RETURNS THE TIME OF THE LATEST RTMA DATASET TO USE AS THE TIME WHEN QUERYING THE METAR DATASETS

        (C) METEOROLOGIST ERIC J. DREWITZ

        '''

        metar_time = metar_observation_time

        rtma_time = real_time_mesoscale_analysis_time

        time_diff = metar_time.hour - rtma_time.hour

        if metar_time.hour > rtma_time.hour:
            new_metar_time = metar_time - timedelta(hours=time_diff)

        if metar_time.hour < rtma_time.hour:
            hour = rtma_time.hour
            new_metar_time = metar_time - timedelta(days=1)
            year = new_metar_time.year
            month = new_metar_time.month
            day = new_metar_time.day
            new_metar_time = datetime(year, month, day, hour)

        else:
            new_metar_time = rtma_time
            

        return new_metar_time


    def check_RTMA_vs_METAR_Times_Alaska(real_time_mesoscale_analysis_time, metar_observation_time):

        r'''
        THIS FUNCTION MAKES SURE THE TIMES MATCH BETWEEN THE RTMA DATA AND METAR DATA. A LOT OF TIMES, THE METAR DATA IS 1-2 HOURS AHEAD OF THE RTMA DATA. THE FUNCTION RETURNS THE TIME OF THE LATEST RTMA DATASET TO USE AS THE TIME WHEN QUERYING THE METAR DATASETS

        (C) METEOROLOGIST ERIC J. DREWITZ

        '''

        metar_time = metar_observation_time

        rtma_time = real_time_mesoscale_analysis_time

        time_diff = metar_time.hour - rtma_time.hour

        minute = 55

        if metar_time.hour > rtma_time.hour:
            new_metar_time = metar_time - timedelta(hours=2)
            new_metar_time1 = datetime(new_metar_time.year, new_metar_time.month, new_metar_time.day, new_metar_time.hour, minute)

        if metar_time.hour < rtma_time.hour:
            hour = rtma_time.hour
            new_metar_time = metar_time - timedelta(days=1)
            year = new_metar_time.year
            month = new_metar_time.month
            day = new_metar_time.day
            new_metar_time1 = datetime(year, month, day, hour, minute)

        else:
            new_metar_time = metar_time - timedelta(hours=1)
            new_metar_time1 = datetime(new_metar_time.year, new_metar_time.month, new_metar_time.day, new_metar_time.hour, minute)

        return new_metar_time1

class save:

    r'''
    This class hosts the function that parses through a figure list and saves the figures to a specified file location

    '''
        
    def extract_NWS_NDFD_figures(figure_list, file_count, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5):

        r'''
        This function extracts indivdual figures from a list of figures and saves them with a specified file path. 
        *This function is only to be used for the National Weather Service NDFD graphics.* 

        Inputs: 1) figure_list (List) - List of figures returned by the plotting function. 
                2) file_count (Integer) - Count of files returned by the plotting function. 
                3) file_path_1 (String) - Path to where the first figure is saved. 
                4) file_path_2 (String) - Path to where the second figure is saved. 
                5) file_path_3 (String) - Path to where the third figure is saved. 
                6) file_path_4 (String) - Path to where the fourth figure is saved. 
                7) file_path_5 (String) - Path to where the fifth figure is saved. 

        Return: Each figure in the list is saved as its own file to a specified file path

        '''
        
        if file_count == 1:
            fig1 = figure_list[0]
            fig1 = fig1.savefig(file_path_1)
            plt.close(fig1)
        if file_count == 2:
            fig1 = figure_list[0]
            fig2 = figure_list[1]
            fig1 = fig1.savefig(file_path_1)
            plt.close(fig1)
            fig2 = fig2.savefig(file_path_2)
            plt.close(fig2)
        if file_count == 3:
            fig1 = figure_list[0]
            fig2 = figure_list[1]
            fig3 = figure_list[2]
            fig1 = fig1.savefig(file_path_1)
            plt.close(fig1)
            fig2 = fig2.savefig(file_path_2)
            plt.close(fig2)
            fig3 = fig3.savefig(file_path_3)
            plt.close(fig3)
        if file_count == 4:
            fig1 = figure_list[0]
            fig2 = figure_list[1]
            fig3 = figure_list[2]
            fig4 = figure_list[3]
            fig1 = fig1.savefig(file_path_1)
            plt.close(fig1)
            fig2 = fig2.savefig(file_path_2)
            plt.close(fig2)
            fig3 = fig3.savefig(file_path_3)
            plt.close(fig3)
            fig4 = fig4.savefig(file_path_4)
            plt.close(fig4)
        if file_count == 5:
            fig1 = figure_list[0]
            fig2 = figure_list[1]
            fig3 = figure_list[2]
            fig4 = figure_list[3]
            fig5 = figure_list[4]
            fig1 = fig1.savefig(file_path_1)
            plt.close(fig1)
            fig2 = fig2.savefig(file_path_2)
            plt.close(fig2)
            fig3 = fig3.savefig(file_path_3)
            plt.close(fig3)
            fig4 = fig4.savefig(file_path_4)
            plt.close(fig4)
            fig5 = fig5.savefig(file_path_5)
            plt.close(fig5)

    def extract_SPC_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7):

        r'''
        This function extracts indivdual figures from a list of figures and saves them with a specified file path. 
        *This function is only to be used for the SPC Fire Weather Outlook Graphics.* 

        Inputs: 1) figure_list (List) - List of figures returned by the plotting function. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.
                7) file_path_7 (String) - Path to where the seventh figure is saved.

        Return: Each figure in the list is saved as its own file to a specified file path

        '''
        try:
            fig1 = figure_list[0]
            fig1 = fig1.savefig(file_path_1)
            plt.close(fig1)
            fig2 = figure_list[1]
            fig2 = fig2.savefig(file_path_2)
            plt.close(fig2)
            fig3 = figure_list[2]
            fig3 = fig3.savefig(file_path_3)
            plt.close(fig3)
            fig4 = figure_list[3]
            fig4 = fig4.savefig(file_path_4)
            plt.close(fig4) 
            fig5 = figure_list[4]
            fig5 = fig5.savefig(file_path_5)
            plt.close(fig5) 
            fig6 = figure_list[5]
            fig6 = fig6.savefig(file_path_6)
            plt.close(fig6) 
            fig7 = figure_list[6]
            fig7 = fig7.savefig(file_path_7)
            plt.close(fig7) 
        except Exception as ee:
            try:
                fig1 = figure_list[0]
                fig1 = fig1.savefig(file_path_1)
                plt.close(fig1)
                fig2 = figure_list[1]
                fig2 = fig2.savefig(file_path_2)
                plt.close(fig2)
                fig3 = figure_list[2]
                fig3 = fig3.savefig(file_path_3)
                plt.close(fig3)
                fig4 = figure_list[3]
                fig4 = fig4.savefig(file_path_4)
                plt.close(fig4) 
                fig5 = figure_list[4]
                fig5 = fig5.savefig(file_path_5)
                plt.close(fig5) 
                fig6 = figure_list[5]
                fig6 = fig6.savefig(file_path_6)
                plt.close(fig6) 
    
            except Exception as a:
                try:
                    fig1 = figure_list[0]
                    fig1 = fig1.savefig(file_path_1)
                    plt.close(fig1)
                    fig2 = figure_list[1]
                    fig2 = fig2.savefig(file_path_2)
                    plt.close(fig2)
                    fig3 = figure_list[2]
                    fig3 = fig3.savefig(file_path_3)
                    plt.close(fig3)
                    fig4 = figure_list[3]
                    fig4 = fig4.savefig(file_path_4)
                    plt.close(fig4) 
                    fig5 = figure_list[4]
                    fig5 = fig5.savefig(file_path_5)
                    plt.close(fig5)
                except Exception as b:    
                    try:
                        fig1 = figure_list[0]
                        fig1 = fig1.savefig(file_path_1)
                        plt.close(fig1)
                        fig2 = figure_list[1]
                        fig2 = fig2.savefig(file_path_2)
                        plt.close(fig2)
                        fig3 = figure_list[2]
                        fig3 = fig3.savefig(file_path_3)
                        plt.close(fig3)
                        fig4 = figure_list[3]
                        fig4 = fig4.savefig(file_path_4)
                        plt.close(fig4)
                    
                    except Exception as c:
                        try:     
                            fig1 = figure_list[0]
                            fig1 = fig1.savefig(file_path_1)
                            plt.close(fig1)
                            fig2 = figure_list[1]
                            fig2 = fig2.savefig(file_path_2)
                            plt.close(fig2)
                            fig3 = figure_list[2]
                            fig3 = fig3.savefig(file_path_3)
                            plt.close(fig3)
                
                        except Exception as b:
                            try:
                                fig1 = figure_list[0]
                                fig1 = fig1.savefig(file_path_1)
                                plt.close(fig1)
                                fig2 = figure_list[1]
                                fig2 = fig2.savefig(file_path_2)
                                plt.close(fig2)
                
                            except Exception as c:
                                try:
                                    fig1 = figure_list[0]
                                    fig1 = fig1.savefig(file_path_1)
                                    plt.close(fig1)
                
                                except Exception as d:
                                    pass



    def make_SPC_Outlook_GIF(GIF_Image_file_path, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, file_path_8, fps):

        r'''
        This function makes an animated GIF images of the SPC Outlooks and saves the GIF to a specified location. 

        Inputs: 1) GIF_Image_file_path (String) - The path to where the GIF image saves to plus the filename of the GIF image. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.
                8) file_path_7 (String) - Path to where the seventh figure is saved.
                9) file_path_8 (String) - Path to where the eigth figure is saved.
                10) fps (Integer) - The rate in frames per second the GIF loops. 

        '''


        try:
            file_path_1 = file_path_1
            file_path_2 = file_path_2
            file_path_3 = file_path_3
            file_path_4 = file_path_4
            file_path_5 = file_path_5
            file_path_6 = file_path_6
            file_path_7 = file_path_7
            file_path_8 = file_path_8

            datetime_str_1 = time.ctime(os.path.getmtime(file_path_1))
            datetime_str_2 = time.ctime(os.path.getmtime(file_path_2))
            datetime_str_3 = time.ctime(os.path.getmtime(file_path_3))
            datetime_str_4 = time.ctime(os.path.getmtime(file_path_4))
            datetime_str_5 = time.ctime(os.path.getmtime(file_path_5))
            datetime_str_6 = time.ctime(os.path.getmtime(file_path_6))
            datetime_str_7 = time.ctime(os.path.getmtime(file_path_7))
            datetime_str_8 = time.ctime(os.path.getmtime(file_path_8))

            day_1 = datetime.strptime(datetime_str_1, '%a %b %d %H:%M:%S %Y')
            day_2 = datetime.strptime(datetime_str_2, '%a %b %d %H:%M:%S %Y')
            day_3 = datetime.strptime(datetime_str_3, '%a %b %d %H:%M:%S %Y')
            day_4 = datetime.strptime(datetime_str_4, '%a %b %d %H:%M:%S %Y')
            day_5 = datetime.strptime(datetime_str_5, '%a %b %d %H:%M:%S %Y')
            day_6 = datetime.strptime(datetime_str_6, '%a %b %d %H:%M:%S %Y')
            day_7 = datetime.strptime(datetime_str_7, '%a %b %d %H:%M:%S %Y')
            day_8 = datetime.strptime(datetime_str_8, '%a %b %d %H:%M:%S %Y')
        
            if day_7.day == day_8.day and day_7.hour == day_8.hour:
                filenames = []
                filenames.append(file_path_1)
                filenames.append(file_path_2)
                filenames.append(file_path_3)
                filenames.append(file_path_4)
                filenames.append(file_path_5)
                filenames.append(file_path_6)
                filenames.append(file_path_7)
                filenames.append(file_path_8)

            else:
                filenames = []
                filenames.append(file_path_1)
                filenames.append(file_path_2)
                filenames.append(file_path_3)
                filenames.append(file_path_4)
                filenames.append(file_path_5)
                filenames.append(file_path_6)
                filenames.append(file_path_7)  
            
            with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                for filename in filenames:
                    image = imageio.v2.imread(filename)
                    writer.append_data(image)
        
        except Exception as a:
            try:
                file_path_1 = file_path_1
                file_path_2 = file_path_2
                file_path_3 = file_path_3
                file_path_4 = file_path_4
                file_path_5 = file_path_5
                file_path_6 = file_path_6
                file_path_7 = file_path_7
                
    
                datetime_str_1 = time.ctime(os.path.getmtime(file_path_1))
                datetime_str_2 = time.ctime(os.path.getmtime(file_path_2))
                datetime_str_3 = time.ctime(os.path.getmtime(file_path_3))
                datetime_str_4 = time.ctime(os.path.getmtime(file_path_4))
                datetime_str_5 = time.ctime(os.path.getmtime(file_path_5))
                datetime_str_6 = time.ctime(os.path.getmtime(file_path_6))
                datetime_str_7 = time.ctime(os.path.getmtime(file_path_7))
    
                day_1 = datetime.strptime(datetime_str_1, '%a %b %d %H:%M:%S %Y')
                day_2 = datetime.strptime(datetime_str_2, '%a %b %d %H:%M:%S %Y')
                day_3 = datetime.strptime(datetime_str_3, '%a %b %d %H:%M:%S %Y')
                day_4 = datetime.strptime(datetime_str_4, '%a %b %d %H:%M:%S %Y')
                day_5 = datetime.strptime(datetime_str_5, '%a %b %d %H:%M:%S %Y')
                day_6 = datetime.strptime(datetime_str_6, '%a %b %d %H:%M:%S %Y')
                day_7 = datetime.strptime(datetime_str_7, '%a %b %d %H:%M:%S %Y')
            
                if day_6.day == day_7.day and day_6.hour == day_7.hour:
                    filenames = []
                    filenames.append(file_path_1)
                    filenames.append(file_path_2)
                    filenames.append(file_path_3)
                    filenames.append(file_path_4)
                    filenames.append(file_path_5)
                    filenames.append(file_path_6)
                    filenames.append(file_path_7)
    
                else:
                    filenames = []
                    filenames.append(file_path_1)
                    filenames.append(file_path_2)
                    filenames.append(file_path_3)
                    filenames.append(file_path_4)
                    filenames.append(file_path_5)
                    filenames.append(file_path_6)

                with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                    for filename in filenames:
                        image = imageio.v2.imread(filename)
                        writer.append_data(image)
        
            except Exception as b:

                file_path_1 = file_path_1
                file_path_2 = file_path_2
                file_path_3 = file_path_3
                file_path_4 = file_path_4
                file_path_5 = file_path_5
                file_path_6 = file_path_6
    
                datetime_str_1 = time.ctime(os.path.getmtime(file_path_1))
                datetime_str_2 = time.ctime(os.path.getmtime(file_path_2))
                datetime_str_3 = time.ctime(os.path.getmtime(file_path_3))
                datetime_str_4 = time.ctime(os.path.getmtime(file_path_4))
                datetime_str_5 = time.ctime(os.path.getmtime(file_path_5))
                datetime_str_6 = time.ctime(os.path.getmtime(file_path_6))
    
                day_1 = datetime.strptime(datetime_str_1, '%a %b %d %H:%M:%S %Y')
                day_2 = datetime.strptime(datetime_str_2, '%a %b %d %H:%M:%S %Y')
                day_3 = datetime.strptime(datetime_str_3, '%a %b %d %H:%M:%S %Y')
                day_4 = datetime.strptime(datetime_str_4, '%a %b %d %H:%M:%S %Y')
                day_5 = datetime.strptime(datetime_str_5, '%a %b %d %H:%M:%S %Y')
                day_6 = datetime.strptime(datetime_str_6, '%a %b %d %H:%M:%S %Y')
            
                if day_5.day == day_6.day and day_5.hour == day_6.hour:
                    filenames = []
                    filenames.append(file_path_1)
                    filenames.append(file_path_2)
                    filenames.append(file_path_3)
                    filenames.append(file_path_4)
                    filenames.append(file_path_5)
                    filenames.append(file_path_6)
              
                else:
                    filenames = []
                    filenames.append(file_path_1)
                    filenames.append(file_path_2)
                    filenames.append(file_path_3)
                    filenames.append(file_path_4)
                    filenames.append(file_path_5)
                
                with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                    for filename in filenames:
                        image = imageio.v2.imread(filename)
                        writer.append_data(image)        
        
        print("GIF Saved!")        
        
        
    def extract_RTMA_figures_6hr_timelapse(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7):

        r'''
        This function extracts indivdual figures from a list of figures and saves them with a specified file path. 
        *This function is only to be used for the SPC Fire Weather Outlook Graphics.* 

        Inputs: 1) figure_list (List) - List of figures returned by the plotting function. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.
                8) file_path_7 (String) - Path to where the seventh figure is saved.

        Return: Each figure in the list is saved as its own file to a specified file path

        '''
        try:
            fig1 = figure_list[0]
            fig1 = fig1.savefig(file_path_1)
            plt.close(fig1)
            fig2 = figure_list[1]
            fig2 = fig2.savefig(file_path_2)
            plt.close(fig2)
            fig3 = figure_list[2]
            fig3 = fig3.savefig(file_path_3)
            plt.close(fig3)
            fig4 = figure_list[3]
            fig4 = fig4.savefig(file_path_4)
            plt.close(fig4) 
            fig5 = figure_list[4]
            fig5 = fig5.savefig(file_path_5)
            plt.close(fig5) 
            fig6 = figure_list[5]
            fig6 = fig6.savefig(file_path_6)
            plt.close(fig6) 
            fig7 = figure_list[6]
            fig7 = fig7.savefig(file_path_7)
            plt.close(fig7)

        except Exception as a:
            try:
                fig1 = figure_list[0]
                fig1 = fig1.savefig(file_path_1)
                plt.close(fig1)
                fig2 = figure_list[1]
                fig2 = fig2.savefig(file_path_2)
                plt.close(fig2)
                fig3 = figure_list[2]
                fig3 = fig3.savefig(file_path_3)
                plt.close(fig3)
                fig4 = figure_list[3]
                fig4 = fig4.savefig(file_path_4)
                plt.close(fig4) 
                fig5 = figure_list[4]
                fig5 = fig5.savefig(file_path_5)
                plt.close(fig5) 
                fig6 = figure_list[5]
                fig6 = fig6.savefig(file_path_6)
                plt.close(fig6) 
    
            except Exception as b:
                try:
                    fig1 = figure_list[0]
                    fig1 = fig1.savefig(file_path_1)
                    plt.close(fig1)
                    fig2 = figure_list[1]
                    fig2 = fig2.savefig(file_path_2)
                    plt.close(fig2)
                    fig3 = figure_list[2]
                    fig3 = fig3.savefig(file_path_3)
                    plt.close(fig3)
                    fig4 = figure_list[3]
                    fig4 = fig4.savefig(file_path_4)
                    plt.close(fig4) 
                    fig5 = figure_list[4]
                    fig5 = fig5.savefig(file_path_5)
                    plt.close(fig5)
                except Exception as c:    
                    try:
                        fig1 = figure_list[0]
                        fig1 = fig1.savefig(file_path_1)
                        plt.close(fig1)
                        fig2 = figure_list[1]
                        fig2 = fig2.savefig(file_path_2)
                        plt.close(fig2)
                        fig3 = figure_list[2]
                        fig3 = fig3.savefig(file_path_3)
                        plt.close(fig3)
                        fig4 = figure_list[3]
                        fig4 = fig4.savefig(file_path_4)
                        plt.close(fig4)
                    
                    except Exception as d:
                        try:     
                            fig1 = figure_list[0]
                            fig1 = fig1.savefig(file_path_1)
                            plt.close(fig1)
                            fig2 = figure_list[1]
                            fig2 = fig2.savefig(file_path_2)
                            plt.close(fig2)
                            fig3 = figure_list[2]
                            fig3 = fig3.savefig(file_path_3)
                            plt.close(fig3)
                
                        except Exception as e:
                            try:
                                fig1 = figure_list[0]
                                fig1 = fig1.savefig(file_path_1)
                                plt.close(fig1)
                                fig2 = figure_list[1]
                                fig2 = fig2.savefig(file_path_2)
                                plt.close(fig2)
                
                            except Exception as f:
                                try:
                                    fig1 = figure_list[0]
                                    fig1 = fig1.savefig(file_path_1)
                                    plt.close(fig1)
                
                                except Exception as g:
                                    pass        


    def make_RTMA_6hr_timelapse_GIF(GIF_Image_file_path, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, fps):

        r'''
        This function makes an animated GIF images of the SPC Outlooks and saves the GIF to a specified location. 

        Inputs: 1) GIF_Image_file_path (String) - The path to where the GIF image saves to plus the filename of the GIF image. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.
                8) file_path_7 (String) - Path to where the seventh figure is saved.
                9) fps (Integer) - The rate in frames per second the GIF loops. 

        '''


        filenames = []
        filenames.append(file_path_1)
        filenames.append(file_path_2)
        filenames.append(file_path_3)
        filenames.append(file_path_4)
        filenames.append(file_path_5)
        filenames.append(file_path_6)
        filenames.append(file_path_7)


        try:
            with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                for filename in filenames:
                    image = imageio.v2.imread(filename)
                    writer.append_data(image)
        
        except Exception as a:
            try:
                with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                    new_list = []
                    image_1 = filenames[0]
                    image_2 = filenames[1]
                    image_3 = filenames[2]
                    image_4 = filenames[3]
                    image_5 = filenames[4]
                    image_6 = filenames[5]
                    image_7 = filenames[6]
                    new_list.append(image_1)
                    new_list.append(image_2)
                    new_list.append(image_3)
                    new_list.append(image_4)
                    new_list.append(image_5)
                    new_list.append(image_6)
                    new_list.append(image_7)
            
                    for filename in new_list:
                        image = imageio.v2.imread(filename)
                        writer.append_data(image)
                        
            
        
            except Exception as b:
                with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                    new_list = []
                    image_1 = filenames[0]
                    image_2 = filenames[1]
                    image_3 = filenames[2]
                    image_4 = filenames[3]
                    image_5 = filenames[4]
                    image_6 = filenames[5]
                    new_list.append(image_1)
                    new_list.append(image_2)
                    new_list.append(image_3)
                    new_list.append(image_4)
                    new_list.append(image_5)
                    new_list.append(image_6)
            
                    for filename in new_list:
                        image = imageio.v2.imread(filename)
                        writer.append_data(image)        
        
        print("GIF Saved!")   
            
