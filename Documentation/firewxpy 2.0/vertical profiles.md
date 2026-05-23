# Observed Vertical Profiles

**Table of Contents**

1) [Temperature/Relative Humidity/Wind](https://github.com/edrewitz/firewxpy/blob/main/Documentation/firewxpy%202.0/vertical%20profiles.md#temperaturerelative-humiditywind)
2) [Temperature/Wind](https://github.com/edrewitz/firewxpy/blob/main/Documentation/firewxpy%202.0/vertical%20profiles.md#temperaturewind)
3) [Relative Humidity/Winds](https://github.com/edrewitz/firewxpy/blob/main/Documentation/firewxpy%202.0/vertical%20profiles.md#relative-humiditywinds)
4) [Temperature/Relative Humidity/Wind Comparison](https://github.com/edrewitz/firewxpy/blob/main/Documentation/firewxpy%202.0/vertical%20profiles.md#temperaturerelative-humiditywind-comparison)
5) [Temperature/Wind Comparison](https://github.com/edrewitz/firewxpy/blob/main/Documentation/firewxpy%202.0/vertical%20profiles.md#temperaturewind-comparison)
6) [Relative Humidity/Wind Comparison](https://github.com/edrewitz/firewxpy/blob/main/Documentation/firewxpy%202.0/vertical%20profiles.md#relative-humiditywind-comparison)

#### Temperature/Relative Humidity/Wind
***def plot_temperature_relative_humidity_wind_profile(station_id,
                                                    current=True,
                                                    custom_time=None,
                                                    proxies=None,
                                                    clear_recycle_bin=False,
                                                    path='FireWxPy Graphics/Observations/Upper Air/Temperature Relative Humidity Wind Profiles',
                                                    to_fahrenheit=False,
                                                    to_kelvin=False,
                                                    to_meters=False,
                                                    to_feet=True,
                                                    to_mph=True,
                                                    to_mps=False,
                                                    anti_aliasing=100,
                                                    temperature_colormap='coolwarm',
                                                    temperature_alpha=1,
                                                    relative_humidity_colormap='BrBG',
                                                    relative_humidity_alpha=1,
                                                    wind_colormap='rainbow',
                                                    wind_barb_length=5,
                                                    wind_barb_alpha=1,
                                                    y_bottom=0,
                                                    y_top=10000,
                                                    fig_x=15,
                                                    fig_y=8,
                                                    signature_box_x=0.85,
                                                    signature_box_y=-0.15,
                                                    signature_box_style='round',
                                                    signature_box_color='steelblue',
                                                    signature_box_alpha=0.5,
                                                    signature_fontsize=8,
                                                    signature_fontcolor='black',
                                                    x_title_position=0.015,
                                                    title_1_fontsize=14,
                                                    title_1_box_style='round',
                                                    title_1_box_color='steelblue',
                                                    title_1_box_alpha=0.5,
                                                    title_1_fontcolor='black',
                                                    title_2_fontsize=12,
                                                    title_2_box_style='round',
                                                    title_2_box_color='crimson',
                                                    title_2_box_alpha=0.5,
                                                    title_2_fontcolor='black',
                                                    title_2_y_position=1,
                                                    title_3_fontsize=12,
                                                    title_3_box_style='round',
                                                    title_3_box_color='lime',
                                                    title_3_box_alpha=0.5,
                                                    title_3_fontcolor='black',
                                                    title_3_y_position=1,
                                                    title_4_fontsize=12,
                                                    title_4_box_style='round',
                                                    title_4_box_color='orange',
                                                    title_4_box_alpha=0.5,
                                                    title_4_fontcolor='black',
                                                    title_4_y_position=1,
                                                    x_axis1_box_style='round',
                                                    x_axis1_box_color='crimson',
                                                    x_axis1_box_alpha=0.5,
                                                    x_axis2_box_style='round',
                                                    x_axis2_box_color='lime',
                                                    x_axis2_box_alpha=0.5,
                                                    x_axis3_box_style='round',
                                                    x_axis3_box_color='orange',
                                                    x_axis3_box_alpha=0.5,
                                                    x_axis_label_fontsize=12,
                                                    y_axis_label_fontsize=12,
                                                    axes_label_color='black',
                                                    xtick_color='black',
                                                    ytick_color='black',
                                                    facecolor='lavender',
                                                    df=None,
                                                    date=None,
                                                    subplot_background_color='silver'):***

    This function plots an observed temperature/relative humidity/wind profile from an atmospheric sounding.
    
    Required Arguments:
    
    1) station_id (String) - The station ID for the sounding site.
    
    Optional Arguments:
    
    1) current (Boolean) - Default=True. When set to True, the function defaults to the latest sounding. Set to False
        when plotting past soundings.
        
    2) custom_time (String) - Default=None. When plotting archived sounding data, specify the custom time as a string in the
        form of 'YYYY-mm-dd:HH'.
        
    3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    4) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    5) path (String) - Default='FireWxPy Graphics/Observations/Upper Air/Temperature Relative Humidity Wind Profiles'. The path where
        the graphic will save.
        
    6) to_fahrenheit (Boolean) - Default=False. Set to True for temperature in Fahrenheit.
    
    7) to_kelvin (Boolean) - Default=False. Set to True for temperature in Kelvin.
    
    8) to_meters (Boolean) - Default=False. Set to True for height in meters.
    
    9) to_feet (Boolean) - Default=True. Set to True for height in feet.
    
    10) to_mph (Boolean) - Default=True. Set to True for wind speed in miles per hour. 
    
    11) to_mps (Boolean) - Default=False. Set to True for wind speed in meters per second.
    
    12) anti_aliasing (Integer) - Default=100. This is the amount of data points interpolated between observed data points.
        The higher the number the more interpolated data points. This is for those who want to have a colormapped profile that
        appears as a line but is a series of colormapped scatter points.
        
    13) temperature_colormap (String) - Default='coolwarm'. The colormap for the temperature line.
    
    14) temperature_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    15) relative_humidity_colormap (String) - Default='BrBG'. The colormap for the relative humidity line.
    
    16) relative_humidity_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    17) wind_colormap (String) - Default='rainbow'. The colormap of the wind barbs.
    
    18) wind_barb_length (Integer) - Default=5. The length of the wind barb.
    
    19) wind_barb_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    20) y_bottom (Integer) - Default=0. The height in feet where the y-axis begins.
    
    21) y_top (Integer) - Default=10000. The height in feet where the y-axis ends.     
    
    22) fig_x (Integer) - Default=15. The x-length of the figure.
    
    23) fig_y (Integer) - Default=8. The y-length of the figure.
    
    24) signature_box_x (Float) - Default=0.85. The x-position of the signature text box with respect to the figure axis.
    
    25) signature_box_y (Float) - Default=-0.15. The y-position of the signature text box with respect to the figure axis.                              

    26) signature_box_style (String) - Default='round'. The style of the text box. 
    
    27) signature_box_color (String) - Default='steelblue'. The color of the text box.
    
    28) signature_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    29) signature_fontsize (Integer) - Default=8. Font size of the font in the textbox. 
    
    30) signature_fontcolor (String) - Default='black'. Font color of the font in the textbox. 
    
    31) x_title_position (Float) - Default=0.015. The x-position for all titles with respect to the figure axis.
    
    32) title_1_fontsize (Integer) - Default=14. Font size of the figure title.
    
    33) title_1_box_style (String) - Default='round'. Text box style of the figure title textbox.
    
    34) title_1_box_color (String) - Default='steelblue'. The color of the text box of the figure title.
    
    35) title_1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    36) title_1_fontcolor (String) - Default='black'. Font color of the first subplot title.
    
    37) title_2_fontsize (Integer) - Default=12. Font size of the first subplot title.
    
    38) title_2_box_style (String) - Default='round'. Text box style of the first subplot text box.
    
    39) title_2_box_color (String) - Default='crimson'. Text box color of the first subplot text box.
    
    40) title_2_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    41) title_2_fontcolor (String) - Default='black'. Font color of the first subplot title.
    
    42) title_2_y_position (Float or Integer) - Default=1. The y-axis positon of the second subplot text box.
    
    43) title_3_fontsize (Integer) - Default=12. Font size of the second subplot title.
    
    44) title_3_box_style (String) - Default='round'. Text box style of the second subplot text box.
    
    45) title_3_box_color (String) - Default='crimson'. Text box color of the second subplot text box.
    
    46) title_3_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    47) title_3_fontcolor (String) - Default='black'. Font color of the second subplot title.
    
    48) title_3_y_position (Float or Integer) - Default=1. The y-axis positon of the second subplot text box.
    
    49) title_4_fontsize (Integer) - Default=12. Font size of the third subplot title.
    
    50) title_4_box_style (String) - Default='round'. Text box style of the third subplot text box.
    
    51) title_4_box_color (String) - Default='crimson'. Text box color of the third subplot text box.
    
    52) title_4_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    53) title_4_fontcolor (String) - Default='black'. Font color of the third subplot title.
    
    54) title_4_y_position (Float or Integer) - Default=1. The y-axis positon of the third subplot text box.
    
    55) x_axis1_box_style (String) - Default='round'. Text box style of the first subplot x-axis text box.
    
    56) x_axis1_box_color (String) - Default='crimson'. Text box color of the first subplot x-axis text box.
    
    57) x_axis1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    58) x_axis2_box_style (String) - Default='round'. Text box style of the second subplot x-axis text box.
    
    59) x_axis2_box_color (String) - Default='crimson'. Text box color of the second subplot x-axis text box.
    
    60) x_axis2_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque.  
        
    61) x_axis3_box_style (String) - Default='round'. Text box style of the third subplot x-axis text box.
    
    62) x_axis3_box_color (String) - Default='crimson'. Text box color of the third subplot x-axis text box.
    
    63) x_axis3_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque.  
    
    64) x_axis_label_fontsize (Integer) - Default=12. Font size of x-axis labels.
    
    65) y_axis_label_fontsize (Integer) - Default=12. Font size of y-axis labels.
    
    66) axes_label_color (String) - Default='black'. The color of the labels on each axis.
    
    67) xtick_color (String) - Default='black'. The color of the x-ticks.
    
    68) ytick_color (String) - Default='black'. The color of the y-ticks.                                                

    70) facecolor (String) - Default='lavander'. The face color of the figure.
    
    71) df (Pandas.DataFrame) - Default=None. If the user wishes to download a medley of Pandas.DataFrames with WxData
        and pass those data frames into the plotting function, set df=df. 
        
    72) date (Datetime) - Default=None. The datetime object associated with the Pandas.DataFrame when downloading 
        the data with WxData outside of the function and passing the date into the function. Set date=date if the user
        is not downloading the data within the function.
        
    73) subplot_background_color (String) - Default='silver'. The background color of each subplot axis.
                                                    
    Returns
    -------
    
    A figure of the vertical profiles saved to {path}

