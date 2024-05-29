import matplotlib.colors


def temperature_colormap():
    temperature_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("temperature", ["darkviolet", "blue", "deepskyblue", "white", "orangered", "red", "darkred"])

    return temperature_colormap


def wind_speed_change_colormap():
    wind_speed_change_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("wind speed", ["darkgreen", "green", "white", "white", "red", "darkred"])

    return wind_speed_change_colormap


def relative_humidity_colormap():
    relative_humidity_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["saddlebrown", "darkorange", "gold", "lightgoldenrodyellow", "yellowgreen", "lawngreen", "springgreen", "lime"])
    
    return relative_humidity_colormap


def relative_humidity_change_colormap():
    relative_humidity_change_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["saddlebrown", "peru", "orange", "gold", "white", "white", "yellowgreen", "lawngreen", "springgreen", "lime"])
    
    return relative_humidity_change_colormap


def excellent_recovery_colormap():
    excellent_recovery_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["greenyellow", "lightgreen", "palegreen", "mediumspringgreen", "springgreen", "lime"])
    
    return excellent_recovery_colormap

def low_relative_humidity_colormap():
    low_relative_humidity_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["saddlebrown", "chocolate", "darkorange", "orange"])
    
    return low_relative_humidity_colormap

def SPC_Critical_Fire_Weather_Risk_Outlook_colormap():
    SPC_Critical_Fire_Weather_Risk_Outlook_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("SPC Critical Fire Weather Outlook", ["gold", "darkorange", "red"])
    
    return SPC_Critical_Fire_Weather_Risk_Outlook_colormap


def red_flag_warning_alaska_temperature_parameter_colormap():
    red_flag_warning_alaska_temperature_parameter_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("temperature", ["pink", "lightcoral", "red", "darkred"])
    
    return red_flag_warning_alaska_temperature_parameter_colormap

def red_flag_warning_wind_parameter_colormap():
    red_flag_warning_wind_parameter_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("wind speed", ["dodgerblue", "royalblue", "blue", "darkblue", "blueviolet", "darkviolet"])
    
    return red_flag_warning_wind_parameter_colormap

def red_flag_warning_criteria_colormap():
    red_flag_warning_criteria_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("red flag warning", ["white", "red"])
    return red_flag_warning_criteria_colormap

def cool_temperatures_colormap():
    cool_temperatures_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("cool temperatures", ["darkviolet", "darkblue", "blue", "dodgerblue"])
    return cool_temperatures_colormap

def warm_temperatures_colormap():
    warm_temperatures_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("warm temperatures", ["pink", "tomato", "red", "darkred"])
    return warm_temperatures_colormap

def negative_relative_humidity_trend_colormap():
    negative_relative_humidity_trend_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("negative relative humidity", ["saddlebrown", "peru", "darkgoldenrod", "goldenrod", "darkorange", "orange"])
    
    return negative_relative_humidity_trend_colormap


def positive_relative_humidity_trend_colormap():
    positive_relative_humidity_trend_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("positive relative humidity", ["yellowgreen", "chartreuse", "lime", "springgreen", "green", "darkgreen"])
    
    return positive_relative_humidity_trend_colormap

def relative_humidity_change_filtered_colormap():
    relative_humidity_change_filtered_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity change filtered", ["saddlebrown", "peru", "darkgoldenrod", "darkorange", "white", "white", "lawngreen", "springgreen", "green", "darkgreen"])
    
    return relative_humidity_change_filtered_colormap    


