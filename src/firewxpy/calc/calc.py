"""
This file hosts functions used to perform various calculations of our weather data.

(C) Eric J. Drewitz 2024-2026
"""

import pandas as pd
import numpy as np

def knots_to_mph(knots):
    
    """
    Converts knots to mph
    
    Returns
    -------
    
    Speed in mpg.     
    """
    
    return knots * 1.1507767864272770986

def knots_to_mps(knots):
    
    """
    Converts knots to m/s
    
    Returns
    -------
    
    Speed in m/s.     
    """
    
    return knots * 0.51444325460445

def round_values(df,
                  parameter,
                  to_nearest=0,
                  data_type='integer'):
    
    """
    Rounds Value to the nearest {to_nearest} and returns either an integer or float datatype
    
    Required Arguments:
    
    1) values (Float or Integer) - The values to round.
    
    2) parameter (String) - The parameter being rounded.
    
    Optional Arguments:
    
    1) to_nearest (Integer) - Default=0. 0 for whole number, 1 for tenths, 2 for hundredths and so on. 
    
    2) data_type (String) - Default='integer'. Set to 'float' when rounding to a decimal. 
    
    Returns
    -------
    
    Rounded values    
    """
    
    data_type = data_type.lower()
    
    if data_type == 'integer':
        df[parameter] = df[parameter].round(to_nearest)
        df[parameter] = df[parameter].convert_dtypes(convert_string=False, 
                                                     convert_integer=True, 
                                                     convert_boolean=False, 
                                                     convert_floating=False)
    else:
        df[parameter] = df[parameter].round(to_nearest)
        
    return df[parameter]
    
def celsius_to_fahrenheit(celsius):
    
    """
    Converts temperature from celsius to fahrenheit.
    
    Required Arguments: 
    
    1) celsius (Integer or Float) - Temperature in celsius.
    
    Returns
    -------
    
    Temperature in fahrenheit.    
    """
    
    fahrenheit = (celsius * (9/5)) + 32
    
    return fahrenheit

def celsius_to_kelvin(celsius):
    
    """
    Converts temperature from celsius to kelvin.
    
    Required Arguments:
    
    1) celsius (Integer or Float) - Temperature in celsius.
    
    Returns
    -------
    
    Temperature in kelvin.    
    """
    
    return celsius - 273.15

def kilometers_to_meters(kilometers):
    
    """
    Converts kilometers to meters
    
    Required Arguments:
    
    1) kilometers (Integer or Float) - Height in Kilometers
    
    Returns
    -------
    
    Height in meters    
    """
    
    return kilometers * 1000


def meters_to_feet(meters):
    
    """
    Converts meters to feet.
    
    Required Arguments:
    
    1) meters (Integer or Float) - Height in meters.
    
    Returns
    -------
    
    Height in feet.    
    """
    
    return meters * 3.28084

def anti_aliasing(x, 
                  y, 
                  anti_aliasing):
    """
    This function interpolates between x and y. 
    
    Required Arguments:
    
    1) x (array) - Array of x-values.
    
    2) y (array) - Array of y-values.
    
    3) anti_aliasing (Integer) - The amount of points in between x and y values. 
    
    Returns
    -------
    
    An interpolated numpy.array of x and y data. 
    """
    
    x = np.asarray(x)
    y = np.asarray(y)
    
    y_point_list = []
    for i in range(0, len(y), 1):
        try:
            y_points = np.linspace(y[i], y[i+1], anti_aliasing)
        except Exception as e:
            pass

        y_point_list.append(y_points)

    x_point_list = []
    for i in range(0, len(x), 1):
        try:
            x_points = np.linspace(x[i], x[i+1], anti_aliasing)
        except Exception as e:
            pass

        x_point_list.append(x_points)
        
    x_point_arr = np.asarray(x_point_list)
    y_point_arr = np.asarray(y_point_list)
    
    x_point_arr = x_point_arr.flatten()
    y_point_arr = y_point_arr.flatten()
    
    return x_point_arr, y_point_arr

    