#### Temperature/Wind
***def plot_temperature_wind_profile(station_id,
                                current=True,
                                custom_time=None,
                                proxies=None,
                                clear_recycle_bin=False,
                                path='FireWxPy Graphics/Observations/Upper Air/Temperature Wind Profiles',
                                to_fahrenheit=True,
                                to_kelvin=False,
                                to_meters=False,
                                to_feet=True,
                                to_mph=True,
                                to_mps=False,
                                anti_aliasing=100,
                                temperature_colormap='coolwarm',
                                temperature_alpha=1,
                                wind_colormap='rainbow',
                                wind_barb_length=7,
                                wind_barb_alpha=1,
                                y_bottom=0,
                                y_top=10000,
                                fig_x=15,
                                fig_y=8,
                                signature_box_x=0.25,
                                signature_box_y=-0.15,
                                signature_box_style='round',
                                signature_box_color='steelblue',
                                signature_box_alpha=0.5,
                                signature_fontsize=8,
                                signature_fontcolor='black',
                                title_1_fontsize=14,
                                title_1_box_style='round',
                                title_1_box_color='steelblue',
                                title_1_box_alpha=0.5,
                                title_1_fontcolor='black',
                                title_2_fontsize=12,
                                title_2_box_style='round',
                                title_2_box_color='crimson',
                                title_2_box_alpha=0.5,
                                title_2_fontcolor='black',
                                title_2_y_position=1,
                                title_3_fontcolor='black',
                                x_axis1_box_style='round',
                                x_axis1_box_color='crimson',
                                x_axis1_box_alpha=0.5,
                                max_temperature_text_box_x_position=0.01,
                                max_temperature_text_box_y_position=0.975,
                                max_temperature_text_box_style='round',
                                max_temperature_text_box_color='crimson',
                                max_temperature_text_box_alpha=1,
                                min_temperature_text_box_x_position=0.415,
                                min_temperature_text_box_y_position=0.975,
                                min_temperature_text_box_style='round',
                                min_temperature_text_box_color='cyan',
                                min_temperature_text_box_alpha=1,
                                max_wind_text_box_x_position=0.75,
                                max_wind_text_box_y_position=0.975,
                                max_wind_text_box_style='round',
                                max_wind_text_box_color='orange',
                                max_wind_text_box_alpha=1,
                                x_axis_label_fontsize=12,
                                y_axis_label_fontsize=12,
                                axes_label_color='black',
                                legend_fontsize=10,
                                xtick_color='black',
                                ytick_color='black',
                                facecolor='lavender',
                                df=None,
                                date=None,
                                subplot_background_color='silver'):***

    This function plots an observed temperature/wind profile from an atmospheric sounding.
    
    Required Arguments:
    
    1) station_id (String) - The station ID for the sounding site.
    
    Optional Arguments:
    
    1) current (Boolean) - Default=True. When set to True, the function defaults to the latest sounding. Set to False
        when plotting past soundings.
        
    2) custom_time (String) - Default=None. When plotting archived sounding data, specify the custom time as a string in the
        form of 'YYYY-mm-dd:HH'.
        
    3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    4) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    5) path (String) - Default='FireWxPy Graphics/Observations/Upper Air/Temperature Wind Profiles'. The path where
        the graphic will save.
        
    6) to_fahrenheit (Boolean) - Default=False. Set to True for temperature in Fahrenheit.
    
    7) to_kelvin (Boolean) - Default=False. Set to True for temperature in Kelvin.
    
    8) to_meters (Boolean) - Default=False. Set to True for height in meters.
    
    9) to_feet (Boolean) - Default=True. Set to True for height in feet.
    
    10) to_mph (Boolean) - Default=True. Set to True for wind speed in miles per hour. 
    
    11) to_mps (Boolean) - Default=False. Set to True for wind speed in meters per second.
    
    12) anti_aliasing (Integer) - Default=100. This is the amount of data points interpolated between observed data points.
        The higher the number the more interpolated data points. This is for those who want to have a colormapped profile that
        appears as a line but is a series of colormapped scatter points.
        
    13) temperature_colormap (String) - Default='coolwarm'. The colormap for the temperature line.
    
    14) temperature_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    15) wind_colormap (String) - Default='rainbow'. The colormap of the wind barbs.
    
    16) wind_barb_length (Integer) - Default=5. The length of the wind barb.
    
    17) wind_barb_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    18) y_bottom (Integer) - Default=0. The height in feet where the y-axis begins.
    
    19) y_top (Integer) - Default=10000. The height in feet where the y-axis ends.     
    
    20) fig_x (Integer) - Default=15. The x-length of the figure.
    
    21) fig_y (Integer) - Default=8. The y-length of the figure.
    
    22) signature_box_x (Float) - Default=0.85. The x-position of the signature text box with respect to the figure axis.
    
    23) signature_box_y (Float) - Default=-0.15. The y-position of the signature text box with respect to the figure axis.                              

    24) signature_box_style (String) - Default='round'. The style of the text box. 
    
    25) signature_box_color (String) - Default='steelblue'. The color of the text box.
    
    26) signature_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    27) signature_fontsize (Integer) - Default=8. Font size of the font in the textbox. 
    
    28) signature_fontcolor (String) - Default='black'. Font color of the font in the textbox. 
    
    29) x_title_position (Float) - Default=0.015. The x-position for all titles with respect to the figure axis.
    
    30) title_1_fontsize (Integer) - Default=14. Font size of the figure title.
    
    31) title_1_box_style (String) - Default='round'. Text box style of the figure title textbox.
    
    32) title_1_box_color (String) - Default='steelblue'. The color of the text box of the figure title.
    
    33) title_1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    34) title_1_fontcolor (String) - Default='black'. Font color of the figure title.
    
    35) title_2_fontsize (Integer) - Default=12. Font size of the first subplot title.
    
    36) title_2_box_style (String) - Default='round'. Text box style of the subplot title text box.
    
    37) title_2_box_color (String) - Default='crimson'. Text box color of the subplot title text box.
    
    38) title_2_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    39) title_2_fontcolor (String) - Default='black'. Font color of the subplot title.
    
    40) title_2_y_position (Float or Integer) - Default=1. The y-axis positon of the subplot title text box.
        
    41) title_3_fontcolor (String) - Default='black'. Font color of the tertiary subplot titles.
    
    42) x_axis1_box_style (String) - Default='round'. Text box style of the first subplot x-axis text box.
    
    43) x_axis1_box_color (String) - Default='crimson'. Text box color of the first subplot x-axis text box.
    
    44) x_axis1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
    
    45) x_axis1_box_style (String) - Default='round'. Text box style for the general x-axis text box.
    
    46) x_axis1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    47) max_temperature_text_box_x_position (Float) - Default=0.01. x-position of the maximum temperature text box
        with respect to the figure axis. 
        
    48) max_temperature_text_box_y_position (Float) - Default=0.975. y-position of the maximum temperature text box
        with respect to the figure axis. 
        
    49) max_temperature_text_box_style (String) - Default='round'. Style of the maximum temperature text box.
    
    50) max_temperature_text_box_color (String) - Default='crimson'. Color of the maximum temperature text box.
    
    51) max_temperature_text_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    52) min_temperature_text_box_x_position (Float) - Default=0.415. x-position of the minimum temperature text box
        with respect to the figure axis. 
        
    53) min_temperature_text_box_y_position (Float) - Default=0.975. y-position of the minimum temperature text box
        with respect to the figure axis. 
        
    54) min_temperature_text_box_style (String) - Default='round'. Style of the minimum temperature text box.
    
    55) min_temperature_text_box_color (String) - Default='cyan'. Color of the minimum temperature text box.
    
    56) min_temperature_text_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    57) max_wind_text_box_x_position (Float) - Default=0.75. x-position of the maximum wind speed text box
        with respect to the figure axis. 
        
    58) max_wind_text_box_y_position (Float) - Default=0.975. y-position of the maximum wind speed text box
        with respect to the figure axis. 
        
    59) max_wind_text_box_style (String) - Default='round'. Style of the maximum wind speed text box.
    
    60) max_wind_text_box_color (String) - Default='orange'. Color of the maximum wind speed text box.
    
    61) max_wind_text_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    62) x_axis_label_fontsize (Integer) - Default=12. Font size of x-axis labels.
    
    63) y_axis_label_fontsize (Integer) - Default=12. Font size of y-axis labels.
    
    64) axes_label_color (String) - Default='black'. The color of the labels on each axis.
    
    65) xtick_color (String) - Default='black'. The color of the x-ticks.
    
    66) ytick_color (String) - Default='black'. The color of the y-ticks.                                                

    67) facecolor (String) - Default='lavander'. The face color of the figure.
    
    68) df (Pandas.DataFrame) - Default=None. If the user wishes to download a medley of Pandas.DataFrames with WxData
        and pass those data frames into the plotting function, set df=df. 
        
    69) date (Datetime) - Default=None. The datetime object associated with the Pandas.DataFrame when downloading 
        the data with WxData outside of the function and passing the date into the function. Set date=date if the user
        is not downloading the data within the function.
        
    70) subplot_background_color (String) - Default='silver'. The background color of each subplot axis.                   
                                                    
    Returns
    -------
    
    A figure of the vertical profiles saved to {path}

