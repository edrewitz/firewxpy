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
from wxdata import get_observed_sounding_data as _get_observed_sounding_data
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
                                                    path='FireWxPy Graphics/Observations/Upper Air/Profiles',
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
    This function plots an observed temperature/relative humidity/wind profile from an atmospheric sounding
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
    
    temp_x, temp_y = _calc.anti_aliasing(df['TEMP'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
    
    rh_x, rh_y = _calc.anti_aliasing(df['RH'][mask], 
                                         df['HGHT'][mask], 
                                         anti_aliasing)
    
    ws_x, ws_y = _calc.anti_aliasing(df['SKNT'][mask], 
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
    
    ax1.set_xlabel(f"{temperature_symbol}", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis1_box)
    
    ax1.set_ylabel(f"HEIGHT {height_symbol}", 
                       fontsize=y_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=title_1_box)
    
    ax1.set_title(f"TEMPERATURE {temperature_symbol}",
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
    ax2.set_title(f"RELATIVE HUMIDITY [%]",
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
    
    ax2.set_xlabel(f"[%]", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis2_box)
    
    
    ax3 = fig.add_subplot(1,3,3)
    ax3.set_facecolor(subplot_background_color)
    ax3.xaxis.set_major_locator(_MaxNLocator(integer=True))
    ax3.yaxis.set_major_locator(_MaxNLocator(integer=True))
    
    ax3.set_xlim((_np.nanmin(df['SKNT'][mask]) - 5), (_np.nanmax(df['SKNT'][mask]) + 5))
    ax3.set_ylim(y_bottom, y_top)
    ax3.set_title(f"WIND SPEED {ws_symbol}",
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
    
    ax3.set_xlabel(f"{ws_symbol}", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold',
                       bbox=x_axis3_box)
    
    fig.savefig(f"{path}/{station_id.upper()}.png", 
                bbox_inches='tight')
    
    _plt.close(fig)
    
    print(f"Saved {station_id.upper()}.png sounding to {path}.")
    
    
    
    
    

    
    
    
    
        