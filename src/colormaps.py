import matplotlib.colors

def temperature_colormap():
    temperature_color_map = matplotlib.colors.LinearSegmentedColormap.from_list("temperature", ["magenta", "darkviolet", "blue", "deepskyblue", "yellow", "mistyrose", "pink", "red", "darkred"])

    return temperature_color_map


def relative_humidity_colormap():
    relative_humidity_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["saddlebrown", "darkorange", "gold", "lightgoldenrodyellow", "yellowgreen", "lawngreen", "springgreen", "lime"])
    
    return relative_humidity_colormap


def relative_humidity_change_colormap():
    relative_humidity_change_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["saddlebrown", "darkorange", "gold", "lightgoldenrodyellow", "white", "yellowgreen", "lawngreen", "springgreen", "lime"])
    
    return relative_humidity_change_colormap


def excellent_recovery_colormap():
    excellent_recovery_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("relative humidity", ["greenyellow", "lightgreen", "palegreen", "mediumspringgreen", "springgreen", "lime"])
    
    return excellent_recovery_colormap