#### Relative Humidity/Winds
***def plot_relative_humidity_wind_profile(station_id,
                                        current=True,
                                        custom_time=None,
                                        proxies=None,
                                        clear_recycle_bin=False,
                                        path='FireWxPy Graphics/Observations/Upper Air/Relative Humidity Wind Profiles',
                                        to_meters=False,
                                        to_feet=True,
                                        to_mph=True,
                                        to_mps=False,
                                        anti_aliasing=100,
                                        relative_humidity_colormap='BrBG',
                                        relative_humidity_alpha=1,
                                        wind_colormap='rainbow',
                                        wind_barb_length=5,
                                        wind_barb_alpha=1,
                                        y_bottom=0,
                                        y_top=10000,
                                        fig_x=15,
                                        fig_y=8,
                                        signature_box_x=0.25,
                                        signature_box_y=-0.15,
                                        signature_box_style='round',
                                        signature_box_color='steelblue',
                                        signature_box_alpha=0.5,
                                        signature_fontsize=8,
                                        signature_fontcolor='black',
                                        title_1_fontsize=14,
                                        title_1_box_style='round',
                                        title_1_box_color='steelblue',
                                        title_1_box_alpha=0.5,
                                        title_1_fontcolor='black',
                                        title_2_fontsize=12,
                                        title_2_box_style='round',
                                        title_2_box_color='lime',
                                        title_2_box_alpha=0.5,
                                        title_2_fontcolor='black',
                                        title_2_y_position=1.02,
                                        x_axis1_box_style='round',
                                        x_axis1_box_color='lime',
                                        x_axis1_box_alpha=0.5,
                                        min_rh_height_box_style='round',
                                        min_rh_height_box_color='saddlebrown',
                                        min_rh_height_box_alpha=1,
                                        min_rh_height_box_x_position=0.01,
                                        min_rh_height_box_y_position=0.975,
                                        max_rh_height_box_style='round',
                                        max_rh_height_box_color='lime',
                                        max_rh_height_box_alpha=1,
                                        max_rh_height_box_x_position=0.25,
                                        max_rh_height_box_y_position=0.975,
                                        rh_range_height_box_style='round',
                                        rh_range_height_box_color='lightblue',
                                        rh_range_height_box_alpha=1,
                                        rh_range_height_box_x_position=0.525,
                                        rh_range_height_box_y_position=0.975,
                                        max_wind_height_box_style='round',
                                        max_wind_height_box_color='crimson',
                                        max_wind_height_box_alpha=1,
                                        max_wind_height_box_x_position=0.705,
                                        max_wind_height_box_y_position=0.975,
                                        legend_fontsize=10,
                                        x_axis_label_fontsize=12,
                                        y_axis_label_fontsize=12,
                                        axes_label_color='black',
                                        xtick_color='black',
                                        ytick_color='black',
                                        facecolor='lavender',
                                        df=None,
                                        date=None,
                                        subplot_background_color='silver'):***

    This function plots an observed relative humidity/wind profile from an atmospheric sounding.
    
    Required Arguments:
    
    1) station_id (String) - The station ID for the sounding site.
    
    Optional Arguments:
    
    1) current (Boolean) - Default=True. When set to True, the function defaults to the latest sounding. Set to False
        when plotting past soundings.
        
    2) custom_time (String) - Default=None. When plotting archived sounding data, specify the custom time as a string in the
        form of 'YYYY-mm-dd:HH'.
        
    3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    4) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    5) path (String) - Default='FireWxPy Graphics/Observations/Upper Air/Relative Humidity Wind Profiles'. The path where
        the graphic will save.
                
    8) to_meters (Boolean) - Default=False. Set to True for height in meters.
    
    9) to_feet (Boolean) - Default=True. Set to True for height in feet.
    
    10) to_mph (Boolean) - Default=True. Set to True for wind speed in miles per hour. 
    
    11) to_mps (Boolean) - Default=False. Set to True for wind speed in meters per second.
    
    12) anti_aliasing (Integer) - Default=100. This is the amount of data points interpolated between observed data points.
        The higher the number the more interpolated data points. This is for those who want to have a colormapped profile that
        appears as a line but is a series of colormapped scatter points.
        
    13) relative_humidity_colormap (String) - Default='BrBG'. The colormap for the temperature line.
    
    14) relative_humidity_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    15) wind_colormap (String) - Default='rainbow'. The colormap of the wind barbs.
    
    16) wind_barb_length (Integer) - Default=5. The length of the wind barb.
    
    17) wind_barb_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    18) y_bottom (Integer) - Default=0. The height in feet where the y-axis begins.
    
    19) y_top (Integer) - Default=10000. The height in feet where the y-axis ends.     
    
    20) fig_x (Integer) - Default=15. The x-length of the figure.
    
    21) fig_y (Integer) - Default=8. The y-length of the figure.
    
    22) signature_box_x (Float) - Default=0.85. The x-position of the signature text box with respect to the figure axis.
    
    23) signature_box_y (Float) - Default=-0.15. The y-position of the signature text box with respect to the figure axis.                              

    24) signature_box_style (String) - Default='round'. The style of the text box. 
    
    25) signature_box_color (String) - Default='steelblue'. The color of the text box.
    
    26) signature_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    27) signature_fontsize (Integer) - Default=8. Font size of the font in the textbox. 
    
    28) signature_fontcolor (String) - Default='black'. Font color of the font in the textbox. 
    
    29) x_title_position (Float) - Default=0.015. The x-position for all titles with respect to the figure axis.
    
    30) title_1_fontsize (Integer) - Default=14. Font size of the figure title.
    
    31) title_1_box_style (String) - Default='round'. Text box style of the figure title textbox.
    
    32) title_1_box_color (String) - Default='steelblue'. The color of the text box of the figure title.
    
    33) title_1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    34) title_1_fontcolor (String) - Default='black'. Font color of the figure title.
    
    35) title_2_fontsize (Integer) - Default=12. Font size of the subplot title.
    
    36) title_2_box_style (String) - Default='round'. Text box style of the subplot title text box.
    
    37) title_2_box_color (String) - Default='lime'. Text box color of the subplot title text box.
    
    38) title_2_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    39) title_2_fontcolor (String) - Default='black'. Font color of the subplot title.
    
    40) title_2_y_position (Float or Integer) - Default=1. The y-axis positon of the subplot text box.
            
    41) x_axis1_box_style (String) - Default='round'. Text box style of the first subplot x-axis text box.
    
    42) x_axis1_box_color (String) - Default='crimson'. Text box color of the first subplot x-axis text box.
    
    43) x_axis1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
    
    44) x_axis1_box_style (String) - Default='round'. Text box style for the general x-axis text box.
    
    45) x_axis1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    46) max_rh_text_box_x_position (Float) - Default=0.01. x-position of the maximum relative humidity text box
        with respect to the figure axis. 
        
    47) max_rh_text_box_y_position (Float) - Default=0.975. y-position of the maximum relative humidity text box
        with respect to the figure axis. 
        
    48) max_rh_text_box_style (String) - Default='round'. Style of the maximum relative humidity text box.
    
    49) max_rh_text_box_color (String) - Default='crimson'. Color of the maximum relative humidity text box.
    
    50) max_rh_text_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    51) min_rh_text_box_x_position (Float) - Default=0.415. x-position of the minimum relative humidity text box
        with respect to the figure axis. 
        
    52) min_rh_text_box_y_position (Float) - Default=0.975. y-position of the minimum relative humidity text box
        with respect to the figure axis. 
        
    53) min_rh_text_box_style (String) - Default='round'. Style of the minimum relative humidity text box.
    
    54) min_rh_text_box_color (String) - Default='saddlebrown'. Color of the minimum relative humidity text box.
    
    55) min_rh_text_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    56) max_wind_text_box_x_position (Float) - Default=0.75. x-position of the maximum wind speed text box
        with respect to the figure axis. 
        
    57) max_wind_text_box_y_position (Float) - Default=0.975. y-position of the maximum wind speed text box
        with respect to the figure axis. 
        
    58) max_wind_text_box_style (String) - Default='round'. Style of the maximum wind speed text box.
    
    59) max_wind_text_box_color (String) - Default='crimson'. Color of the maximum wind speed text box.
    
    60) max_wind_text_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    61) x_axis_label_fontsize (Integer) - Default=12. Font size of x-axis labels.
    
    62) y_axis_label_fontsize (Integer) - Default=12. Font size of y-axis labels.
    
    63) axes_label_color (String) - Default='black'. The color of the labels on each axis.
    
    64) xtick_color (String) - Default='black'. The color of the x-ticks.
    
    65) ytick_color (String) - Default='black'. The color of the y-ticks.                                                

    66) facecolor (String) - Default='lavander'. The face color of the figure.
    
    67) df (Pandas.DataFrame) - Default=None. If the user wishes to download a medley of Pandas.DataFrames with WxData
        and pass those data frames into the plotting function, set df=df. 
        
    68) date (Datetime) - Default=None. The datetime object associated with the Pandas.DataFrame when downloading 
        the data with WxData outside of the function and passing the date into the function. Set date=date if the user
        is not downloading the data within the function.
        
    69) subplot_background_color (String) - Default='silver'. The background color of each subplot axis.                   
                                                    
    Returns
    -------
    
    A figure of the vertical profiles saved to {path}

