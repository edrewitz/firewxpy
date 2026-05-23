"""
This file hosts the function that plots observed vertical profile graphics.

Data Source: University of Wyoming.

(C) Eric J. Drewitz 2024-2026
"""
import matplotlib.pyplot as _plt
import matplotlib as _mpl
import pandas as _pd
import metpy.calc as _mpcalc
import numpy as _np
import firewxpy.calc.calc as _calc

from metpy.units import units as _units
from matplotlib.ticker import MaxNLocator as _MaxNLocator
from wxdata import(
    get_observed_sounding_data as _get_observed_sounding_data,
    linear_anti_aliasing as _linear_anti_aliasing
)
from firewxpy.utils.standard import(
    plot_creation_time as _plot_creation_time,
    get_timezone_abbreviation as _get_timezone_abbreviation
)

from firewxpy.utils.directory import build_directory_branch as _build_directory_branch

_plt.rcParams["axes.labelweight"] = "bold"
_mpl.rcParams['font.weight'] = 'bold'
_pd.options.mode.copy_on_write = True
_local, _utc = _plot_creation_time()
_timezone = _get_timezone_abbreviation()
    
def plot_temperature_relative_humidity_wind_profile(station_id,
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
                                                    subplot_background_color='silver'):
    

    """
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
    """
    
    _build_directory_branch(path)

    if df == None:
        df, date = _get_observed_sounding_data(station_id, 
                                                current=current, 
                                                custom_time=custom_time, 
                                                comparison_24=False, 
                                                proxies=proxies,
                                                clear_recycle_bin=clear_recycle_bin)
    else:
        df = df
        date = date
        
        
    pressure = df['PRES'].values * _units('hPa')
    
    height = _mpcalc.pressure_to_height_std(pressure)
    
    if to_meters == True and to_feet == False:
        height = _calc.kilometers_to_meters(height)
        height_symbol = f"[M]"

    elif to_feet == True and to_meters == False:
        height = _calc.kilometers_to_meters(height)
        height = _calc.meters_to_feet(height)
        height_symbol = f"[FT]"
    else:
        height = height
        height_symbol = f"[KM]"
    
    df['HGHT'] = height.m
        
    if to_fahrenheit == True and to_kelvin == False:
        df['TEMP'] = _calc.celsius_to_fahrenheit(df['TEMP'])
        temperature_symbol = f"[°F]"
    elif to_kelvin == True and to_fahrenheit == False:
        df['TEMP'] = _calc.celsius_to_kelvin(df['TEMP'])
        temperature_symbol = f"[K]"
    else:
        temperature_symbol = f"[°C]"
        
    if to_mph == True and to_mps == False:
        df['SKNT'] = _calc.knots_to_mph(df['SKNT'])
        ws_symbol = f"[MPH]"
    elif to_mph == False and to_mps == True:
        df['SKNT'] = _calc.knots_to_mps(df['SKNT'])
        ws_symbol = f"[M/S]"
    else:
        ws_symbol = f"[KTS]"
        
    if title_1_box_alpha < 0.5:
        title_1_box_alpha = 0.5
    if title_2_box_alpha < 0.5:
        title_2_box_alpha = 0.5
    if title_3_box_alpha < 0.5:
        title_3_box_alpha = 0.5
    if title_4_box_alpha < 0.5:
        title_4_box_alpha = 0.5
    if signature_box_alpha < 0.5:
        signature_box_alpha = 0.5
    if x_axis1_box_alpha < 0.5:
        x_axis1_box_alpha = 0.5
    if x_axis2_box_alpha < 0.5:
        x_axis2_box_alpha = 0.5
    if x_axis3_box_alpha < 0.5:
        x_axis3_box_alpha = 0.5
    
    title_1_box = dict(boxstyle=title_1_box_style, 
                       facecolor=title_1_box_color, 
                       alpha=title_1_box_alpha) 
    
    title_2_box = dict(boxstyle=title_2_box_style, 
                       facecolor=title_2_box_color, 
                       alpha=title_2_box_alpha) 
    
    title_3_box = dict(boxstyle=title_3_box_style, 
                       facecolor=title_3_box_color, 
                       alpha=title_3_box_alpha) 
    
    title_4_box = dict(boxstyle=title_4_box_style, 
                       facecolor=title_4_box_color, 
                       alpha=title_4_box_alpha)
    
    props = dict(boxstyle=signature_box_style, 
                 facecolor=signature_box_color, 
                 alpha=signature_box_alpha)   
    
    x_axis1_box = dict(boxstyle=x_axis1_box_style, 
                 facecolor=x_axis1_box_color, 
                 alpha=x_axis1_box_alpha)  
    
    x_axis2_box = dict(boxstyle=x_axis2_box_style, 
                 facecolor=x_axis2_box_color, 
                 alpha=x_axis2_box_alpha) 
    
    x_axis3_box = dict(boxstyle=x_axis3_box_style, 
                 facecolor=x_axis3_box_color, 
                 alpha=x_axis3_box_alpha) 
    
    _mpl.rcParams['axes.labelcolor'] = axes_label_color
    _mpl.rcParams['xtick.color'] = xtick_color     
    _mpl.rcParams['ytick.color'] = ytick_color
    
    mask = (df['HGHT'] <= y_top) & (df['HGHT'] >= y_bottom) 
    
    df['HGHT']
    
    temp_x, temp_y = _linear_anti_aliasing(df['TEMP'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
    
    rh_x, rh_y = _linear_anti_aliasing(df['RH'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
    
    ws_x, ws_y = _linear_anti_aliasing(df['SKNT'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
        
    fig = _plt.figure(figsize=(fig_x, fig_y))
    fig.patch.set_facecolor(facecolor)

    fig.suptitle(f"{station_id.upper()} VERTICAL PROFILE" 
                 f" | VALID: {date.strftime('%m/%d/%Y %H:00 UTC')}",
                 fontsize=title_1_fontsize,
                 fontweight='bold',
                 color=title_1_fontcolor,
                 bbox=title_1_box)
    
    ax1 = fig.add_subplot(1,3,1)
    ax1.set_facecolor(subplot_background_color)
    ax1.xaxis.set_major_locator(_MaxNLocator(integer=True))
    ax1.yaxis.set_major_locator(_MaxNLocator(integer=True))
    
    ax1.set_xlim((_np.nanmin(df['TEMP'][mask]) - 5), (_np.nanmax(df['TEMP'][mask]) + 5))
    ax1.set_ylim(y_bottom, y_top)
    
    ax1.set_xlabel(f"TEMPERATURE {temperature_symbol}", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis1_box)
    
    ax1.set_ylabel(f"HEIGHT {height_symbol}", 
                       fontsize=y_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=title_1_box)
    
    ax1.set_title(f"TEMPERATURE",
                  fontweight='bold',
                  loc='left',
                  x=x_title_position,
                  fontsize=title_2_fontsize,
                  color=title_2_fontcolor,
                  bbox=title_2_box,
                  y=title_2_y_position)
    
    ax1.scatter(temp_x, 
                temp_y,
                c=temp_x,
                vmin=_np.nanmin(df['TEMP'][mask]),
                vmax=_np.nanmax(df['TEMP'][mask]),
                cmap=temperature_colormap,
                alpha=temperature_alpha)
    
    ax1.text(signature_box_x, 
             signature_box_y, 
             f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024-{_utc.strftime('%Y')} "
             f"| Data Source: weather.uwyo.edu\n"
             f"                      Image Created: {_local.strftime(f'%m/%d/%Y %H:00 {_timezone}')} - {_utc.strftime(f'%m/%d/%Y %H:00 UTC')}", 
             fontsize=signature_fontsize, 
             bbox=props, 
             fontweight='bold', 
             color=signature_fontcolor,
             transform=ax1.transAxes)

    
    ax2 = fig.add_subplot(1,3,2)
    ax2.set_facecolor(subplot_background_color)
    ax2.xaxis.set_major_locator(_MaxNLocator(integer=True))
    ax2.yaxis.set_major_locator(_MaxNLocator(integer=True))

    ax2.set_xlim(0, 100)
    ax2.set_ylim(y_bottom, y_top)
    ax2.set_title(f"RELATIVE HUMIDITY",
                  fontweight='bold',
                  loc='left',
                  x=x_title_position,
                  fontsize=title_3_fontsize,
                  color=title_3_fontcolor,
                  bbox=title_3_box,
                  y=title_3_y_position)
    
    ax2.scatter(rh_x, 
                rh_y,
                c=rh_x,
                vmin=_np.nanmin(df['RH'][mask]),
                vmax=_np.nanmax(df['RH'][mask]),
                cmap=relative_humidity_colormap,
                alpha=relative_humidity_alpha)
    
    ax2.set_xlabel(f"RELATIVE HUMIDITY [%]", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis2_box)
    
    
    ax3 = fig.add_subplot(1,3,3)
    ax3.set_facecolor(subplot_background_color)
    ax3.xaxis.set_major_locator(_MaxNLocator(integer=True))
    ax3.yaxis.set_major_locator(_MaxNLocator(integer=True))
    
    ax3.set_xlim((_np.nanmin(df['SKNT'][mask]) - 5), (_np.nanmax(df['SKNT'][mask]) + 5))
    ax3.set_ylim(y_bottom, y_top)
    ax3.set_title(f"WIND SPEED",
                  fontweight='bold',
                  loc='left',
                  x=x_title_position,
                  fontsize=title_4_fontsize,
                  color=title_4_fontcolor,
                  bbox=title_4_box,
                  y=title_4_y_position)
    
    ax3.scatter(ws_x, 
                ws_y,
                c=ws_x,
                vmin=_np.nanmin(df['SKNT'][mask]),
                vmax=_np.nanmax(df['SKNT'][mask]),
                cmap=wind_colormap)
    
    x_positions = []
    x_position = (_np.nanmin(df['SKNT'][mask]) + _np.nanmax(df['SKNT'][mask]))/2
    for i in range(0, len(df['HGHT'][mask]), 1):
        x_positions.append(x_position)
    
    x_position = _np.asarray(x_positions) 
    
    
    ax3.barbs(x_position,
              df['HGHT'][mask],
              df['U-WIND'][mask],
              df['V-WIND'][mask],
              df['SKNT'][mask],
              cmap=wind_colormap,
              length=wind_barb_length,
              alpha=wind_barb_alpha)
    
    ax3.set_xlabel(f"WIND SPEED {ws_symbol}", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis3_box)
    
    fig.savefig(f"{path}/{station_id.upper()}.png", 
                bbox_inches='tight')
    
    _plt.close(fig)
    
    print(f"Saved {station_id.upper()}.png profiles to {path}.")
    
    
def plot_temperature_wind_profile(station_id,
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
                                subplot_background_color='silver'):
    

    """
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
    """
    
    _build_directory_branch(path)

    if df == None:
        df, date = _get_observed_sounding_data(station_id, 
                                                current=current, 
                                                custom_time=custom_time, 
                                                comparison_24=False, 
                                                proxies=proxies,
                                                clear_recycle_bin=clear_recycle_bin)
    else:
        df = df
        date = date
        
        
    pressure = df['PRES'].values * _units('hPa')
    
    height = _mpcalc.pressure_to_height_std(pressure)
    
    if to_meters == True and to_feet == False:
        height = _calc.kilometers_to_meters(height)
        height_symbol = f"[M]"

    elif to_feet == True and to_meters == False:
        height = _calc.kilometers_to_meters(height)
        height = _calc.meters_to_feet(height)
        height_symbol = f"[FT]"
    else:
        height = height
        height_symbol = f"[KM]"
    
    df['HGHT'] = height.m
        
    if to_fahrenheit == True and to_kelvin == False:
        df['TEMP'] = _calc.celsius_to_fahrenheit(df['TEMP'])
        temperature_symbol = f"[°F]"
    elif to_kelvin == True and to_fahrenheit == False:
        df['TEMP'] = _calc.celsius_to_kelvin(df['TEMP'])
        temperature_symbol = f"[K]"
    else:
        temperature_symbol = f"[°C]"
        
    if to_mph == True and to_mps == False:
        df['SKNT'] = _calc.knots_to_mph(df['SKNT'])
        ws_symbol = f"[MPH]"
    elif to_mph == False and to_mps == True:
        df['SKNT'] = _calc.knots_to_mps(df['SKNT'])
        ws_symbol = f"[M/S]"
    else:
        ws_symbol = f"[KTS]"
        
    if title_1_box_alpha < 0.5:
        title_1_box_alpha = 0.5
    if title_2_box_alpha < 0.5:
        title_2_box_alpha = 0.5
    if max_temperature_text_box_alpha < 0.5:
        max_temperature_text_box_alpha = 0.5
    if min_temperature_text_box_alpha < 0.5:
        min_temperature_text_box_alpha = 0.5
    if signature_box_alpha < 0.5:
        signature_box_alpha = 0.5
    if x_axis1_box_alpha < 0.5:
        x_axis1_box_alpha = 0.5
    if max_wind_text_box_alpha < 0.5:
        max_wind_text_box_alpha = 0.5
    
    title_1_box = dict(boxstyle=title_1_box_style, 
                       facecolor=title_1_box_color, 
                       alpha=title_1_box_alpha) 
    
    title_2_box = dict(boxstyle=title_2_box_style, 
                       facecolor=title_2_box_color, 
                       alpha=title_2_box_alpha) 
    
    maxt_box = dict(boxstyle=max_temperature_text_box_style, 
                       facecolor=max_temperature_text_box_color, 
                       alpha=max_temperature_text_box_alpha) 
    
    mint_box = dict(boxstyle=min_temperature_text_box_style, 
                       facecolor=min_temperature_text_box_color, 
                       alpha=min_temperature_text_box_alpha) 
    
    maxws_box = dict(boxstyle=max_wind_text_box_style, 
                       facecolor=max_wind_text_box_color, 
                       alpha=max_wind_text_box_alpha) 
    
    props = dict(boxstyle=signature_box_style, 
                 facecolor=signature_box_color, 
                 alpha=signature_box_alpha)   
    
    x_axis1_box = dict(boxstyle=x_axis1_box_style, 
                 facecolor=x_axis1_box_color, 
                 alpha=x_axis1_box_alpha)  
    
    _mpl.rcParams['axes.labelcolor'] = axes_label_color
    _mpl.rcParams['xtick.color'] = xtick_color     
    _mpl.rcParams['ytick.color'] = ytick_color
    
    mask = (df['HGHT'] <= y_top) & (df['HGHT'] >= y_bottom) 
    
    temp_x, temp_y = _linear_anti_aliasing(df['TEMP'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
    
    min_t_height = _np.nanmax(_np.where(df['TEMP'][mask] == _np.nanmin(df['TEMP'][mask]), 
                                         df['HGHT'][mask], 
                                         0))  
    
    max_t_height = _np.nanmax(_np.where(df['TEMP'][mask] == _np.nanmax(df['TEMP'][mask]), 
                                         df['HGHT'][mask], 
                                         0)) 
    
    max_ws_height = _np.nanmax(_np.where(df['SKNT'][mask] == _np.nanmax(df['SKNT'][mask]), 
                                         df['HGHT'][mask], 
                                         0)) 
        
    fig = _plt.figure(figsize=(fig_x, fig_y))
    fig.patch.set_facecolor(facecolor)

    fig.suptitle(f"{station_id.upper()} VERTICAL PROFILE" 
                 f" | VALID: {date.strftime('%m/%d/%Y %H:00 UTC')}",
                 fontsize=title_1_fontsize,
                 fontweight='bold',
                 color=title_1_fontcolor,
                 bbox=title_1_box)
    
    ax = fig.add_subplot(1,1,1)
    ax.set_facecolor(subplot_background_color)
    ax.xaxis.set_major_locator(_MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(_MaxNLocator(integer=True))
    
    ax.set_xlim((_np.nanmin(df['TEMP'][mask]) - 5), (_np.nanmax(df['TEMP'][mask]) + 5))
    ax.set_ylim(y_bottom, y_top)
    
    ax.set_xlabel(f"TEMPERATURE {temperature_symbol}", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis1_box)
    
    ax.set_ylabel(f"HEIGHT {height_symbol}", 
                       fontsize=y_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=title_1_box)
    
    ax.set_title(f"TEMPERATURE {temperature_symbol} & WIND SPEED {ws_symbol}",
                  fontweight='bold',
                  loc='center',
                  fontsize=title_2_fontsize,
                  color=title_2_fontcolor,
                  bbox=title_2_box,
                  y=title_2_y_position)
    
    ax.scatter(temp_x, 
                temp_y,
                c=temp_x,
                vmin=_np.nanmin(df['TEMP'][mask]),
                vmax=_np.nanmax(df['TEMP'][mask]),
                cmap=temperature_colormap,
                alpha=temperature_alpha)
    
    ax.text(signature_box_x, 
             signature_box_y, 
             f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024-{_utc.strftime('%Y')} "
             f"| Data Source: weather.uwyo.edu\n"
             f"                      Image Created: {_local.strftime(f'%m/%d/%Y %H:00 {_timezone}')} - {_utc.strftime(f'%m/%d/%Y %H:00 UTC')}", 
             fontsize=signature_fontsize, 
             bbox=props, 
             fontweight='bold', 
             color=signature_fontcolor,
             transform=ax.transAxes)
    
    ax.text(max_temperature_text_box_x_position,
            max_temperature_text_box_y_position,
            f"MAX T: {int(round(_np.nanmax(df['TEMP'][mask]), 0))} {temperature_symbol} @ {int(round(max_t_height, 0))} {height_symbol}",
            fontsize=legend_fontsize,
            bbox=maxt_box,
            fontweight='bold',
            color=title_3_fontcolor,
            transform=ax.transAxes)
    
    ax.text(min_temperature_text_box_x_position,
            min_temperature_text_box_y_position,
            f"MIN T: {int(round(_np.nanmin(df['TEMP'][mask]), 0))} {temperature_symbol} @ {int(round(min_t_height, 0))} {height_symbol}",
            fontsize=legend_fontsize,
            bbox=mint_box,
            fontweight='bold',
            color=title_3_fontcolor,
            transform=ax.transAxes)
    
    ax.text(max_wind_text_box_x_position,
            max_wind_text_box_y_position,
            f"MAX WIND: {int(round(_np.nanmax(df['SKNT'][mask]), 0))} {ws_symbol} @ {int(round(max_ws_height, 0))} {height_symbol}",
            fontsize=legend_fontsize,
            bbox=maxws_box,
            fontweight='bold',
            color=title_3_fontcolor,
            transform=ax.transAxes)

    x_positions = []
    x_position = (_np.nanmin(df['TEMP'][mask]) + _np.nanmax(df['TEMP'][mask]))/2
    for i in range(0, len(df['HGHT'][mask]), 1):
        x_positions.append(x_position)
    
    x_position = _np.asarray(x_positions) 

    ax.barbs(x_position,
                df['HGHT'][mask],
                df['U-WIND'][mask],
                df['V-WIND'][mask],
                df['SKNT'][mask],
                cmap=wind_colormap,
                length=wind_barb_length,
                alpha=wind_barb_alpha)
    
    fig.savefig(f"{path}/{station_id.upper()}.png", 
                bbox_inches='tight')
    
    _plt.close(fig)
    
    print(f"Saved {station_id.upper()}.png profiles to {path}.")
    
    
def plot_relative_humidity_wind_profile(station_id,
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
                                        subplot_background_color='silver'):
    

    """
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
    """
    
    _build_directory_branch(path)

    if df == None:
        df, date = _get_observed_sounding_data(station_id, 
                                                current=current, 
                                                custom_time=custom_time, 
                                                comparison_24=False, 
                                                proxies=proxies,
                                                clear_recycle_bin=clear_recycle_bin)
    else:
        df = df
        date = date
        
        
    pressure = df['PRES'].values * _units('hPa')
    
    height = _mpcalc.pressure_to_height_std(pressure)
    
    if to_meters == True and to_feet == False:
        height = _calc.kilometers_to_meters(height)
        height_symbol = f"[M]"

    elif to_feet == True and to_meters == False:
        height = _calc.kilometers_to_meters(height)
        height = _calc.meters_to_feet(height)
        height_symbol = f"[FT]"
    else:
        height = height
        height_symbol = f"[KM]"
    
    df['HGHT'] = height.m
        
    if to_mph == True and to_mps == False:
        df['SKNT'] = _calc.knots_to_mph(df['SKNT'])
        ws_symbol = f"[MPH]"
    elif to_mph == False and to_mps == True:
        df['SKNT'] = _calc.knots_to_mps(df['SKNT'])
        ws_symbol = f"[M/S]"
    else:
        ws_symbol = f"[KTS]"
        
    if title_1_box_alpha < 0.5:
        title_1_box_alpha = 0.5
    if title_2_box_alpha < 0.5:
        title_2_box_alpha = 0.5
    if signature_box_alpha < 0.5:
        signature_box_alpha = 0.5
    if x_axis1_box_alpha < 0.5:
        x_axis1_box_alpha = 0.5
    if min_rh_height_box_alpha < 0.5:
        min_rh_height_box_alpha = 0.5
    if max_rh_height_box_alpha < 0.5:
        max_rh_height_box_alpha = 0.5
    if rh_range_height_box_alpha < 0.5:
        rh_range_height_box_alpha = 0.5
    if max_wind_height_box_alpha < 0.5:
        max_wind_height_box_alpha = 0.5

    title_1_box = dict(boxstyle=title_1_box_style, 
                       facecolor=title_1_box_color, 
                       alpha=title_1_box_alpha) 
    
    title_2_box = dict(boxstyle=title_2_box_style, 
                       facecolor=title_2_box_color, 
                       alpha=title_2_box_alpha) 
    
    props = dict(boxstyle=signature_box_style, 
                 facecolor=signature_box_color, 
                 alpha=signature_box_alpha)   
    
    x_axis1_box = dict(boxstyle=x_axis1_box_style, 
                 facecolor=x_axis1_box_color, 
                 alpha=x_axis1_box_alpha) 
    
    min_rh_height_box = dict(boxstyle=min_rh_height_box_style, 
                             facecolor=min_rh_height_box_color, 
                             alpha=min_rh_height_box_alpha) 
    
    max_rh_height_box = dict(boxstyle=max_rh_height_box_style, 
                             facecolor=max_rh_height_box_color, 
                             alpha=max_rh_height_box_alpha) 
    
    rh_range_height_box = dict(boxstyle=rh_range_height_box_style, 
                             facecolor=rh_range_height_box_color, 
                             alpha=rh_range_height_box_alpha) 
    
    max_wind_height_box = dict(boxstyle=max_wind_height_box_style, 
                             facecolor=max_wind_height_box_color, 
                             alpha=max_wind_height_box_alpha) 
    
    _mpl.rcParams['axes.labelcolor'] = axes_label_color
    _mpl.rcParams['xtick.color'] = xtick_color     
    _mpl.rcParams['ytick.color'] = ytick_color
    
    mask = (df['HGHT'] <= y_top) & (df['HGHT'] >= y_bottom) 
    
    rh_x, rh_y = _linear_anti_aliasing(df['RH'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
    
    
    min_rh_height = _np.nanmax(_np.where(df['RH'][mask] == _np.nanmin(df['RH'][mask]), 
                                         df['HGHT'][mask], 
                                         0))  
    
    max_rh_height = _np.nanmax(_np.where(df['RH'][mask] == _np.nanmax(df['RH'][mask]), 
                                         df['HGHT'][mask], 
                                         0)) 
    
    max_ws_height = _np.nanmax(_np.where(df['SKNT'][mask] == _np.nanmax(df['SKNT'][mask]), 
                                         df['HGHT'][mask], 
                                         0)) 
        
    fig = _plt.figure(figsize=(fig_x, fig_y))
    fig.patch.set_facecolor(facecolor)

    fig.suptitle(f"{station_id.upper()} VERTICAL PROFILE" 
                 f" | VALID: {date.strftime('%m/%d/%Y %H:00 UTC')}",
                 fontsize=title_1_fontsize,
                 fontweight='bold',
                 color=title_1_fontcolor,
                 bbox=title_1_box)

    
    ax = fig.add_subplot(1,1,1)
    ax.set_facecolor(subplot_background_color)
    ax.xaxis.set_major_locator(_MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(_MaxNLocator(integer=True))
    
    ax.text(signature_box_x, 
             signature_box_y, 
             f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024-{_utc.strftime('%Y')} "
             f"| Data Source: weather.uwyo.edu\n"
             f"                      Image Created: {_local.strftime(f'%m/%d/%Y %H:00 {_timezone}')} - {_utc.strftime(f'%m/%d/%Y %H:00 UTC')}", 
             fontsize=signature_fontsize, 
             bbox=props, 
             fontweight='bold', 
             color=signature_fontcolor,
             transform=ax.transAxes)

    ax.set_xlim((_np.nanmin(df['RH'][mask]) -5 ), (_np.nanmax(df['RH'][mask]) + 5))
    ax.set_ylim(y_bottom, y_top)
    ax.set_title(f"RELATIVE HUMIDITY & WIND SPEED {ws_symbol}",
                  fontweight='bold',
                  loc='center',
                  fontsize=title_2_fontsize,
                  color=title_2_fontcolor,
                  bbox=title_2_box,
                  y=title_2_y_position)
    
    ax.text(max_rh_height_box_x_position,
            max_rh_height_box_y_position,
            f"RH MAX = {int(round(_np.nanmax(df['RH'][mask]), 0))} [%] @ {int(round(max_rh_height, 0))} {height_symbol}",
            fontweight='bold',
            fontsize=legend_fontsize,
            color=title_2_fontcolor,
            bbox=max_rh_height_box,
            transform=ax.transAxes)
    
    ax.text(min_rh_height_box_x_position,
            min_rh_height_box_y_position,
            f"RH MIN = {int(round(_np.nanmin(df['RH'][mask]), 0))} [%] @ {int(round(min_rh_height, 0))} {height_symbol}",
            fontweight='bold',
            fontsize=legend_fontsize,
            color=title_2_fontcolor,
            bbox=min_rh_height_box,
            transform=ax.transAxes)
    
    ax.text(rh_range_height_box_x_position,
            rh_range_height_box_y_position,
            f"RH RANGE = {int(round(_np.nanmax(df['RH'][mask]), 0)) - int(round(_np.nanmin(df['RH'][mask]), 0))} [%]",
            fontweight='bold',
            fontsize=legend_fontsize,
            color=title_2_fontcolor,
            bbox=rh_range_height_box,
            transform=ax.transAxes)
    
    ax.text(max_wind_height_box_x_position,
            max_wind_height_box_y_position,
            f"WIND SPEED MAX = {int(round(_np.nanmax(df['SKNT'][mask]), 0))} {ws_symbol} @ {int(round(max_ws_height, 0))} {height_symbol}",
            fontweight='bold',
            fontsize=legend_fontsize,
            color=title_2_fontcolor,
            bbox=max_wind_height_box,
            transform=ax.transAxes)
    
    ax.scatter(rh_x, 
                rh_y,
                c=rh_x,
                vmin=_np.nanmin(df['RH'][mask]),
                vmax=_np.nanmax(df['RH'][mask]),
                cmap=relative_humidity_colormap,
                alpha=relative_humidity_alpha)
    
    ax.set_xlabel(f"RELATIVE HUMIDITY [%]", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis1_box)
    
    ax.set_ylabel(f"HEIGHT {height_symbol}", 
                       fontsize=y_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=title_1_box)
    
    x_positions = []
    x_position = (_np.nanmin(df['RH'][mask]) + _np.nanmax(df['RH'][mask]))/2
    for i in range(0, len(df['HGHT'][mask]), 1):
        x_positions.append(x_position)
    
    x_position = _np.asarray(x_positions) 

    ax.barbs(x_position,
                df['HGHT'][mask],
                df['U-WIND'][mask],
                df['V-WIND'][mask],
                df['SKNT'][mask],
                cmap=wind_colormap,
                length=wind_barb_length,
                alpha=wind_barb_alpha)
    
    fig.savefig(f"{path}/{station_id.upper()}.png", 
                bbox_inches='tight')
    
    _plt.close(fig)
    
    print(f"Saved {station_id.upper()}.png profiles to {path}.")
    
def plot_temperature_relative_humidity_wind_profile_comparison(station_id,
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
                                                    barb_legend_zorder=10):
    

    """
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
    """
    
    _build_directory_branch(path)

    if df == None and current == True:
        df, df_comp, date, date_comp = _get_observed_sounding_data(station_id, 
                                                current=current, 
                                                comparison_24=True, 
                                                proxies=proxies,
                                                clear_recycle_bin=clear_recycle_bin)
    
    elif df == None and current == False:
        df, date = _get_observed_sounding_data(station_id, 
                                            current=current, 
                                            custom_time=custom_time_1,
                                            comparison_24=False, 
                                            proxies=proxies,
                                            clear_recycle_bin=clear_recycle_bin)
        
        df_comp, date_comp = _get_observed_sounding_data(station_id, 
                                            current=current, 
                                            custom_time=custom_time_2,
                                            comparison_24=False, 
                                            proxies=proxies,
                                            clear_recycle_bin=clear_recycle_bin)
    
    else:
        df = df
        df_comp = df_comp
        date = date
        date_comp = date_comp
        
        
    pressure = df['PRES'].values * _units('hPa')
    pressure_comp = df_comp['PRES'].values * _units('hPa')
    
    height = _mpcalc.pressure_to_height_std(pressure)
    height_comp = _mpcalc.pressure_to_height_std(pressure_comp)
    
    if to_meters == True and to_feet == False:
        height = _calc.kilometers_to_meters(height)
        height_comp = _calc.kilometers_to_meters(height_comp)
        height_symbol = f"[M]"

    elif to_feet == True and to_meters == False:
        height = _calc.kilometers_to_meters(height)
        height = _calc.meters_to_feet(height)
        height_comp = _calc.kilometers_to_meters(height_comp)
        height_comp = _calc.meters_to_feet(height_comp)
        height_symbol = f"[FT]"
    else:
        height = height
        height_comp = height_comp
        height_symbol = f"[KM]"
    
    df['HGHT'] = height.m
    df_comp['HGHT'] = height_comp.m
        
    if to_fahrenheit == True and to_kelvin == False:
        df['TEMP'] = _calc.celsius_to_fahrenheit(df['TEMP'])
        df_comp['TEMP'] = _calc.celsius_to_fahrenheit(df_comp['TEMP'])
        temperature_symbol = f"[°F]"
    elif to_kelvin == True and to_fahrenheit == False:
        df['TEMP'] = _calc.celsius_to_kelvin(df['TEMP'])
        df_comp['TEMP'] = _calc.celsius_to_kelvin(df_comp['TEMP'])
        temperature_symbol = f"[K]"
    else:
        temperature_symbol = f"[°C]"
        
    if to_mph == True and to_mps == False:
        df['SKNT'] = _calc.knots_to_mph(df['SKNT'])
        df_comp['SKNT'] = _calc.knots_to_mph(df_comp['SKNT'])
        ws_symbol = f"[MPH]"
    elif to_mph == False and to_mps == True:
        df['SKNT'] = _calc.knots_to_mps(df['SKNT'])
        df_comp['SKNT'] = _calc.knots_to_mps(df_comp['SKNT'])
        ws_symbol = f"[M/S]"
    else:
        ws_symbol = f"[KTS]"
        
    if title_1_box_alpha < 0.5:
        title_1_box_alpha = 0.5
    if title_2_box_alpha < 0.5:
        title_2_box_alpha = 0.5
    if title_3_box_alpha < 0.5:
        title_3_box_alpha = 0.5
    if title_4_box_alpha < 0.5:
        title_4_box_alpha = 0.5
    if signature_box_alpha < 0.5:
        signature_box_alpha = 0.5
    if x_axis1_box_alpha < 0.5:
        x_axis1_box_alpha = 0.5
    if x_axis2_box_alpha < 0.5:
        x_axis2_box_alpha = 0.5
    if x_axis3_box_alpha < 0.5:
        x_axis3_box_alpha = 0.5
    
    title_1_box = dict(boxstyle=title_1_box_style, 
                       facecolor=title_1_box_color, 
                       alpha=title_1_box_alpha) 
    
    title_2_box = dict(boxstyle=title_2_box_style, 
                       facecolor=title_2_box_color, 
                       alpha=title_2_box_alpha) 
    
    title_3_box = dict(boxstyle=title_3_box_style, 
                       facecolor=title_3_box_color, 
                       alpha=title_3_box_alpha) 
    
    title_4_box = dict(boxstyle=title_4_box_style, 
                       facecolor=title_4_box_color, 
                       alpha=title_4_box_alpha)
    
    props = dict(boxstyle=signature_box_style, 
                 facecolor=signature_box_color, 
                 alpha=signature_box_alpha)   
    
    x_axis1_box = dict(boxstyle=x_axis1_box_style, 
                 facecolor=x_axis1_box_color, 
                 alpha=x_axis1_box_alpha)  
    
    x_axis2_box = dict(boxstyle=x_axis2_box_style, 
                 facecolor=x_axis2_box_color, 
                 alpha=x_axis2_box_alpha) 
    
    x_axis3_box = dict(boxstyle=x_axis3_box_style, 
                 facecolor=x_axis3_box_color, 
                 alpha=x_axis3_box_alpha) 
    
    _mpl.rcParams['axes.labelcolor'] = axes_label_color
    _mpl.rcParams['xtick.color'] = xtick_color     
    _mpl.rcParams['ytick.color'] = ytick_color
    
    mask = (df['HGHT'] <= y_top) & (df['HGHT'] >= y_bottom) 
    mask_comp = (df_comp['HGHT'] <= y_top) & (df_comp['HGHT'] >= y_bottom) 
    
    temp_x, temp_y = _linear_anti_aliasing(df['TEMP'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
    
    temp_x_comp, temp_y_comp = _linear_anti_aliasing(df_comp['TEMP'][mask_comp], 
                                                    df_comp['HGHT'][mask_comp], 
                                                    anti_aliasing)
                
    rh_x, rh_y = _linear_anti_aliasing(df['RH'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
    
    rh_x_comp, rh_y_comp = _linear_anti_aliasing(df_comp['RH'][mask_comp], 
                                                df_comp['HGHT'][mask_comp], 
                                                anti_aliasing)
    
    ws_x, ws_y = _linear_anti_aliasing(df['SKNT'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
    
    ws_x_comp, ws_y_comp = _linear_anti_aliasing(df_comp['SKNT'][mask_comp], 
                                         df_comp['HGHT'][mask_comp], 
                                         anti_aliasing)
    
    temp_mins = []
    temp_x_min = (_np.nanmin(df['TEMP'][mask]) - 5)
    temp_comp_x_min = (_np.nanmin(df_comp['TEMP'][mask_comp]) - 5)
    temp_mins.append(temp_x_min)
    temp_mins.append(temp_comp_x_min)
    
    temp_maxs = []
    temp_x_max = (_np.nanmax(df['TEMP'][mask]) + 5)
    temp_comp_x_max = (_np.nanmax(df_comp['TEMP'][mask_comp]) + 5)
    temp_maxs.append(temp_x_max)
    temp_maxs.append(temp_comp_x_max)
    
    ws_mins = []
    ws_x_min = (_np.nanmin(df['SKNT'][mask]))
    ws_comp_x_min = (_np.nanmin(df_comp['SKNT'][mask_comp]))
    ws_mins.append(ws_x_min)
    ws_mins.append(ws_comp_x_min)
    
    ws_maxs = []
    ws_x_max = (_np.nanmax(df['SKNT'][mask]) + 5)
    ws_comp_x_max = (_np.nanmax(df_comp['SKNT'][mask_comp]) + 5)
    ws_maxs.append(ws_x_max)
    ws_maxs.append(ws_comp_x_max)
        
    fig = _plt.figure(figsize=(fig_x, fig_y))
    fig.patch.set_facecolor(facecolor)

    fig.suptitle(f"{station_id.upper()} VERTICAL PROFILE" 
                 f" | TIME 1: {date.strftime('%m/%d/%Y %H:00 UTC')} | TIME 2: {date_comp.strftime('%m/%d/%Y %H:00 UTC')}",
                 fontsize=title_1_fontsize,
                 fontweight='bold',
                 color=title_1_fontcolor,
                 bbox=title_1_box)
    
    ax1 = fig.add_subplot(1,3,1)
    ax1.set_facecolor(subplot_background_color)
    ax1.xaxis.set_major_locator(_MaxNLocator(integer=True))
    ax1.yaxis.set_major_locator(_MaxNLocator(integer=True))
    
    ax1.set_xlim(_np.nanmin(temp_mins), _np.nanmax(temp_maxs))
    ax1.set_ylim(y_bottom, y_top)
    
    ax1.set_xlabel(f"{temperature_symbol}", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis1_box)
    
    ax1.set_ylabel(f"{height_symbol}", 
                       fontsize=y_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=title_1_box)
    
    ax1.set_title(f"TEMPERATURE",
                  fontweight='bold',
                  loc='left',
                  x=x_title_position,
                  fontsize=title_2_fontsize,
                  color=title_2_fontcolor,
                  bbox=title_2_box,
                  y=title_2_y_position)
    
    ax1.scatter(temp_x, 
                temp_y,
                vmin=_np.nanmin(df['TEMP'][mask]),
                vmax=_np.nanmax(df['TEMP'][mask]),
                color=temperature_color,
                alpha=temperature_alpha,
                label=f"{date.strftime('%Y-%m-%d %H:00 UTC')}")
    
    ax1.scatter(temp_x_comp, 
                temp_y_comp,
                vmin=_np.nanmin(df_comp['TEMP'][mask_comp]),
                vmax=_np.nanmax(df_comp['TEMP'][mask_comp]),
                color=temperature_comparison_color,
                alpha=temperature_comparison_alpha,
                label=f"{date_comp.strftime('%Y-%m-%d %H:00 UTC')}")
    
    ax1.text(signature_box_x, 
             signature_box_y, 
             f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024-{_utc.strftime('%Y')} "
             f"| Data Source: weather.uwyo.edu\n"
             f"                      Image Created: {_local.strftime(f'%m/%d/%Y %H:00 {_timezone}')} - {_utc.strftime(f'%m/%d/%Y %H:00 UTC')}", 
             fontsize=signature_fontsize, 
             bbox=props, 
             fontweight='bold', 
             color=signature_fontcolor,
             transform=ax1.transAxes)
    
    leg = ax1.legend(loc=(barb_legend_x_position, barb_legend_y_position), prop={'size': barb_legend_fontsize})
    leg.set_zorder(barb_legend_zorder)
    
    ax2 = fig.add_subplot(1,3,2)
    ax2.set_facecolor(subplot_background_color)
    ax2.xaxis.set_major_locator(_MaxNLocator(integer=True))
    ax2.yaxis.set_major_locator(_MaxNLocator(integer=True))

    ax2.set_xlim(0, 100)
    ax2.set_ylim(y_bottom, y_top)
    ax2.set_title(f"RELATIVE HUMIDITY",
                  fontweight='bold',
                  loc='left',
                  x=x_title_position,
                  fontsize=title_3_fontsize,
                  color=title_3_fontcolor,
                  bbox=title_3_box,
                  y=title_3_y_position)
    
    ax2.scatter(rh_x, 
                rh_y,
                vmin=_np.nanmin(df['RH'][mask]),
                vmax=_np.nanmax(df['RH'][mask]),
                color=relative_humidity_color,
                alpha=relative_humidity_alpha,
                label=f"{date.strftime('%Y-%m-%d %H:00 UTC')}")
    
    ax2.scatter(rh_x_comp, 
                rh_y_comp,
                vmin=_np.nanmin(df_comp['RH'][mask_comp]),
                vmax=_np.nanmax(df_comp['RH'][mask_comp]),
                color=relative_humidity_comparison_color,
                alpha=relative_humidity_comparison_alpha,
                label=f"{date_comp.strftime('%Y-%m-%d %H:00 UTC')}")
    
    ax2.set_xlabel(f"[%]", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis2_box)
    
    leg = ax2.legend(loc=(barb_legend_x_position, barb_legend_y_position), prop={'size': barb_legend_fontsize})
    leg.set_zorder(barb_legend_zorder)
    
    ax3 = fig.add_subplot(1,3,3)
    ax3.set_facecolor(subplot_background_color)
    ax3.xaxis.set_major_locator(_MaxNLocator(integer=True))
    ax3.yaxis.set_major_locator(_MaxNLocator(integer=True))
    
    ax3.set_xlim(_np.nanmin(ws_mins), _np.nanmax(ws_maxs))
    ax3.set_ylim(y_bottom, y_top)
    ax3.set_title(f"WIND SPEED",
                  fontweight='bold',
                  loc='left',
                  x=x_title_position,
                  fontsize=title_4_fontsize,
                  color=title_4_fontcolor,
                  bbox=title_4_box,
                  y=title_4_y_position)
    
    ax3.scatter(ws_x, 
                ws_y,
                vmin=_np.nanmin(df['SKNT'][mask]),
                vmax=_np.nanmax(df['SKNT'][mask]),
                color=wind_color,
                label=f"{date.strftime('%Y-%m-%d %H:00 UTC')}")
    
    ax3.scatter(ws_x_comp, 
                ws_y_comp,
                vmin=_np.nanmin(df_comp['SKNT'][mask_comp]),
                vmax=_np.nanmax(df_comp['SKNT'][mask_comp]),
                color=wind_comparison_color,
                label=f"{date_comp.strftime('%Y-%m-%d %H:00 UTC')}")
    
    x_positions = []
    x_positions_comp = []
    x_position = (_np.nanmin(df['SKNT'][mask]) + _np.nanmax(df['SKNT'][mask]))/2
    x_position_comp = (_np.nanmin(df_comp['SKNT'][mask_comp]) + _np.nanmax(df_comp['SKNT'][mask_comp]))/2
    for i in range(0, len(df['HGHT'][mask]), 1):
        x_positions.append(x_position)
        
    for i in range(0, len(df_comp['HGHT'][mask_comp]), 1):
        x_positions_comp.append(x_position_comp)
    
    x_position = _np.asarray(x_positions) 
    x_position_comp = _np.asarray(x_positions_comp)
    
    ax3.barbs(x_position,
              df['HGHT'][mask],
              df['U-WIND'][mask],
              df['V-WIND'][mask],
              df['SKNT'][mask],
              color=wind_color,
              length=wind_barb_length,
              alpha=wind_barb_alpha)
    
    ax3.barbs(x_position_comp,
              df_comp['HGHT'][mask_comp],
              df_comp['U-WIND'][mask_comp],
              df_comp['V-WIND'][mask_comp],
              df_comp['SKNT'][mask_comp],
              color=wind_comparison_color,
              length=wind_barb_comparison_length,
              alpha=wind_barb_comparison_alpha)
    
    ax3.set_xlabel(f"{ws_symbol}", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis3_box)
    
    leg = ax3.legend(loc=(barb_legend_x_position, barb_legend_y_position), prop={'size': barb_legend_fontsize})
    leg.set_zorder(barb_legend_zorder)
    
    fig.savefig(f"{path}/{station_id.upper()}.png", 
                bbox_inches='tight')
    
    _plt.close(fig)
    
    print(f"Saved {station_id.upper()}.png profiles to {path}.")
    
    
def plot_temperature_wind_profile_comparison(station_id,
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
                                barb_legend_zorder=10):
    

    """
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
    """
    
    _build_directory_branch(path)

    if df == None and current == True:
        df, df_comp, date, date_comp = _get_observed_sounding_data(station_id, 
                                                current=current, 
                                                comparison_24=True, 
                                                proxies=proxies,
                                                clear_recycle_bin=clear_recycle_bin)
    
    elif df == None and current == False:
        df, date = _get_observed_sounding_data(station_id, 
                                            current=current, 
                                            custom_time=custom_time_1,
                                            comparison_24=False, 
                                            proxies=proxies,
                                            clear_recycle_bin=clear_recycle_bin)
        
        df_comp, date_comp = _get_observed_sounding_data(station_id, 
                                            current=current, 
                                            custom_time=custom_time_2,
                                            comparison_24=False, 
                                            proxies=proxies,
                                            clear_recycle_bin=clear_recycle_bin)
    
    else:
        df = df
        df_comp = df_comp
        date = date
        date_comp = date_comp
        
        
    pressure = df['PRES'].values * _units('hPa')
    pressure_comp = df_comp['PRES'].values * _units('hPa')
    
    height = _mpcalc.pressure_to_height_std(pressure)
    height_comp = _mpcalc.pressure_to_height_std(pressure_comp)
    
    if to_meters == True and to_feet == False:
        height = _calc.kilometers_to_meters(height)
        height_comp = _calc.kilometers_to_meters(height_comp)
        height_symbol = f"[M]"

    elif to_feet == True and to_meters == False:
        height = _calc.kilometers_to_meters(height)
        height = _calc.meters_to_feet(height)
        height_comp = _calc.kilometers_to_meters(height_comp)
        height_comp = _calc.meters_to_feet(height_comp)
        height_symbol = f"[FT]"
    else:
        height = height
        height_comp = height_comp
        height_symbol = f"[KM]"
    
    df['HGHT'] = height.m
    df_comp['HGHT'] = height_comp.m
        
    if to_fahrenheit == True and to_kelvin == False:
        df['TEMP'] = _calc.celsius_to_fahrenheit(df['TEMP'])
        df_comp['TEMP'] = _calc.celsius_to_fahrenheit(df_comp['TEMP'])
        temperature_symbol = f"[°F]"
    elif to_kelvin == True and to_fahrenheit == False:
        df['TEMP'] = _calc.celsius_to_kelvin(df['TEMP'])
        df_comp['TEMP'] = _calc.celsius_to_kelvin(df_comp['TEMP'])
        temperature_symbol = f"[K]"
    else:
        temperature_symbol = f"[°C]"
        
    if to_mph == True and to_mps == False:
        df['SKNT'] = _calc.knots_to_mph(df['SKNT'])
        df_comp['SKNT'] = _calc.knots_to_mph(df_comp['SKNT'])
        ws_symbol = f"[MPH]"
    elif to_mph == False and to_mps == True:
        df['SKNT'] = _calc.knots_to_mps(df['SKNT'])
        df_comp['SKNT'] = _calc.knots_to_mps(df_comp['SKNT'])
        ws_symbol = f"[M/S]"
    else:
        ws_symbol = f"[KTS]"
        
    if title_1_box_alpha < 0.5:
        title_1_box_alpha = 0.5
    if title_2_box_alpha < 0.5:
        title_2_box_alpha = 0.5
    if stats_text_box_alpha < 0.5:
        stats_text_box_alpha = 0.5
    if signature_box_alpha < 0.5:
        signature_box_alpha = 0.5
    if x_axis1_box_alpha < 0.5:
        x_axis1_box_alpha = 0.5
    
    title_1_box = dict(boxstyle=title_1_box_style, 
                       facecolor=title_1_box_color, 
                       alpha=title_1_box_alpha) 
    
    title_2_box = dict(boxstyle=title_2_box_style, 
                       facecolor=title_2_box_color, 
                       alpha=title_2_box_alpha) 
    
    stats_box = dict(boxstyle=stats_text_box_style, 
                       facecolor=stats_text_box_color, 
                       alpha=stats_text_box_alpha) 
    
    props = dict(boxstyle=signature_box_style, 
                 facecolor=signature_box_color, 
                 alpha=signature_box_alpha)   
    
    x_axis1_box = dict(boxstyle=x_axis1_box_style, 
                 facecolor=x_axis1_box_color, 
                 alpha=x_axis1_box_alpha)  
    
    _mpl.rcParams['axes.labelcolor'] = axes_label_color
    _mpl.rcParams['xtick.color'] = xtick_color     
    _mpl.rcParams['ytick.color'] = ytick_color
    
    mask = (df['HGHT'] <= y_top) & (df['HGHT'] >= y_bottom) 
    mask_comp = (df_comp['HGHT'] <= y_top) & (df_comp['HGHT'] >= y_bottom) 
    
    temp_x, temp_y = _linear_anti_aliasing(df['TEMP'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
    
    temp_comp_x, temp_comp_y = _linear_anti_aliasing(df_comp['TEMP'][mask_comp], 
                                         df_comp['HGHT'][mask_comp], 
                                         anti_aliasing)
    
    min_t_height = _np.nanmax(_np.where(df['TEMP'][mask] == _np.nanmin(df['TEMP'][mask]), 
                                         df['HGHT'][mask], 
                                         0))  
    
    max_t_height = _np.nanmax(_np.where(df['TEMP'][mask] == _np.nanmax(df['TEMP'][mask]), 
                                         df['HGHT'][mask], 
                                         0)) 
    
    max_ws_height = _np.nanmax(_np.where(df['SKNT'][mask] == _np.nanmax(df['SKNT'][mask]), 
                                         df['HGHT'][mask], 
                                         0)) 
    
    min_t_height_comp = _np.nanmax(_np.where(df_comp['TEMP'][mask_comp] == _np.nanmin(df_comp['TEMP'][mask_comp]), 
                                         df_comp['HGHT'][mask_comp], 
                                         0))  
    
    max_t_height_comp = _np.nanmax(_np.where(df_comp['TEMP'][mask_comp] == _np.nanmax(df_comp['TEMP'][mask_comp]), 
                                         df_comp['HGHT'][mask_comp], 
                                         0)) 
    
    max_ws_height_comp = _np.nanmax(_np.where(df_comp['SKNT'][mask_comp] == _np.nanmax(df_comp['SKNT'][mask_comp]), 
                                         df_comp['HGHT'][mask_comp], 
                                         0)) 
    
    temp_mins = []
    temp_x_min = (_np.nanmin(df['TEMP'][mask]) - 5)
    temp_comp_x_min = (_np.nanmin(df_comp['TEMP'][mask_comp]) - 5)
    temp_mins.append(temp_x_min)
    temp_mins.append(temp_comp_x_min)
    
    temp_maxs = []
    temp_x_max = (_np.nanmax(df['TEMP'][mask]) + 5)
    temp_comp_x_max = (_np.nanmax(df_comp['TEMP'][mask_comp]) + 5)
    temp_maxs.append(temp_x_max)
    temp_maxs.append(temp_comp_x_max)
        
    fig = _plt.figure(figsize=(fig_x, fig_y))
    fig.patch.set_facecolor(facecolor)

    fig.suptitle(f"{station_id.upper()} VERTICAL PROFILE" 
                 f" | TIME 1: {date.strftime('%m/%d/%Y %H:00 UTC')} | TIME 2: {date_comp.strftime('%m/%d/%Y %H:00 UTC')}",
                 fontsize=title_1_fontsize,
                 fontweight='bold',
                 color=title_1_fontcolor,
                 bbox=title_1_box)
    
    ax = fig.add_subplot(1,1,1)
    ax.set_facecolor(subplot_background_color)
    ax.xaxis.set_major_locator(_MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(_MaxNLocator(integer=True))
    
    ax.set_xlim(_np.nanmin(temp_mins), _np.nanmax(temp_maxs))
    ax.set_ylim(y_bottom, y_top)
    
    ax.set_xlabel(f"{temperature_symbol}", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis1_box)
    
    ax.set_ylabel(f"{height_symbol}", 
                       fontsize=y_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=title_1_box)
    
    ax.set_title(f"TEMPERATURE {temperature_symbol} & WIND SPEED {ws_symbol}",
                  fontweight='bold',
                  loc='center',
                  fontsize=title_2_fontsize,
                  color=title_2_fontcolor,
                  bbox=title_2_box,
                  y=title_2_y_position)
    
    ax.scatter(temp_x, 
                temp_y,
                vmin=_np.nanmin(df['TEMP'][mask]),
                vmax=_np.nanmax(df['TEMP'][mask]),
                color=temperature_color,
                alpha=temperature_alpha,
                label=f"{date.strftime('%Y-%m-%d %H:00 UTC')}")
    
    ax.scatter(temp_comp_x, 
                temp_comp_y,
                vmin=_np.nanmin(df_comp['TEMP'][mask_comp]),
                vmax=_np.nanmax(df_comp['TEMP'][mask_comp]),
                color=temperature_comp_color,
                alpha=temperature_comp_alpha,
                label=f"{date_comp.strftime('%Y-%m-%d %H:00 UTC')}")
    
    ax.text(signature_box_x, 
             signature_box_y, 
             f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024-{_utc.strftime('%Y')} "
             f"| Data Source: weather.uwyo.edu\n"
             f"                      Image Created: {_local.strftime(f'%m/%d/%Y %H:00 {_timezone}')} - {_utc.strftime(f'%m/%d/%Y %H:00 UTC')}", 
             fontsize=signature_fontsize, 
             bbox=props, 
             fontweight='bold', 
             color=signature_fontcolor,
             transform=ax.transAxes)
    
    ax.text(stats_text_box_x_position,
            stats_text_box_y_position,
            f"{date.strftime('%Y-%m-%d %H:00 UTC')}\n"
            f"MAX TEMP ({date.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmax(df['TEMP'][mask]), 0))} {temperature_symbol} @ {int(round(max_t_height, 0))} {height_symbol}\n"
            f"MIN TEMP ({date.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmin(df['TEMP'][mask]), 0))} {temperature_symbol} @ {int(round(min_t_height, 0))} {height_symbol}\n"
            f"MAX WIND ({date.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmax(df['SKNT'][mask]), 0))} {ws_symbol} @ {int(round(max_ws_height, 0))} {height_symbol}\n\n"
            f"{date_comp.strftime('%Y-%m-%d %H:00 UTC')}\n"
            f"MAX TEMP ({date_comp.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmax(df_comp['TEMP'][mask_comp]), 0))} {temperature_symbol} @ {int(round(max_t_height_comp, 0))} {height_symbol}\n"
            f"MIN TEMP ({date_comp.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmin(df_comp['TEMP'][mask_comp]), 0))} {temperature_symbol} @ {int(round(min_t_height_comp, 0))} {height_symbol}\n"
            f"MAX WIND ({date_comp.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmax(df_comp['SKNT'][mask_comp]), 0))} {ws_symbol} @ {int(round(max_ws_height_comp, 0))} {height_symbol}",
            fontsize=legend_fontsize,
            bbox=stats_box,
            fontweight='bold',
            color=stats_text_box_fontcolor,
            transform=ax.transAxes)

    x_positions = []
    x_position = (_np.nanmin(df['TEMP'][mask]) + _np.nanmax(df['TEMP'][mask]))/2
    for i in range(0, len(df['HGHT'][mask]), 1):
        x_positions.append(x_position)
    
    x_position = _np.asarray(x_positions) 
    
    x_positions_comp = []
    x_position_comp = (_np.nanmin(df_comp['TEMP'][mask_comp]) + _np.nanmax(df_comp['TEMP'][mask_comp]))/2
    for i in range(0, len(df_comp['HGHT'][mask_comp]), 1):
        x_positions_comp.append(x_position_comp)
    
    x_position_comp = _np.asarray(x_positions_comp) 

    ax.barbs(x_position,
                df['HGHT'][mask],
                df['U-WIND'][mask],
                df['V-WIND'][mask],
                df['SKNT'][mask],
                color=wind_color,
                length=wind_barb_length,
                alpha=wind_barb_alpha)
    
    ax.barbs(x_position_comp,
                df_comp['HGHT'][mask_comp],
                df_comp['U-WIND'][mask_comp],
                df_comp['V-WIND'][mask_comp],
                df_comp['SKNT'][mask_comp],
                color=wind_comp_color,
                length=wind_comp_barb_length,
                alpha=wind_comp_barb_alpha)
    
    leg = ax.legend(loc=(barb_legend_x_position, barb_legend_y_position), prop={'size': barb_legend_fontsize})
    leg.set_zorder(barb_legend_zorder)
    
    fig.savefig(f"{path}/{station_id.upper()}.png", 
                bbox_inches='tight')
    
    _plt.close(fig)
    
    print(f"Saved {station_id.upper()}.png profiles to {path}.")
    
def plot_relative_humidity_wind_profile_comparison(station_id,
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
                                barb_legend_zorder=10):
    

    """
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
        
    12) relative_humidity_color (String) - Default='red'. The color for the relative humidity line corresponding to custom_time_1. 
    
    13) relative_humidity_color_comparison (String) - Default='blue'. The color for the relative humidity line corresponding to custom_time_2. 
    
    14) relative_humidity_alpha (Float or Integer) - Default=1. A number between 0 and 1 that corresponds to the transparency of the line.
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
    """
    
    _build_directory_branch(path)

    if df == None and current == True:
        df, df_comp, date, date_comp = _get_observed_sounding_data(station_id, 
                                                current=current, 
                                                comparison_24=True, 
                                                proxies=proxies,
                                                clear_recycle_bin=clear_recycle_bin)
    
    elif df == None and current == False:
        df, date = _get_observed_sounding_data(station_id, 
                                            current=current, 
                                            custom_time=custom_time_1,
                                            comparison_24=False, 
                                            proxies=proxies,
                                            clear_recycle_bin=clear_recycle_bin)
        
        df_comp, date_comp = _get_observed_sounding_data(station_id, 
                                            current=current, 
                                            custom_time=custom_time_2,
                                            comparison_24=False, 
                                            proxies=proxies,
                                            clear_recycle_bin=clear_recycle_bin)
    
    else:
        df = df
        df_comp = df_comp
        date = date
        date_comp = date_comp
        
        
    pressure = df['PRES'].values * _units('hPa')
    pressure_comp = df_comp['PRES'].values * _units('hPa')
    
    height = _mpcalc.pressure_to_height_std(pressure)
    height_comp = _mpcalc.pressure_to_height_std(pressure_comp)
    
    if to_meters == True and to_feet == False:
        height = _calc.kilometers_to_meters(height)
        height_comp = _calc.kilometers_to_meters(height_comp)
        height_symbol = f"[M]"

    elif to_feet == True and to_meters == False:
        height = _calc.kilometers_to_meters(height)
        height = _calc.meters_to_feet(height)
        height_comp = _calc.kilometers_to_meters(height_comp)
        height_comp = _calc.meters_to_feet(height_comp)
        height_symbol = f"[FT]"
    else:
        height = height
        height_comp = height_comp
        height_symbol = f"[KM]"
    
    df['HGHT'] = height.m
    df_comp['HGHT'] = height_comp.m
        
    if to_mph == True and to_mps == False:
        df['SKNT'] = _calc.knots_to_mph(df['SKNT'])
        df_comp['SKNT'] = _calc.knots_to_mph(df_comp['SKNT'])
        ws_symbol = f"[MPH]"
    elif to_mph == False and to_mps == True:
        df['SKNT'] = _calc.knots_to_mps(df['SKNT'])
        df_comp['SKNT'] = _calc.knots_to_mps(df_comp['SKNT'])
        ws_symbol = f"[M/S]"
    else:
        ws_symbol = f"[KTS]"
        
    if title_1_box_alpha < 0.5:
        title_1_box_alpha = 0.5
    if title_2_box_alpha < 0.5:
        title_2_box_alpha = 0.5
    if stats_text_box_alpha < 0.5:
        stats_text_box_alpha = 0.5
    if signature_box_alpha < 0.5:
        signature_box_alpha = 0.5
    if x_axis1_box_alpha < 0.5:
        x_axis1_box_alpha = 0.5
    
    title_1_box = dict(boxstyle=title_1_box_style, 
                       facecolor=title_1_box_color, 
                       alpha=title_1_box_alpha) 
    
    title_2_box = dict(boxstyle=title_2_box_style, 
                       facecolor=title_2_box_color, 
                       alpha=title_2_box_alpha) 
    
    stats_box = dict(boxstyle=stats_text_box_style, 
                       facecolor=stats_text_box_color, 
                       alpha=stats_text_box_alpha) 
    
    props = dict(boxstyle=signature_box_style, 
                 facecolor=signature_box_color, 
                 alpha=signature_box_alpha)   
    
    x_axis1_box = dict(boxstyle=x_axis1_box_style, 
                 facecolor=x_axis1_box_color, 
                 alpha=x_axis1_box_alpha)  
    
    _mpl.rcParams['axes.labelcolor'] = axes_label_color
    _mpl.rcParams['xtick.color'] = xtick_color     
    _mpl.rcParams['ytick.color'] = ytick_color
    
    mask = (df['HGHT'] <= y_top) & (df['HGHT'] >= y_bottom) 
    mask_comp = (df_comp['HGHT'] <= y_top) & (df_comp['HGHT'] >= y_bottom) 
    
    rh_x, rh_y = _linear_anti_aliasing(df['RH'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
    
    rh_comp_x, rh_comp_y = _linear_anti_aliasing(df_comp['RH'][mask_comp], 
                                         df_comp['HGHT'][mask_comp], 
                                         anti_aliasing)
    
    min_rh_height = _np.nanmax(_np.where(df['RH'][mask] == _np.nanmin(df['RH'][mask]), 
                                         df['HGHT'][mask], 
                                         0))  
    
    max_rh_height = _np.nanmax(_np.where(df['RH'][mask] == _np.nanmax(df['RH'][mask]), 
                                         df['RH'][mask], 
                                         0)) 
    
    max_ws_height = _np.nanmax(_np.where(df['SKNT'][mask] == _np.nanmax(df['SKNT'][mask]), 
                                         df['HGHT'][mask], 
                                         0)) 
    
    min_rh_height_comp = _np.nanmax(_np.where(df_comp['RH'][mask_comp] == _np.nanmin(df_comp['RH'][mask_comp]), 
                                         df_comp['HGHT'][mask_comp], 
                                         0))  
    
    max_rh_height_comp = _np.nanmax(_np.where(df_comp['RH'][mask_comp] == _np.nanmax(df_comp['RH'][mask_comp]), 
                                         df_comp['HGHT'][mask_comp], 
                                         0)) 
    
    max_ws_height_comp = _np.nanmax(_np.where(df_comp['SKNT'][mask_comp] == _np.nanmax(df_comp['SKNT'][mask_comp]), 
                                         df_comp['HGHT'][mask_comp], 
                                         0)) 
        
    fig = _plt.figure(figsize=(fig_x, fig_y))
    fig.patch.set_facecolor(facecolor)

    fig.suptitle(f"{station_id.upper()} VERTICAL PROFILE" 
                 f" | TIME 1: {date.strftime('%m/%d/%Y %H:00 UTC')} | TIME 2: {date_comp.strftime('%m/%d/%Y %H:00 UTC')}",
                 fontsize=title_1_fontsize,
                 fontweight='bold',
                 color=title_1_fontcolor,
                 bbox=title_1_box)
    
    ax = fig.add_subplot(1,1,1)
    ax.set_facecolor(subplot_background_color)
    ax.xaxis.set_major_locator(_MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(_MaxNLocator(integer=True))
    
    ax.set_xlim(0, 100)
    ax.set_ylim(y_bottom, y_top)
    
    ax.set_xlabel(f"[%]", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis1_box)
    
    ax.set_ylabel(f"{height_symbol}", 
                       fontsize=y_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=title_1_box)
    
    ax.set_title(f"RELATIVE HUMIDITY [%] & WIND SPEED {ws_symbol}",
                  fontweight='bold',
                  loc='center',
                  fontsize=title_2_fontsize,
                  color=title_2_fontcolor,
                  bbox=title_2_box,
                  y=title_2_y_position)
    
    ax.scatter(rh_x, 
                rh_y,
                vmin=_np.nanmin(df['TEMP'][mask]),
                vmax=_np.nanmax(df['TEMP'][mask]),
                color=rh_color,
                alpha=rh_alpha,
                label=f"{date.strftime('%Y-%m-%d %H:00 UTC')}")
    
    ax.scatter(rh_comp_x, 
                rh_comp_y,
                vmin=_np.nanmin(df_comp['TEMP'][mask_comp]),
                vmax=_np.nanmax(df_comp['TEMP'][mask_comp]),
                color=rh_comp_color,
                alpha=rh_comp_alpha,
                label=f"{date_comp.strftime('%Y-%m-%d %H:00 UTC')}")
    
    ax.text(signature_box_x, 
             signature_box_y, 
             f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024-{_utc.strftime('%Y')} "
             f"| Data Source: weather.uwyo.edu\n"
             f"                      Image Created: {_local.strftime(f'%m/%d/%Y %H:00 {_timezone}')} - {_utc.strftime(f'%m/%d/%Y %H:00 UTC')}", 
             fontsize=signature_fontsize, 
             bbox=props, 
             fontweight='bold', 
             color=signature_fontcolor,
             transform=ax.transAxes)
    
    ax.text(stats_text_box_x_position,
            stats_text_box_y_position,
            f"{date.strftime('%Y-%m-%d %H:00 UTC')}\n"
            f"MAX RH ({date.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmax(df['RH'][mask]), 0))} [%] @ {int(round(max_rh_height, 0))} {height_symbol}\n"
            f"MIN RH ({date.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmin(df['RH'][mask]), 0))} [%] @ {int(round(min_rh_height, 0))} {height_symbol}\n"
            f"MAX WIND ({date.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmax(df['SKNT'][mask]), 0))} {ws_symbol} @ {int(round(max_ws_height, 0))} {height_symbol}\n\n"
            f"{date_comp.strftime('%Y-%m-%d %H:00 UTC')}\n"
            f"MAX RH ({date_comp.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmax(df_comp['RH'][mask_comp]), 0))} [%] @ {int(round(max_rh_height_comp, 0))} {height_symbol}\n"
            f"MIN RH ({date_comp.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmin(df_comp['RH'][mask_comp]), 0))} [%] @ {int(round(min_rh_height_comp, 0))} {height_symbol}\n"
            f"MAX WIND ({date_comp.strftime('%Y-%m-%d %H:00 UTC')}): {int(round(_np.nanmax(df_comp['SKNT'][mask_comp]), 0))} {ws_symbol} @ {int(round(max_ws_height_comp, 0))} {height_symbol}",
            fontsize=legend_fontsize,
            bbox=stats_box,
            fontweight='bold',
            color=stats_text_box_fontcolor,
            transform=ax.transAxes)

    x_positions = []
    x_position = (_np.nanmin(df['RH'][mask]) + _np.nanmax(df['RH'][mask]))/2
    for i in range(0, len(df['HGHT'][mask]), 1):
        x_positions.append(x_position)
    
    x_position = _np.asarray(x_positions) 
    
    x_positions_comp = []
    x_position_comp = (_np.nanmin(df_comp['RH'][mask_comp]) + _np.nanmax(df_comp['RH'][mask_comp]))/2
    for i in range(0, len(df_comp['HGHT'][mask_comp]), 1):
        x_positions_comp.append(x_position_comp)
    
    x_position_comp = _np.asarray(x_positions_comp) 

    ax.barbs(x_position,
                df['HGHT'][mask],
                df['U-WIND'][mask],
                df['V-WIND'][mask],
                df['SKNT'][mask],
                color=wind_color,
                length=wind_barb_length,
                alpha=wind_barb_alpha)
    
    ax.barbs(x_position_comp,
                df_comp['HGHT'][mask_comp],
                df_comp['U-WIND'][mask_comp],
                df_comp['V-WIND'][mask_comp],
                df_comp['SKNT'][mask_comp],
                color=wind_comp_color,
                length=wind_comp_barb_length,
                alpha=wind_comp_barb_alpha)
    
    leg = ax.legend(loc=(barb_legend_x_position, barb_legend_y_position), prop={'size': barb_legend_fontsize})
    leg.set_zorder(barb_legend_zorder)
    
    fig.savefig(f"{path}/{station_id.upper()}.png", 
                bbox_inches='tight')
    
    _plt.close(fig)
    
    print(f"Saved {station_id.upper()}.png profiles to {path}.")
    
        