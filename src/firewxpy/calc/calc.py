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

def mps_to_mph(mps):
    
    """
    Converts m/s to mph
    
    Returns
    -------
    
    Speed in mph    
    """
    
    return mps * 2.23694

def mph_to_kts(mps):
    
    """
    Converts mps to knots
    
    Returns
    -------
    
    Speed in knots
    """

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

def kelvin_to_fahrenheit(kelvin):
    
    """
    Converts temperature from celsius to fahrenheit.
    
    Required Arguments: 
    
    1) celsius (Integer or Float) - Temperature in celsius.
    
    Returns
    -------
    
    Temperature in fahrenheit.    
    """
    celsius= kelvin - 273.15
    
    fahrenheit = (celsius * (9/5)) + 32
    
    return fahrenheit

def fahrenheit_to_kelvin(fahrenheit):
    
    """
    Converts temperature from fahrenheit to kelvin.
    
    Required Arguments: 
    
    1) fahrenheit (Integer or Float) - Temperature in fahrenheit.
    
    Returns
    -------
    
    Temperature in kelvin.    
    """
    celsius = (fahrenheit - 32) * (5/9)
    
    kelvin = celsius + 273.15
    
    return kelvin
    
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

def fahrenheit_to_celsius(fahrenheit):
    
    """
    Converts temperature from fahrenheit to celsius.
    
    Required Arguments: 
    
    1) celsius (Integer or Float) - Temperature in fahrenheit.
    
    Returns
    -------
    
    Temperature in celsius.    
    """
    
    celsius = (fahrenheit - 32) * (5/9)
    
    return celsius

def kelvin_to_celsius(celsius):
    
    """
    Converts temperature from kelvin to celsius.
    
    Required Arguments:
    
    1) celsius (Integer or Float) - Temperature in kelvin.
    
    Returns
    -------
    
    Temperature in celsius.    
    """
    
    return celsius - 273.15

def celsius_to_kelvin(celsius):
    
    """
    Converts temperature fromcelsius to kelvin.
    
    Required Arguments:
    
    1) celsius (Integer or Float) - Temperature in celsius.
    
    Returns
    -------
    
    Temperature in kelvin.    
    """
    
    return celsius + 273.15

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

def u_v_components(ds,
                   u_var_key,
                   v_var_key,
                   deg_var_key,
                   speed_var_key):
    
    """
    Calculates u and v components in a data array.
    
    Returns
    -------
    
    Data Array with u and v components.    
    """
    
    ds['wind_direction_radians'] = np.deg2rad(ds[deg_var_key])
    ds[u_var_key] = -ds[speed_var_key] * np.sin(ds['wind_direction_radians'])
    ds[v_var_key] = -ds[speed_var_key] * np.cos(ds['wind_direction_radians'])
    
    return ds
    
    