#### Temperature/Relative Humidity/Wind Comparison
***def plot_temperature_relative_humidity_wind_profile_comparison(station_id,
                                                    current=True,
                                                    custom_time_1=None,
                                                    custom_time_2=None,
                                                    proxies=None,
                                                    clear_recycle_bin=False,
                                                    path='FireWxPy Graphics/Observations/Upper Air/Temperature Relative Humidity Wind Profiles Comparison',
                                                    to_fahrenheit=False,
                                                    to_kelvin=False,
                                                    to_meters=False,
                                                    to_feet=True,
                                                    to_mph=True,
                                                    to_mps=False,
                                                    anti_aliasing=100,
                                                    temperature_color='red',
                                                    temperature_comparison_color='blue',
                                                    temperature_alpha=1,
                                                    temperature_comparison_alpha=1,
                                                    relative_humidity_color='darkgreen',
                                                    relative_humidity_comparison_color='darkorange',
                                                    relative_humidity_alpha=1,
                                                    relative_humidity_comparison_alpha=1,
                                                    wind_color='red',
                                                    wind_comparison_color='blue',
                                                    wind_barb_length=5,
                                                    wind_barb_comparison_length=5,
                                                    wind_barb_alpha=1,
                                                    wind_barb_comparison_alpha=1,
                                                    y_bottom=0,
                                                    y_top=10000,
                                                    fig_x=15,
                                                    fig_y=8,
                                                    signature_box_x=0.85,
                                                    signature_box_y=-0.15,
                                                    signature_box_style='round',
                                                    signature_box_color='steelblue',
                                                    signature_box_alpha=0.5,
                                                    signature_fontsize=8,
                                                    signature_fontcolor='black',
                                                    x_title_position=0.015,
                                                    title_1_fontsize=14,
                                                    title_1_box_style='round',
                                                    title_1_box_color='steelblue',
                                                    title_1_box_alpha=0.5,
                                                    title_1_fontcolor='black',
                                                    title_2_fontsize=12,
                                                    title_2_box_style='round',
                                                    title_2_box_color='crimson',
                                                    title_2_box_alpha=0.5,
                                                    title_2_fontcolor='black',
                                                    title_2_y_position=1,
                                                    title_3_fontsize=12,
                                                    title_3_box_style='round',
                                                    title_3_box_color='lime',
                                                    title_3_box_alpha=0.5,
                                                    title_3_fontcolor='black',
                                                    title_3_y_position=1,
                                                    title_4_fontsize=12,
                                                    title_4_box_style='round',
                                                    title_4_box_color='orange',
                                                    title_4_box_alpha=0.5,
                                                    title_4_fontcolor='black',
                                                    title_4_y_position=1,
                                                    x_axis1_box_style='round',
                                                    x_axis1_box_color='crimson',
                                                    x_axis1_box_alpha=0.5,
                                                    x_axis2_box_style='round',
                                                    x_axis2_box_color='lime',
                                                    x_axis2_box_alpha=0.5,
                                                    x_axis3_box_style='round',
                                                    x_axis3_box_color='orange',
                                                    x_axis3_box_alpha=0.5,
                                                    x_axis_label_fontsize=12,
                                                    y_axis_label_fontsize=12,
                                                    axes_label_color='black',
                                                    xtick_color='black',
                                                    ytick_color='black',
                                                    facecolor='lavender',
                                                    df=None,
                                                    df_comp=None,
                                                    date=None,
                                                    date_comp=None,
                                                    subplot_background_color='silver',
                                                    barb_legend_x_position=0,
                                                    barb_legend_y_position=0,
                                                    barb_legend_fontsize=10,
                                                    barb_legend_zorder=10):***

    This function plots an observed temperature/relative humidity/wind profile comparison from 2 different atmospheric soundings.
    
    Required Arguments:
    
    1) station_id (String) - The station ID for the sounding site.
    
    Optional Arguments:
    
    1) current (Boolean) - Default=True. When set to True, the function defaults to the latest sounding. Set to False
        when plotting past soundings.
        
    2) custom_time_1 (String) - Default=None. When plotting archived sounding data, specify the first custom time as a string in the
        form of 'YYYY-mm-dd:HH'.
        
    3) custom_time_2 (String) - Default=None. When plotting archived sounding data, specify the second custom time as a string in the
        form of 'YYYY-mm-dd:HH'.
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    5) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    6) path (String) - Default='FireWxPy Graphics/Observations/Upper Air/Temperature Relative Humidity Wind Profiles Comparison'. The path where
        the graphic will save.
        
    7) to_fahrenheit (Boolean) - Default=False. Set to True for temperature in Fahrenheit.
    
    8) to_kelvin (Boolean) - Default=False. Set to True for temperature in Kelvin.
    
    9) to_meters (Boolean) - Default=False. Set to True for height in meters.
    
    10) to_feet (Boolean) - Default=True. Set to True for height in feet.
    
    11) to_mph (Boolean) - Default=True. Set to True for wind speed in miles per hour. 
    
    12) to_mps (Boolean) - Default=False. Set to True for wind speed in meters per second.
    
    13) anti_aliasing (Integer) - Default=100. This is the amount of data points interpolated between observed data points.
        The higher the number the more interpolated data points. This is for those who want to have a colormapped profile that
        appears as a line but is a series of colormapped scatter points.
        
    14) temperature_color (String) - Default='red'. The color for the temperature line corresponding to custom_time_1. 
    
    15) temperature_color_comparison (String) - Default='blue'. The color for the temperature line corresponding to custom_time_2. 
    
    16) temperature_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    17) relative_humidity_color (String) - Default='darkgreen'. The color for the relative humidity line corresponding to custom_time_1. 
    
    18) relative_humidity_color_comparison (String) - Default='darkorange'. The color for the relative humidity line corresponding to custom_time_2. 
    
    19) relative_humidity_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    20) wind_color (String) - Default='red'. The color for the wind line and wind barbs corresponding to custom_time_1.
    
    21) wind_color_comparison (String) - Default='blue'. The color for the wind line and wind barbs corresponding to custom_time_2.
    
    22) wind_barb_length (Integer) - Default=5. The length of the wind barb.
    
    23) wind_barb_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    24) y_bottom (Integer) - Default=0. The height in feet where the y-axis begins.
    
    25) y_top (Integer) - Default=10000. The height in feet where the y-axis ends.     
    
    26) fig_x (Integer) - Default=15. The x-length of the figure.
    
    27) fig_y (Integer) - Default=8. The y-length of the figure.
    
    28) signature_box_x (Float) - Default=0.85. The x-position of the signature text box with respect to the figure axis.
    
    29) signature_box_y (Float) - Default=-0.15. The y-position of the signature text box with respect to the figure axis.                              

    30) signature_box_style (String) - Default='round'. The style of the text box. 
    
    31) signature_box_color (String) - Default='steelblue'. The color of the text box.
    
    32) signature_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    33) signature_fontsize (Integer) - Default=8. Font size of the font in the textbox. 
    
    34) signature_fontcolor (String) - Default='black'. Font color of the font in the textbox. 
    
    35) x_title_position (Float) - Default=0.015. The x-position for all titles with respect to the figure axis.
    
    36) title_1_fontsize (Integer) - Default=14. Font size of the figure title.
    
    37) title_1_box_style (String) - Default='round'. Text box style of the figure title textbox.
    
    38) title_1_box_color (String) - Default='steelblue'. The color of the text box of the figure title.
    
    39) title_1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    40) title_1_fontcolor (String) - Default='black'. Font color of the first subplot title.
    
    41) title_2_fontsize (Integer) - Default=12. Font size of the first subplot title.
    
    42) title_2_box_style (String) - Default='round'. Text box style of the first subplot text box.
    
    43) title_2_box_color (String) - Default='crimson'. Text box color of the first subplot text box.
    
    44) title_2_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    45) title_2_fontcolor (String) - Default='black'. Font color of the first subplot title.
    
    46) title_2_y_position (Float or Integer) - Default=1. The y-axis positon of the second subplot text box.
    
    47) title_3_fontsize (Integer) - Default=12. Font size of the second subplot title.
    
    48) title_3_box_style (String) - Default='round'. Text box style of the second subplot text box.
    
    49) title_3_box_color (String) - Default='crimson'. Text box color of the second subplot text box.
    
    50) title_3_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    51) title_3_fontcolor (String) - Default='black'. Font color of the second subplot title.
    
    52) title_3_y_position (Float or Integer) - Default=1. The y-axis positon of the second subplot text box.
    
    53) title_4_fontsize (Integer) - Default=12. Font size of the third subplot title.
    
    54) title_4_box_style (String) - Default='round'. Text box style of the third subplot text box.
    
    55) title_4_box_color (String) - Default='crimson'. Text box color of the third subplot text box.
    
    56) title_4_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    57) title_4_fontcolor (String) - Default='black'. Font color of the third subplot title.
    
    58) title_4_y_position (Float or Integer) - Default=1. The y-axis positon of the third subplot text box.
    
    59) x_axis1_box_style (String) - Default='round'. Text box style of the first subplot x-axis text box.
    
    60) x_axis1_box_color (String) - Default='crimson'. Text box color of the first subplot x-axis text box.
    
    61) x_axis1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    62) x_axis2_box_style (String) - Default='round'. Text box style of the second subplot x-axis text box.
    
    63) x_axis2_box_color (String) - Default='crimson'. Text box color of the second subplot x-axis text box.
    
    64) x_axis2_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque.  
        
    65) x_axis3_box_style (String) - Default='round'. Text box style of the third subplot x-axis text box.
    
    66) x_axis3_box_color (String) - Default='crimson'. Text box color of the third subplot x-axis text box.
    
    67) x_axis3_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque.  
    
    68) x_axis_label_fontsize (Integer) - Default=12. Font size of x-axis labels.
    
    69) y_axis_label_fontsize (Integer) - Default=12. Font size of y-axis labels.
    
    70) axes_label_color (String) - Default='black'. The color of the labels on each axis.
    
    71) xtick_color (String) - Default='black'. The color of the x-ticks.
    
    72) ytick_color (String) - Default='black'. The color of the y-ticks.                                                

    73) facecolor (String) - Default='lavander'. The face color of the figure.
    
    74) df (Pandas.DataFrame) - Default=None. If the user wishes to download a medley of Pandas.DataFrames with WxData
        and pass those data frames into the plotting function, set df=df. 
        
    75) date (Datetime) - Default=None. The datetime object associated with the Pandas.DataFrame when downloading 
        the data with WxData outside of the function and passing the date into the function. Set date=date if the user
        is not downloading the data within the function.
        
    76) subplot_background_color (String) - Default='silver'. The background color of each subplot axis.
    
    77) barb_legend_x_position (Float or Integer) - Default=0. x-position of wind barb legend with respect to the figure axis.
    
    78) barb_legend_y_position (Float or Integer) - Default=0. y-position of wind barb legend with respect to the figure axis.
    
    79) barb_legend_fontsize (Integer) - Default=10. Font size of wind barb legend. 
    
    80) barb_legend_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
                                                    
    Returns
    -------
    
    A figure of the vertical profiles comparison saved to {path}

