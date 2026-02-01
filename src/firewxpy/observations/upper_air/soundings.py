"""
This file hosts the function that plots observed sounding graphics.

Data Source: University of Wyoming.

(C) Eric J. Drewitz 2024-2026
"""
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib as mpl
import pandas as pd
import metpy.calc as mpcalc
import numpy as np
import math

from metpy.plots import SkewT
from metpy.units import units
from wxdata import get_observed_sounding_data as _get_observed_sounding_data
from firewxpy.utils.standard import(
    plot_creation_time as _plot_creation_time,
    get_timezone_abbreviation as _get_timezone_abbreviation
)
from firewxpy.utils.directory import build_directory_branch as _build_directory_branch

mpl.rcParams['font.weight'] = 'bold'
pd.options.mode.copy_on_write = True
local, utc = _plot_creation_time()
timezone = _get_timezone_abbreviation()

try:
    nan = np.NaN
except Exception as e:
    nan = np.nan

def plot_observed_sounding(station_id,
                           current=True,
                           custom_time=None,
                           proxies=None,
                           clear_recycle_bin=False,
                           path='FireWxPy Graphics/Observations/Upper Air/Soundings',
                           temperature_line_color='crimson',
                           temperature_linewidth=3,
                           temperature_line_alpha=0.5,
                           dew_point_line_color='lime',
                           dew_point_linewidth=3,
                           dew_point_line_alpha=0.5,
                           wet_bulb_line_color='cyan',
                           wet_bulb_linewidth=2,
                           wet_bulb_line_alpha=0.5,
                           wind_barb_color='deeppink',
                           wind_barb_color_table='rainbow',
                           wind_barb_dynamic_colors=True,
                           wind_barb_length=6,
                           lcl_marker_color='purple',
                           lfc_marker_color='darkorange',
                           el_marker_color='violet',
                           lcl_lfc_el_marker_size=30,
                           lcl_lfc_el_marker_edge_width=3,
                           dry_adiabats_alpha=0.5,
                           moist_adiabats_alpha=0.5,
                           mixing_ratio_lines_alpha=0.5,
                           freezing_level_line_color='aquamarine',
                           freezing_level_linestyle='--',
                           freezing_level_linewidth=3,
                           y_bottom=1030,
                           y_top=100,
                           x_bottom=-45,
                           x_top=45,
                           fig_y=12,
                           fig_x=10,
                           parcel_profile_color='yellow',
                           parcel_profile_linestyle='--',
                           parcel_profile_linewidth=2,
                           parcel_profile_alpha=0.5,
                           signature_box_x=0.1725,
                           signature_box_y=0.04,
                           signature_box_style='round',
                           signature_box_color='steelblue',
                           signature_box_alpha=0.5,
                           signature_fontsize=8,
                           signature_fontcolor='black',
                           legend_x_position=0,
                           legend_y_position=0,
                           legend_fontsize=10,
                           title_1_fontsize=14,
                           title_1_box_style='round',
                           title_1_box_color='steelblue',
                           title_1_box_alpha=0.5,
                           title_1_fontcolor='black',
                           title_2_fontsize=12,
                           title_2_box_style='round',
                           title_2_box_color='steelblue',
                           title_2_box_alpha=0.5,
                           title_2_fontcolor='black',
                           x_axis_label_fontsize=12,
                           y_axis_label_fontsize=12,
                           axes_label_color='black',
                           xtick_color='black',
                           ytick_color='black',
                           facecolor='lavender',
                           skew_t_background_color='silver',
                           df=None,
                           date=None,):
    
    """
    This function plots the observed sounding data for any upper-air observations site. 
    
    Required Arguments:

    1) station_id (String or Integer) - User inputs the station_id as a string or an integer. 
    Some stations only have the ID by integer. Please see https://weather.uwyo.edu/upperair/sounding_legacy.html for more info. 
    
    Optional Arguments:

    1) current (Boolean) - Default = True. When set to True, the latest available data will be returned.
    If set to False, the user can download the data for a custom date/time of their choice. 

    2) custom_time (String) - If a user wants to download the data for a custom date/time, they must do the following:

        1. set current=False
        2. set custom_time='YYYY-mm-dd:HH'

    3) proxies (String) - Default=None. If the user is requesting the data on a machine using a proxy server,
    the user must set proxy='proxy_url'. The default setting assumes the user is not using a proxy server conenction.
    
        Example
        -------
        
        If the user wishes to configure a proxy:
        
        proxies=None ---> proxies={
                        'http':'http://url',
                        'https':'https://url'
                        }

        [e.g. get_observed_sounding_data('nkx', proxies=proxies)]
    
    4) clear_recycle_bin (Boolean) - Default=True. When set to True, the contents in your recycle/trash bin will be deleted with each run
        of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    5) path (String) - Default='FireWxPy Graphics/Observations/Upper Air/Soundings'. The branch of the graphics directory that hosts the graphics.
    
    6) temperature_line_color (String) - Default='red'. Color of the temperature line on the skew-t.
    
    7) temperature_linewidth (Integer) - Default=3.
    
    8) temperature_line_alpha (Float or Integer) - Default=0.5. Ranges from 0 to 1. 0 being more transparent (faded), 1 being opaque. 
    
    9) dew_point_line_color (String) - Default='green'. Color of the dew point line on the skew-t. 
    
    10) dew_point_linewidth (Integer) - Default=3.
    
    11) dew_point_line_alpha (Float or Integer) - Default=0.5. Ranges from 0 to 1. 0 being more transparent (faded), 1 being opaque.
    
    12) wet_bulb_line_color (String) - Default = 'cyan'. Color of the wet-bulb line on the skew-t.
    
    13) wet_bulb_linewidth (Integer) - Default=2. 
    
    14) wet_bulb_line_alpha (Float or Integer) - Default=0.3. Ranges from 0 to 1. 0 being more transparent (faded), 1 being opaque.
    
    15) wind_barb_color (String) - Default='deeppink'. Color of wind barbs.  
    
    16) wind_barb_color_table (String) - Default='rainbow'. The colortable for wind barbs. See matplotlib colortables for more information.
    
    17) wind_barb_dynamic_colors (Boolean) - Default=True. When set to True, wind barbs will be displayed by wind_barb_color_table.
        When set to False, color will be static and wind barbs will be displayed by wind_barb_color.
        
    18) wind_barb_length (Integer) - Default=6. The length of the wind barbs. 
    
    19) lcl_marker_color (String) - Default='purple'. Color of the LCL marker on the skew-t. 
    
    20) lfc_marker_color (String) - Default='darkorange'. Color of the LFC marker on the skew-t. 
    
    21) el_marker_color (String) - Default='violet'. Color of the EL marker on the skew-t. 
    
    22) lcl_lfc_el_marker_size (Integer) - Default=30. 
    
    23) lcl_lfc_el_marker_edge_width (Integer) - Default=3. 
    
    24) dry_adiabats_alpha (Float or Integer) - Default=0.5. Ranges from 0 to 1. 0 being more transparent (faded), 1 being opaque.
    
    25) moist_adiabats_alpha (Float or Integer) - Default=0.5. Ranges from 0 to 1. 0 being more transparent (faded), 1 being opaque.
    
    26) mixing_ratio_lines_alpha (Float or Integer) - Default=0.5. Ranges from 0 to 1. 0 being more transparent (faded), 1 being opaque.
    
    27) freezing_level_line_color (String) - Default='aquamarine'. 
    
    28) freezing_level_linestyle (String) - Default='--'.
    
    29) freezing_level_linewidth (Integer) - Default=3. 
    
    27) y_bottom (Integer) - Default=1030. The pressure in hectopascals/millibars of the bottom of the skew-t graphic.
    
    28) y_top (Integer) - Default=100. The pressure in hectopascals/millibars of the top of the skew-t graphic. 
    
    29) x_bottom (Integer) - Default=-45. The temperature [Celsius] denoting the far-left side of the skew-t graphic. 
    
    30) x_top (Integer) - Default=45. The temperature [Celsius] denoting the far-right side of the skew-t graphic.
    
    31) fig_y (Integer) - Default=12. The y-direction (number of columns) length of the figure. 
    
    32) fig_x (Integer) - Default=10. The x-direction (number of rows) length of the figure.  
    
    33) parcel_profile_color (String) - Default='black'. The color of the parcel profile on the skew-t. 
    
    34) parcel_profile_linestyle (String) - Default='--'.
    
    35) parcel_profile_linewidth (Integer) - Default=2.
    
    36) parcel_profile_alpha (Float) - Default=0.5. Ranges from 0 to 1. 0 being more transparent (faded), 1 being opaque. 
        
    37) signature_box_x (Float) - Default=0.1725. The x-position on the figure of the signature box. This is based on a 
        figure with 12 rows and 10 columns. This setting will likely need to be tweaked if the user changes the figure
        dimensions. 
        
    38) signature_box_y (Float) - Default=0.04. The y-position on the figure of the signature box. This is based on a 
        figure with 12 rows and 10 columns. This setting will likely need to be tweaked if the user changes the figure
        dimensions. 
    
    39) signature_box_style (String) - Default='round'. The style of the signature text box.
    
        Matplotlib Text Box Style Options
        ---------------------------------
        
                'square'
                'circle'
                'ellipse'
                'larrow'
                'rarrow'
                'darrow'
                'round'
                'round4'
                'sawtooth'
                'roundtooth'
        
    40) signature_box_color (String) - Default='steelblue'. The color of the signature box at the bottom of the figure. 
    
    41) signature_box_alpha (Float or Integer) - Default=0.5. Ranging from 0.5 to 1 for the transparency of the signature box.
        To ensure FireWxPy gets credit for the graphics, this setting can only be reduced to 0.5 at minimum. 
        
    42) signature_fontsize (Integer) - Default=8. Fontsize of the text in the signature text box. 
    
    43) signature_fontcolor (String) - Default='black'. The color of the text in the signature text box. 
    
    44) legend_x_position (Integer) - Default=0. x-position on the skew-t subplot axis of the left side of the legend.
    
    45) legend_y_position (Integer) - Default=0. y-position on the skew-t subplot axis of the bottom of the legend.
    
    46) legend_fontsize (Integer) - Default=10. The fontsize of the text in the legend. 
    
    47) title_1_fontsize (Integer) - Default=14. The fontsize of the title on the left side of the skew-t graphic. 
        This title features the station_id chosen by the user indicating the sounding site station identifier. 
        
    48) title_1_box_style (String) - Default='round'. The style of the left-side title text box. 
    
        Matplotlib Text Box Style Options
        ---------------------------------
        
                'square'
                'circle'
                'ellipse'
                'larrow'
                'rarrow'
                'darrow'
                'round'
                'round4'
                'sawtooth'
                'roundtooth'

    49) title_1_box_color (String) - Default='steelblue'. The color of the left-side title box at the top of the figure. 
    
    50) title_1_box_alpha (Float or Integer) - Default=0.5. The transparency of the left-side title box. Ranges from 0.5 to 1.
    
    51) title_1_fontcolor (String) - Default='black'. The color of the text in the left-side title box. 
        
    52) title_2_fontsize (Integer) - Default=12. The fontsize of the title on the right side of the skew-t graphic. 
        This title features the observation validity time.
        
    53) title_2_box_style (String) - Default='round'. The style of the right-side title text box. 
    
        Matplotlib Text Box Style Options
        ---------------------------------
        
                'square'
                'circle'
                'ellipse'
                'larrow'
                'rarrow'
                'darrow'
                'round'
                'round4'
                'sawtooth'
                'roundtooth'
        
    54) title_2_box_color (String) - Default='steelblue'. The color of the right-side title box at the top of the figure. 
    
    55) title_2_box_alpha (Float or Integer) - Default=0.5. The transparency of the right-side title box. Ranges from 0.5 to 1.
    
    56) title_2_fontcolor (String) - Default='black'. The color of the text in the right-side title box.
        
    57) x_axis_label_fontsize (Integer) - Default=12. The fontsize of the x-axis label.
    
    58) y_axis_label_fontsize (Integer) - Default=12. The fontsize of the y-axis label.
    
    59) axes_label_color (String) - Default='black'. The color of the labels on both axes. 
    
    60) xtick_color (String) - Default='black'. The color of the tick marks on the x-axis. 
    
    61) ytick_color (String) - Default='black'. The color of the tick marks on the y-axis.
    
    62) facecolor (String) - Default='lavender'. The color of the plot outside of the skew-t graphic.
    
    63) skew_t_background_color (String) - Default='silver'. The color of the background inside of the skew-t subplot. 
    
    64) df (Pandas.DataFrame) - Default=None. If the user is creating a medley of observed upper-air plots and is 
        properly minimizing the amount of requests on the data servers, the user is downloading the data via
        the WxData package once per station and is passing the data into the function. Set df={name of dataframe}
        to pass data in that was downloaded externally. When set to the default value of None, the data is downloaded
        inside of the function. 
        
    65) date (datetime) - Default=None. If the user is creating a medley of observed upper-air plots and is 
        properly minimizing the amount of requests on the data servers, the user is downloading the data via
        the WxData package once per station and is passing the data into the function. Set ate={name of datetime object}
        to pass data in that was downloaded externally. When set to the default value of None, the data is downloaded
        inside of the function. 
        
    Returns
    -------
    
    A observed sounding graphic for the user-specified time and preferences saved to {path}
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
    
    
    pressure = df['PRES'].values * units('hPa')
    temperature = df['TEMP'].values * units('degC')
    dewpoint = df['DWPT'].values * units('degC')
    u = df['U-WIND'].values * units('kts')
    v = df['V-WIND'].values * units('kts')
    ws = df['SKNT'].values  * units('kts')
    wetbulb = df['WET-BULB'].values * units('degC')
    
    interval = np.logspace(2, 3) 
    mask = (pressure >= y_top * units('hPa'))
    pres = pressure[mask]
    idx = mpcalc.resample_nn_1d(pres.m, 
                                interval)
    
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
    
    mpl.rcParams['axes.labelcolor'] = axes_label_color
    mpl.rcParams['xtick.color'] = xtick_color     
    mpl.rcParams['ytick.color'] = ytick_color
    
    fig = plt.figure(figsize=(fig_y, fig_x))
    fig.patch.set_facecolor(facecolor)
    
    skew = SkewT(fig, 
                 rotation=45, 
                 subplot=(1,1,1))
    
    skew.ax.set_facecolor(skew_t_background_color)
    
    skew.ax.set_title(f"{station_id.upper()} SOUNDING", 
                      fontsize=title_1_fontsize, 
                      fontweight='bold', 
                      loc='left', 
                      bbox=title_1_box, 
                      color=title_1_fontcolor,
                      x=0.01)
    
    skew.ax.set_title(f"Valid: {date.strftime('%m/%d/%Y %H:00 UTC')}", 
                      fontsize=title_2_fontsize, 
                      fontweight='bold', 
                      loc='right', 
                      bbox=title_2_box, 
                      color=title_2_fontcolor)
    
    skew.plot_dry_adiabats(label='Dry Adiabats', 
                           alpha=dry_adiabats_alpha)
    
    skew.plot_mixing_lines(label='Mixing Ratio Lines', 
                           alpha=mixing_ratio_lines_alpha)
    
    skew.plot_moist_adiabats(label='Moist Adiabats', 
                             alpha=moist_adiabats_alpha)
    
    skew.ax.set_xlabel("Temperature [℃]", 
                       fontsize=x_axis_label_fontsize, 
                       fontweight='bold')
    
    skew.ax.set_ylabel("Pressure [hPa]", 
                       fontsize=y_axis_label_fontsize, 
                       fontweight='bold')
    
    skew.ax.set_ylim(y_bottom, 
                     y_top)
    
    skew.ax.set_xlim(x_bottom, 
                     x_top)
    
    skew.plot(pressure[mask], 
              temperature[mask], 
              temperature_line_color, 
              linewidth=temperature_linewidth, 
              alpha=temperature_line_alpha)
    
    skew.plot(pressure[mask], 
              dewpoint[mask], 
              dew_point_line_color, 
              linewidth=dew_point_linewidth, 
              alpha=dew_point_line_alpha)
    
    if wind_barb_dynamic_colors == True:
        
        skew.plot_barbs(pressure[idx], 
                        u[idx], 
                        v[idx], 
                        c=ws[idx],
                        cmap=wind_barb_color_table,
                        length=wind_barb_length)
    
    else:
        skew.plot_barbs(pressure[idx], 
                        u[idx], 
                        v[idx], 
                        color=wind_barb_color, 
                        length=wind_barb_length)
    
    skew.plot(pressure[mask], 
              wetbulb[mask], 
              wet_bulb_line_color, 
              alpha=wet_bulb_line_alpha, 
              linewidth=wet_bulb_linewidth)
    
    lcl_pressure, lcl_temperature = mpcalc.lcl(pressure[0], 
                                               temperature[0], 
                                               dewpoint[0])
    
    lfc_pressure, lfc_temperature = mpcalc.lfc(pressure, 
                                               temperature, 
                                               dewpoint)
    
    el_pressure, el_temperature = mpcalc.el(pressure, 
                                            temperature, 
                                            dewpoint)
    
    lcl_pressure = float(lcl_pressure.m)
    lfc_pressure = float(lfc_pressure.m)
    el_pressure = float(el_pressure.m)
    
    lcl_nan = math.isnan(lcl_pressure)
    lfc_nan = math.isnan(lfc_pressure)
    el_nan = math.isnan(el_pressure)
    
    profile = mpcalc.parcel_profile(pressure, 
                                    temperature[0], 
                                    dewpoint[0]).to('degC')
    
    skew.plot(pressure, 
              profile, 
              parcel_profile_color, 
              linestyle=parcel_profile_linestyle, 
              linewidth=parcel_profile_linewidth, 
              alpha=parcel_profile_alpha)
    
    # Shade areas of CAPE and CIN
    skew.shade_cin(pressure, 
                   temperature, 
                   profile, 
                   dewpoint)
    
    skew.shade_cape(pressure, 
                    temperature, 
                    profile)
    
    # Plots LCL LFC and EL
    if lcl_nan == False:
        skew.ax.plot(lcl_temperature, 
                        lcl_pressure, 
                        marker="_", 
                        label='LCL', 
                        color=lcl_marker_color, 
                        markersize=lcl_lfc_el_marker_size, 
                        markeredgewidth=lcl_lfc_el_marker_edge_width)
    else:
        pass

    if lfc_nan == False:
        skew.ax.plot(lfc_temperature, 
                     lfc_pressure, 
                     marker="_", 
                     label='LFC', 
                     color=lfc_marker_color, 
                     markersize=lcl_lfc_el_marker_size, 
                     markeredgewidth=lcl_lfc_el_marker_edge_width)
    else:
        pass

    if el_nan == False:
        skew.ax.plot(el_temperature, 
                     el_pressure, marker="_", 
                     label='EL', 
                     color=el_marker_color, 
                     markersize=lcl_lfc_el_marker_size, 
                     markeredgewidth=lcl_lfc_el_marker_edge_width)
    else:
        pass
    
    # Colors of the freezing level isotherm (cyan) and the boundaries of the dendridic growth zone (yellow)
    skew.ax.axvline(0, 
                    color=freezing_level_line_color, 
                    linestyle=freezing_level_linestyle, 
                    linewidth=freezing_level_linewidth)
    
    skew.ax.legend(loc=(legend_x_position, legend_y_position), 
                   prop={'size': legend_fontsize})
        
    if signature_box_alpha < 0.5:
        signature_box_alpha = 0.5    
        
    props = dict(boxstyle=signature_box_style, 
                 facecolor=signature_box_color, 
                 alpha=signature_box_alpha)    
        
    fig.text(signature_box_x, 
             signature_box_y, 
             f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024-{utc.strftime('%Y')} "
             f"| Data Source: weather.uwyo.edu"
             f"| Image Created: {utc.strftime('%m/%d/%Y %H:00 UTC')}", 
             fontsize=signature_fontsize, 
             bbox=props, 
             fontweight='bold', 
             color=signature_fontcolor)
    
    fig.savefig(f"{path}/{station_id.upper()}.png", 
                bbox_inches='tight')
    
    plt.close(fig)
    
    print(f"Saved {station_id.upper()}.png sounding to {path}.")
    
    
    
    
    