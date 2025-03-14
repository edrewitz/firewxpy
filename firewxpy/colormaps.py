import matplotlib.colors
import warnings
warnings.filterwarnings('ignore')

def cross_section_wind_speed():
    cross_section_wind_speed = matplotlib.colors.LinearSegmentedColormap.from_list("cs wind speed", ["darkblue", "blue", "cyan", "lawngreen", "yellowgreen", "orange", "red", "darkred", "violet", "dimgrey"])

    return cross_section_wind_speed    

def precipitation_colormap():
    precipitation_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("precipitation", ["magenta", "blue", "cyan", "lime", "darkgreen", "gold", "orange", "red", "darkred", "maroon", "dimgrey"])

    return precipitation_colormap

def gph_colormap():
    gph_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("gph", [ "indigo", "purple", "darkblue", "blue", "dodgerblue", "cyan", "orange", "darkorange", "orangered", "red", "darkred", "maroon"])

    return gph_colormap

def vorticity_colormap():
    vorticity_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("vorticity", [ "white", "white", "cyan", "lime", "gold", "orangered", "darkred", "blueviolet", "dimgrey"])

    return vorticity_colormap

def temperature_colormap():
    temperature_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("temperature", ["darkviolet", "blue", "deepskyblue", "white", "orangered", "red", "darkred"])

    return temperature_colormap

def temperature_colormap_alt():
    temperature_colormap_alt = matplotlib.colors.LinearSegmentedColormap.from_list("temperature alt", ["darkviolet", "blue", "deepskyblue", "lime", "gold", "orangered", "red", "darkred"])

    return temperature_colormap_alt

def gph_change_colormap():
    gph_change_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("gph change", ["darkblue", "blue", "deepskyblue", "white", "orangered", "red", "darkred"])

    return gph_change_colormap

def temperature_change_colormap():
    temperature_change_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("temperature change", ["darkblue", "blue", "deepskyblue", "lightgrey", "lightgrey", "orangered", "red", "darkred"])

    return temperature_change_colormap

def vertical_velocity_colormap():
    vertical_velocity_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("vv", ["darkblue", "blue", "deepskyblue", "orangered", "red", "darkred"])

    return vertical_velocity_colormap

def dew_point_colormap():
    dew_point_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("dew point", ["darkorange", "orange", "darkkhaki", "forestgreen", "lime", "aqua"])

    return dew_point_colormap

def dew_point_change_colormap():
    dew_point_change_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("dew point change", ["darkorange", "darkkhaki", "white", "white", "forestgreen", "aqua"])

    return dew_point_change_colormap

def wind_speed_colormap():
    wind_speed_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("wind speed", ["magenta", "purple", "blue", "cyan", "goldenrod", "darkgoldenrod", "orange", "darkorange"])

    return wind_speed_colormap

def theta_e_colormap():
    theta_e_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("theta e", ["darkblue", "dodgerblue", "turquoise", "lawngreen", "gold", "darkorange", "darkred"])

    return theta_e_colormap

def wind_speed_change_colormap():
    wind_speed_change_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("wind speed change", ["magenta", "blue", "white", "white", "darkgoldenrod", "darkorange"])

    return wind_speed_change_colormap

def thresh_contour_line_relative_humidity_colormap():
    thresh_contour_line_relative_humidity_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity thresh", ["black"])
    
    return thresh_contour_line_relative_humidity_colormap

def relative_humidity_colormap():
    relative_humidity_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["saddlebrown", "darkorange", "gold", "lightgoldenrodyellow", "yellowgreen", "lawngreen", "springgreen", "lime"])
    
    return relative_humidity_colormap


def relative_humidity_change_colormap():
    relative_humidity_change_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["saddlebrown", "peru", "orange", "gold", "lightgrey", "yellowgreen", "lawngreen", "springgreen", "lime"])
    
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

def SPC_Dry_Lightning_Risk_Outlook_colormap():
    SPC_Dry_Lightning_Risk_Outlook_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("SPC Dry Lightning Outlook", ["darkorange", "red"])
    
    return SPC_Dry_Lightning_Risk_Outlook_colormap


def red_flag_warning_alaska_temperature_parameter_colormap():
    red_flag_warning_alaska_temperature_parameter_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("temperature", ["pink", "lightcoral", "red", "darkred"])
    
    return red_flag_warning_alaska_temperature_parameter_colormap

def red_flag_warning_wind_parameter_colormap():
    red_flag_warning_wind_parameter_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("wind speed", ["dodgerblue", "royalblue", "blue", "darkblue", "blueviolet", "darkviolet"])
    
    return red_flag_warning_wind_parameter_colormap

def red_flag_warning_criteria_colormap():
    red_flag_warning_criteria_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("red flag warning", ["beige", "red"])
    return red_flag_warning_criteria_colormap

def red_flag_warning_criteria_colormap_alt():
    red_flag_warning_criteria_colormap_alt = matplotlib.colors.LinearSegmentedColormap.from_list("red flag warning alt", ["beige", "purple"])
    return red_flag_warning_criteria_colormap_alt

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

def cloud_cover_colormap():
    cloud_cover_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("cloud cover", ["deepskyblue", "lightslategrey"])
    
    return cloud_cover_colormap   

def cloud_cover_change_colormap():
    cloud_cover_change_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("cloud cover change", ["deepskyblue", "white", "lightslategrey"])
    
    return cloud_cover_change_colormap

def colorblind_mode_divergent_colormap():
    colorblind_mode_divergent_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("colorblind mode divergent", ["indigo", "darkviolet", "white", "white", "orange", "darkorange"])
    
    return colorblind_mode_divergent_colormap