#### Temperature/Wind Comparison
***def plot_temperature_wind_profile_comparison(station_id,
                                current=True,
                                custom_time_1=None,
                                custom_time_2=None,
                                proxies=None,
                                clear_recycle_bin=False,
                                path='FireWxPy Graphics/Observations/Upper Air/Temperature Wind Profiles Comparison',
                                to_fahrenheit=True,
                                to_kelvin=False,
                                to_meters=False,
                                to_feet=True,
                                to_mph=True,
                                to_mps=False,
                                anti_aliasing=100,
                                temperature_color='red',
                                temperature_comp_color='blue',
                                temperature_alpha=1,
                                temperature_comp_alpha=1,
                                wind_color='darkorange',
                                wind_comp_color='purple',
                                wind_barb_length=7,
                                wind_comp_barb_length=7,
                                wind_barb_alpha=1,
                                wind_comp_barb_alpha=1,
                                y_bottom=0,
                                y_top=10000,
                                fig_x=15,
                                fig_y=8,
                                signature_box_x=0.25,
                                signature_box_y=-0.15,
                                signature_box_style='round',
                                signature_box_color='steelblue',
                                signature_box_alpha=0.5,
                                signature_fontsize=8,
                                signature_fontcolor='black',
                                title_1_fontsize=14,
                                title_1_box_style='round',
                                title_1_box_color='steelblue',
                                title_1_box_alpha=0.5,
                                title_1_fontcolor='black',
                                title_2_fontsize=12,
                                title_2_box_style='round',
                                title_2_box_color='crimson',
                                title_2_box_alpha=0.5,
                                title_2_fontcolor='black',
                                title_2_y_position=1,
                                x_axis1_box_style='round',
                                x_axis1_box_color='crimson',
                                x_axis1_box_alpha=0.5,
                                stats_text_box_fontcolor='black',
                                stats_text_box_x_position=0.7405,
                                stats_text_box_y_position=0.8495,
                                stats_text_box_style='round',
                                stats_text_box_color='wheat',
                                stats_text_box_alpha=1,
                                x_axis_label_fontsize=12,
                                y_axis_label_fontsize=12,
                                axes_label_color='black',
                                legend_fontsize=6.5,
                                xtick_color='black',
                                ytick_color='black',
                                facecolor='lavender',
                                df=None,
                                df_comp=None,
                                date=None,
                                date_comp=None,
                                subplot_background_color='silver',
                                barb_legend_fontsize=10,
                                barb_legend_x_position=0,
                                barb_legend_y_position=0,
                                barb_legend_zorder=10):***

    This function plots an observed temperature/wind profile comparison from 2 different atmospheric soundings.
    
    Required Arguments:
    
    1) station_id (String) - The station ID for the sounding site.
    
    Optional Arguments:
    
    1) current (Boolean) - Default=True. When set to True, the function defaults to the latest sounding. Set to False
        when plotting past soundings.
        
    2) custom_time_1 (String) - Default=None. When plotting archived sounding data, specify the first custom time as a string in the
        form of 'YYYY-mm-dd:HH'.
        
    3) custom_time_2 (String) - Default=None. When plotting archived sounding data, specify the second custom time as a string in the
        form of 'YYYY-mm-dd:HH'.
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    5) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    6) path (String) - Default='FireWxPy Graphics/Observations/Upper Air/Temperature Wind Profiles Comparison'. The path where
        the graphic will save.
        
    7) to_fahrenheit (Boolean) - Default=False. Set to True for temperature in Fahrenheit.
    
    8) to_kelvin (Boolean) - Default=False. Set to True for temperature in Kelvin.
    
    9) to_meters (Boolean) - Default=False. Set to True for height in meters.
    
    10) to_feet (Boolean) - Default=True. Set to True for height in feet.
    
    11) to_mph (Boolean) - Default=True. Set to True for wind speed in miles per hour. 
    
    12) to_mps (Boolean) - Default=False. Set to True for wind speed in meters per second.
    
    13) anti_aliasing (Integer) - Default=100. This is the amount of data points interpolated between observed data points.
        The higher the number the more interpolated data points. This is for those who want to have a colormapped profile that
        appears as a line but is a series of colormapped scatter points.
        
    14) temperature_color (String) - Default='red'. The color for the temperature line corresponding to custom_time_1. 
    
    15) temperature_color_comparison (String) - Default='blue'. The color for the temperature line corresponding to custom_time_2. 
    
    16) temperature_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    17) wind_color (String) - Default='red'. The color for the wind line and wind barbs corresponding to custom_time_1.
    
    18) wind_color_comparison (String) - Default='blue'. The color for the wind line and wind barbs corresponding to custom_time_2.
    
    19) wind_barb_length (Integer) - Default=5. The length of the wind barb.
    
    20) wind_barb_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    21) y_bottom (Integer) - Default=0. The height in feet where the y-axis begins.
    
    22) y_top (Integer) - Default=10000. The height in feet where the y-axis ends.     
    
    23) fig_x (Integer) - Default=15. The x-length of the figure.
    
    24) fig_y (Integer) - Default=8. The y-length of the figure.
    
    25) signature_box_x (Float) - Default=0.85. The x-position of the signature text box with respect to the figure axis.
    
    26) signature_box_y (Float) - Default=-0.15. The y-position of the signature text box with respect to the figure axis.                              

    27) signature_box_style (String) - Default='round'. The style of the text box. 
    
    28) signature_box_color (String) - Default='steelblue'. The color of the text box.
    
    29) signature_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    30) signature_fontsize (Integer) - Default=8. Font size of the font in the textbox. 
    
    31) signature_fontcolor (String) - Default='black'. Font color of the font in the textbox. 
    
    32) x_title_position (Float) - Default=0.015. The x-position for all titles with respect to the figure axis.
    
    33) title_1_fontsize (Integer) - Default=14. Font size of the figure title.
    
    34) title_1_box_style (String) - Default='round'. Text box style of the figure title textbox.
    
    35) title_1_box_color (String) - Default='steelblue'. The color of the text box of the figure title.
    
    36) title_1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    37) title_1_fontcolor (String) - Default='black'. Font color of the figure title.
    
    38) title_2_fontsize (Integer) - Default=12. Font size of the first subplot title.
    
    39) title_2_box_style (String) - Default='round'. Text box style of the subplot title text box.
    
    40) title_2_box_color (String) - Default='crimson'. Text box color of the subplot title text box.
    
    41) title_2_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    42) title_2_fontcolor (String) - Default='black'. Font color of the subplot title.
    
    43) title_2_y_position (Float or Integer) - Default=1. The y-axis positon of the subplot title text box.
    
    44) x_axis1_box_style (String) - Default='round'. Text box style of the first subplot x-axis text box.
    
    45) x_axis1_box_color (String) - Default='crimson'. Text box color of the first subplot x-axis text box.
    
    46) x_axis1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
    
    47) x_axis1_box_style (String) - Default='round'. Text box style for the general x-axis text box.
    
    48) x_axis1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    49) stats_text_box_fontcolor (String) - Default='black'. Font color of the stats table.
    
    50) stats_text_box_x_position (Float) - Default=0.7405. The x-position of the stats table text box.
    
    51) stats_text_box_y_position (Float) - Default=0.8495. The y-position of the stats table text box.
    
    52) stats_text_box_style (String) - Default='round'. The style of the stats text box.
    
    53) stats_text_box_color (String) - Defaults='wheat'. The color of the stats text box.
    
    54) stats_text_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 

    55) x_axis_label_fontsize (Integer) - Default=12. Font size of x-axis labels.
    
    56) y_axis_label_fontsize (Integer) - Default=12. Font size of y-axis labels.
    
    57) axes_label_color (String) - Default='black'. The color of the labels on each axis.
    
    58) xtick_color (String) - Default='black'. The color of the x-ticks.
    
    59) ytick_color (String) - Default='black'. The color of the y-ticks.                                                

    60) facecolor (String) - Default='lavander'. The face color of the figure.
    
    61) df (Pandas.DataFrame) - Default=None. If the user wishes to download a medley of Pandas.DataFrames with WxData
        and pass those data frames into the plotting function, set df=df. 
        
    62) date (Datetime) - Default=None. The datetime object associated with the Pandas.DataFrame when downloading 
        the data with WxData outside of the function and passing the date into the function. Set date=date if the user
        is not downloading the data within the function.
        
    63) subplot_background_color (String) - Default='silver'. The background color of each subplot axis.    
    
    64) barb_legend_x_position (Float or Integer) - Default=0. x-position of wind barb legend with respect to the figure axis.
    
    65) barb_legend_y_position (Float or Integer) - Default=0. y-position of wind barb legend with respect to the figure axis.
    
    66) barb_legend_fontsize (Integer) - Default=10. Font size of wind barb legend. 
    
    67) barb_legend_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.               
                                                    
    Returns
    -------
    
    A figure of the vertical profiles comparison saved to {path}

