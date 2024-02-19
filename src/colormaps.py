'''
This file hosts functions that call custom colormaps which are used for plotting. 

This file hosts colormaps for:
                            1) Temperature
                            2) Relative Humidity
                            3) Relative Humidity Change
                            4) Areas of high relative humidity
                            5) Areas of low relative humidity
                            6) The temperature parameter for National Weather Service Red Flag Warnings in Alaska
                            7) The wind speed parameter for National Weather Service Red Flag Warnings nationally. 
                            8) The red shading for areas that meet the weather criteria for National Weather Service Red Flag Warnings. 

This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS


'''

import matplotlib.colors

def temperature_colormap():
    temperature_color_map = matplotlib.colors.LinearSegmentedColormap.from_list("temperature", ["magenta", "darkviolet", "blue", "deepskyblue", "yellow", "mistyrose", "pink", "red", "darkred"])

    return temperature_color_map


def relative_humidity_colormap():
    relative_humidity_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["saddlebrown", "darkorange", "gold", "lightgoldenrodyellow", "yellowgreen", "lawngreen", "springgreen", "lime"])
    
    return relative_humidity_colormap


def relative_humidity_change_colormap():
    relative_humidity_change_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["saddlebrown", "peru", "orange", "gold", "white", "yellowgreen", "lawngreen", "springgreen", "lime"])
    
    return relative_humidity_change_colormap


def excellent_recovery_colormap():
    excellent_recovery_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["greenyellow", "lightgreen", "palegreen", "mediumspringgreen", "springgreen", "lime"])
    
    return excellent_recovery_colormap

def low_relative_humidity_colormap():
    low_relative_humidity_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["saddlebrown", "chocolate", "darkorange", "orange", "gold", "yellow"])
    
    return low_relative_humidity_colormap


def red_flag_warning_alaska_temperature_parameter_colormap():
    red_flag_warning_alaska_temperature_parameter_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("temperature", ["pink", "lightcoral", "red", "darkred"])
    
    return red_flag_warning_alaska_temperature_parameter_colormap

def red_flag_warning_wind_parameter_colormap():
    red_flag_warning_wind_parameter_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("wind speed", ["dodgerblue", "royalblue", "blue", "darkblue", "blueviolet", "darkviolet"])
    
    return red_flag_warning_wind_parameter_colormap

def red_flag_warning_criteria_colormap():
    red_flag_warning_criteria_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("red flag warning", ["white", "red"])
    return red_flag_warning_criteria_colormap