#### Relative Humidity/Wind Comparison
***def plot_relative_humidity_wind_profile_comparison(station_id,
                                current=True,
                                custom_time_1=None,
                                custom_time_2=None,
                                proxies=None,
                                clear_recycle_bin=False,
                                path='FireWxPy Graphics/Observations/Upper Air/Relative Humidity Wind Profiles Comparison',
                                to_meters=False,
                                to_feet=True,
                                to_mph=True,
                                to_mps=False,
                                anti_aliasing=100,
                                rh_color='red',
                                rh_comp_color='blue',
                                rh_alpha=1,
                                rh_comp_alpha=1,
                                wind_color='darkorange',
                                wind_comp_color='purple',
                                wind_barb_length=7,
                                wind_comp_barb_length=7,
                                wind_barb_alpha=1,
                                wind_comp_barb_alpha=1,
                                y_bottom=0,
                                y_top=10000,
                                fig_x=15,
                                fig_y=8,
                                signature_box_x=0.25,
                                signature_box_y=-0.15,
                                signature_box_style='round',
                                signature_box_color='steelblue',
                                signature_box_alpha=0.5,
                                signature_fontsize=8,
                                signature_fontcolor='black',
                                title_1_fontsize=14,
                                title_1_box_style='round',
                                title_1_box_color='steelblue',
                                title_1_box_alpha=0.5,
                                title_1_fontcolor='black',
                                title_2_fontsize=12,
                                title_2_box_style='round',
                                title_2_box_color='crimson',
                                title_2_box_alpha=0.5,
                                title_2_fontcolor='black',
                                title_2_y_position=1,
                                x_axis1_box_style='round',
                                x_axis1_box_color='crimson',
                                x_axis1_box_alpha=0.5,
                                stats_text_box_fontcolor='black',
                                stats_text_box_x_position=0.7405,
                                stats_text_box_y_position=0.8495,
                                stats_text_box_style='round',
                                stats_text_box_color='wheat',
                                stats_text_box_alpha=1,
                                x_axis_label_fontsize=12,
                                y_axis_label_fontsize=12,
                                axes_label_color='black',
                                legend_fontsize=6.5,
                                xtick_color='black',
                                ytick_color='black',
                                facecolor='lavender',
                                df=None,
                                df_comp=None,
                                date=None,
                                date_comp=None,
                                subplot_background_color='silver',
                                barb_legend_fontsize=10,
                                barb_legend_x_position=0,
                                barb_legend_y_position=0,
                                barb_legend_zorder=10):***

    This function plots an observed relative humidity/wind profile comparison from 2 different atmospheric soundings.
    
    Required Arguments:
    
    1) station_id (String) - The station ID for the sounding site.
    
    Optional Arguments:
    
    1) current (Boolean) - Default=True. When set to True, the function defaults to the latest sounding. Set to False
        when plotting past soundings.
        
    2) custom_time_1 (String) - Default=None. When plotting archived sounding data, specify the first custom time as a string in the
        form of 'YYYY-mm-dd:HH'.
        
    3) custom_time_2 (String) - Default=None. When plotting archived sounding data, specify the second custom time as a string in the
        form of 'YYYY-mm-dd:HH'.
        
    4) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    5) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    6) path (String) - Default='FireWxPy Graphics/Observations/Upper Air/Relative Humidity Wind Profiles Comparison'. The path where
        the graphic will save.
                
    7) to_meters (Boolean) - Default=False. Set to True for height in meters.
    
    8) to_feet (Boolean) - Default=True. Set to True for height in feet.
    
    9) to_mph (Boolean) - Default=True. Set to True for wind speed in miles per hour. 
    
    10) to_mps (Boolean) - Default=False. Set to True for wind speed in meters per second.
    
    11) anti_aliasing (Integer) - Default=100. This is the amount of data points interpolated between observed data points.
        The higher the number the more interpolated data points. This is for those who want to have a colormapped profile that
        appears as a line but is a series of colormapped scatter points.
        
    12) rh_color (String) - Default='red'. The color for the relative humidity line corresponding to custom_time_1. 
    
    13) rh_comp_color (String) - Default='blue'. The color for the relative humidity line corresponding to custom_time_2. 
    
    14) rh_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    15) wind_color (String) - Default='darkorange'. The color for the wind line and wind barbs corresponding to custom_time_1.
    
    16) wind_color_comparison (String) - Default='purple'. The color for the wind line and wind barbs corresponding to custom_time_2.
    
    17) wind_barb_length (Integer) - Default=5. The length of the wind barb.
    
    18) wind_barb_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
        0 = Completely Transparent, 1 = Completely Opaque.
        
    19) y_bottom (Integer) - Default=0. The height in feet where the y-axis begins.
    
    20) y_top (Integer) - Default=10000. The height in feet where the y-axis ends.     
    
    21) fig_x (Integer) - Default=15. The x-length of the figure.
    
    22) fig_y (Integer) - Default=8. The y-length of the figure.
    
    23) signature_box_x (Float) - Default=0.85. The x-position of the signature text box with respect to the figure axis.
    
    24) signature_box_y (Float) - Default=-0.15. The y-position of the signature text box with respect to the figure axis.                              

    25) signature_box_style (String) - Default='round'. The style of the text box. 
    
    26) signature_box_color (String) - Default='steelblue'. The color of the text box.
    
    27) signature_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    28) signature_fontsize (Integer) - Default=8. Font size of the font in the textbox. 
    
    29) signature_fontcolor (String) - Default='black'. Font color of the font in the textbox. 
    
    30) x_title_position (Float) - Default=0.015. The x-position for all titles with respect to the figure axis.
    
    31) title_1_fontsize (Integer) - Default=14. Font size of the figure title.
    
    32) title_1_box_style (String) - Default='round'. Text box style of the figure title textbox.
    
    33) title_1_box_color (String) - Default='steelblue'. The color of the text box of the figure title.
    
    34) title_1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    35) title_1_fontcolor (String) - Default='black'. Font color of the figure title.
    
    36) title_2_fontsize (Integer) - Default=12. Font size of the subplot title.
    
    37) title_2_box_style (String) - Default='round'. Text box style of the subplot title text box.
    
    38) title_2_box_color (String) - Default='lime'. Text box color of the subplot title text box.
    
    39) title_2_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    40) title_2_fontcolor (String) - Default='black'. Font color of the subplot title.
    
    41) title_2_y_position (Float or Integer) - Default=1. The y-axis positon of the subplot text box.
            
    42) x_axis1_box_style (String) - Default='round'. Text box style of the first subplot x-axis text box.
    
    43) x_axis1_box_color (String) - Default='crimson'. Text box color of the first subplot x-axis text box.
    
    44) x_axis1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
    
    45) x_axis1_box_style (String) - Default='round'. Text box style for the general x-axis text box.
    
    46) x_axis1_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 
        
    47) stats_text_box_fontcolor (String) - Default='black'. Font color of the stats table.
    
    48) stats_text_box_x_position (Float) - Default=0.7405. The x-position of the stats table text box.
    
    49) stats_text_box_y_position (Float) - Default=0.8495. The y-position of the stats table text box.
    
    50) stats_text_box_style (String) - Default='round'. The style of the stats text box.
    
    51) stats_text_box_color (String) - Defaults='wheat'. The color of the stats text box.
    
    52) stats_text_box_alpha (Float or Integer) - Default=0.5. A value between 0.5 and 1. 
        0.5 = Most transparency allowed. 1 = Completely opaque. 

    53) x_axis_label_fontsize (Integer) - Default=12. Font size of x-axis labels.
    
    54) y_axis_label_fontsize (Integer) - Default=12. Font size of y-axis labels.
    
    55) axes_label_color (String) - Default='black'. The color of the labels on each axis.
    
    56) xtick_color (String) - Default='black'. The color of the x-ticks.
    
    57) ytick_color (String) - Default='black'. The color of the y-ticks.                                                

    58) facecolor (String) - Default='lavander'. The face color of the figure.
    
    59) df (Pandas.DataFrame) - Default=None. If the user wishes to download a medley of Pandas.DataFrames with WxData
        and pass those data frames into the plotting function, set df=df. 
        
    60) date (Datetime) - Default=None. The datetime object associated with the Pandas.DataFrame when downloading 
        the data with WxData outside of the function and passing the date into the function. Set date=date if the user
        is not downloading the data within the function.
        
    61) subplot_background_color (String) - Default='silver'. The background color of each subplot axis.   
    
    62) barb_legend_x_position (Float or Integer) - Default=0. x-position of wind barb legend with respect to the figure axis.
    
    63) barb_legend_y_position (Float or Integer) - Default=0. y-position of wind barb legend with respect to the figure axis.
    
    64) barb_legend_fontsize (Integer) - Default=10. Font size of wind barb legend. 
    
    65) barb_legend_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.                    
                                                    
    Returns
    -------
    
    A figure of the vertical profiles comparison saved to {path}
