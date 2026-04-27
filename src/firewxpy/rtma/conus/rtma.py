"""
This file hosts the functions for the CONUS Real Time Mesoscale Analysis (RTMA) Graphics

(C) Eric J. Drewitz 2024 - 2026
"""
import warnings as _warnings
_warnings.filterwarnings('ignore')
import matplotlib as _mpl 
import firewxpy.calc.calc as _calc
import matplotlib.pyplot as _plt 
import matplotlib.colors as _mcolors
import cartopy.crs as _ccrs 
import cartopy.feature as _cfeature 
import metpy.plots as _mpplots
import numpy as _np
import pandas as _pd

from dateutil import tz as _tz
from matplotlib.patheffects import withStroke as _withStroke
from firewxpy.utils.station_plot_formatting import fix_var_array as _fix_var_array
from firewxpy.utils.directory import build_directory_branch as _build_directory_branch
from firewxpy.utils.plot_coords import bounding_box as _bounding_box
from firewxpy.calc.calc import(
    kelvin_to_fahrenheit as _kelvin_to_fahrenheit, 
    celsius_to_fahrenheit as _celsius_to_fahrenheit,
    kelvin_to_celsius as _kelvin_to_celsius
)
from firewxpy.utils.standard import(
    get_timezone_abbreviation as _get_timezone_abbreviation,
    plot_creation_time as _plot_creation_time
)
from firewxpy.utils.geometry import(
    import_shapefile_from_web as _import_shapefile_from_web,
    import_shapefile_local as _import_shapefile_local,
    import_geojson_from_web as _import_geojson_from_web,
    import_geojson_local as _import_geojson_local,
    get_filename_from_url as _get_filename_from_url
)
from wxdata import rtma as _rtma

_local, _utc = _plot_creation_time()
_timezone = _get_timezone_abbreviation()
_from_zone = _tz.tzutc()
_to_zone = _tz.tzlocal()
_mpl.rcParams['font.weight'] = 'bold'

def plot_temperature(region='conus',
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=50,
                     start=-30,
                     stop=130,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER TEMPERATURE [°F]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=12,
                     secondary_title_fontsize=10,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=10,
                     colorbar_aspect=50,
                     colormap='jet',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['magenta',
                             'orchid',
                             'plum',
                             'darkviolet',
                             'darkslateblue',
                             'blue',
                             'cyan',
                             'lawngreen',
                             'greenyellow',
                             'olive',
                             'gold',
                             'goldenrod',
                             'darkorange',
                             'deeppink',
                             'crimson',
                             'darkred',
                             'grey'],
                     ds=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=4,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA/Temperature',
                     filename='RTMA Temperature.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     convert_temperature=True,
                     convert_from='kelvin',
                     convert_to='fahrenheit',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     var_key='2m_temperature',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude'):
    
    """
    This function plots the latest Real Time Mesoscale Analysis (RTMA) for temperature.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Entire CONUS region.
            ii) 'Jet' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Required Arguments: None
    
    Optional Arguments:
    
    1) region (String) - Default='conus'. The region of the plot. Use the 2-letter state abbreviation or 4-letter GACC abbreviation.
        If the user wants a completely custom region where they define their own lat/lon bounds, set region='custom'. 
        
    2) show_states (Boolean) - Default=True. When set to True, U.S. state borders are shown. 
    
    3) state_border_color (String) - Default='black'. The color of the U.S. state borders.
    
    4) state_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the U.S. state borders.
    
    5) state_border_zorder (Integer) - Default=3. The z-order of the state borders. For state borders to be displayed
        the following condition must be met: state_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
        
    6) show_counties (Boolean) - Default=True. When set to True, U.S. county borders are shown. 
    
    7) county_border_color (String) - Default='black'. The color of the U.S. county borders.
    
    8) county_border_linewidth (Float or Integer) - Default=0.25. The linewidth of the U.S. county borders.
    
    9) county_border_zorder (Integer) - Default=3. The z-order of the county borders. For county borders to be displayed
        the following condition must be met: county_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
    
    10) show_gacc_boundaries (Boolean) - Default=False. When set to True, Geographic Area Coordination Center borders are shown. 
    
    11) gacc_border_color (String) - Default='black'. The color of the Geographic Area Coordination Center borders.
    
    12) gacc_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the Geographic Area Coordination Center borders.
    
    13) gacc_border_zorder (Integer) - Default=3. The z-order of the Geographic Area Coordination Center borders. 
       For Geographic Area Coordination Center borders to be displayed the following condition must be met: gacc_border_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
       
    14) show_predictive_services_areas (Boolean) - Default=False. When set to True, Predictive Services Areas borders are shown. 
    
    15) predictive_services_areas_color (String) - Default='black'. The color of the Predictive Services Areas borders.
    
    16) predictive_services_areas_linewidth (Float or Integer) - Default=0.25. The linewidth of the Predictive Services Areas borders.
    
    17) predictive_services_areas_zorder (Integer) - Default=3. The z-order of the Predictive Services Areas borders. 
       For Predictive Services Areas borders to be displayed the following condition must be met: predictive_services_areas_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    18) show_nws_public_zones (Boolean) - Default=False. When set to True, NWS Public Zone borders are shown. 
    
    19) nws_public_zones_color (String) - Default='black'. The color of the NWS Public Zone borders.
    
    20) nws_public_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Public Zone borders.
    
    21) nws_public_zones_zorder (Integer) - Default=3. The z-order of the NWS Public Zone borders. 
       For NWS Public Zone borders to be displayed the following condition must be met: nws_public_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    22) show_nws_fire_weather_zones (Boolean) - Default=False. When set to True, NWS Fire Weather Zone borders are shown. 
    
    23) nws_fire_weather_zones_color (String) - Default='black'. The color of the NWS Fire Weather Zone borders.
    
    24) nws_fire_weather_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Fire Weather Zone borders.
    
    25) nws_fire_weather_zones_zorder (Integer) - Default=3. The z-order of the NWS Fire Weather Zone borders. 
       For NWS Fire Weather Zone borders to be displayed the following condition must be met: nws_fire_weather_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    26) show_nws_cwa (Boolean) - Default=False. When set to True, NWS CWA borders are shown.
    
    27) nws_cwa_color (String) - Default='black'. The color of the NWS CWA borders.
    
    28) nws_cwa_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS CWA borders.
    
    29) nws_cwa_zorder (Integer) - Default=3. The z-order of the NWS CWA borders. 
       For NWS CWA borders to be displayed the following condition must be met: nws_cwa_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    30) show_calfire_boundaries (Boolean) - Default=False. When set to True, CalFire borders are shown.
    
    31) calfire_boundary_color (String) - Default='black'. The color of the CalFire borders.
    
    32) calfire_boundary_linewidth (Float or Integer) - Default=0.25. The linewidth of the CalFire borders.
    
    33) calfire_boundary_zorder (Integer) - Default=3. The z-order of the CalFire borders. 
       For CalFire borders to be displayed the following condition must be met: calfire_boundary_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.

    34) custom_shapefile_url (String or None) - Default=None. If the user wishes to set up an automation importing geometry from a shapefile that
        is not in the base version of FireWxPy, this is how to do that. The user will pass the download URL as a string by setting
        custom_shapefile_url='https"//shapefile_download_url.file_extension'. 
        
    35) custom_shapefile_file_extension (String) - Default='.zip'. This is the file extension of the zipped shapefile folder on the web
        server. 
        
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    36) custom_shapefile_color (String) - Default='black'. The color of the borders in the custom shapefile.
    
    37) custom_shapefile_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders in the custom shapefile.
    
    38) custom_shapefile_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    39) custom_geojson_url (String) - Default=None. If the user wishes to set up an automation with a publicly available
        geojson on the web, pass in the full download URL into this argument.
    
    40) custom_geojson_filename (String) - Default=None. The filename of the custom geojson file. 
    
    41) custom_geojson_folder_name (String) Default='Custom GeoJSON'. The folder where the custom geojson will be saved in.
    
    42) custom_geojson_color (String) - Default='black'. The edge color of the geometries in the custom geojson file.
    
    43) custom_geojson_linewidth (Integer or Float) - Default=0.5. The linewidth of the borders in the custom geojson. 
    
    44) custom_geojson_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    45) custom_shapefile_local_path (String) - Default=None. The path to a shapefile locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    46) custom_shapefile_local_color (String) - Default='black'. The edge color of the geometries in the shapefile.
    
    47) custom_shapefile_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    48) custom_shapefile_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    49) custom_geojson_local_path (String) - Default=None. The path to a geojson locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    50) custom_geojson_local_color (String) - Default='black'. The edge color of the geometries in the geojson.
    
    51) custom_geojson_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    52) custom_geojson_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    53) convert_custom_shapefile_crs (Boolean)- Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom shapefile. 
        
    54) convert_local_custom_shapefile_crs (Boolean) - Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom geojson.
        
    55)  refresh_cartographic_files (Boolean) - Default=True. Users that have automated pipelines set up for shapefiles. Having this set to
        True allows the client to delete and re-download the shapefiles with each run of the script. This is useful for shapefiles
        that have frequent geometry updates.
        
    56) reference_system (String) - Default='States & Counties'. The name of the borders overlaid onto the map.
    
    57) show_rivers (Boolean) - Default=False. Set to True to display rivers. 
    
    58) rivers_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    59) rivers_color (String) - Default='lightcyan'. The color of the river. 
    
    60) figure_x_length (Integer) - Default=12. The length of the figure in the x-direction.
    
    61) figure_y_length (Integer) - Default=12. The length of the figure in the y-direction.
    
    62) coastline_linewidth (Float or Integer) - Default=0.75. The linewidth of the coastline.
    
    63) land_color (String) - Default='beige'. The color of the land on a map.
    
    64) ocean_color (String) - Default='lightcyan'. The color of the ocean on a map.
    
    65) lakes_color (String) - Default='lightcyan'. The color of lakes on a map. 

    66) costline_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    67) ocean_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    68) lakes_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    69) land_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    70) decimate (Integer) - Default=50. This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. When set to 50, every 50 values will be queried. Use
        larger numbers for larger areas and smaller values for smaller areas. The default of 50 represents the setting for
        CONUS. 
        
    71) start (Integer) - Default=-30. The start of the filled contour range.
    
    72) stop (Integer) - Default=130. The end of the filled contour range. 
    
    73) step (Integer) - Default=1. The interval of the filled contours.
    
    74) facecolor (String) - Default='aliceblue'. The background color of the graphic. 
    
    75) primary_title_text (String) - Default='RTMA 2-METER TEMPERATURE [°F]'. The primary title
        of the graphic. 
        
    76) primary_title_textbox_color (String) - Default='wheat'. The color of the textbox of the primary title.
    
    77) primary_title_textbox_style (String) - Default='round'. The style of the textbox of the primary title.
    
    78) primary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    79) secondary_title_textbox_color (Float or Integer) Default='wheat'. The color of the textbox of the secondary title.
        
    80) secondary_title_textbox_style (String) - Default='round'. The style of the textbox of the secondary title.
    
    81) secondary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    82) primary_title_fontsize (Integer) - Default=12. Fontsize of the primary title text.
    
    83) secondary_title_fontsize (Integer) Default=10. Fontsize of the secondary title text.
    
    84) local_time (Boolean) - Default=True. Set to False for UTC time.
    
    85) signature_textbox_color (String) - Default='wheat'. The color of the textbox of the graphic's signature.
    
    86) signature_textbox_style (String) - Default='round'. The style of the textbox of the graphic's signature.
    
    87) signature_textbox_alpha (Float or Integer) - Default=1. A value between 0.5 and 1 representing transparency.

    88) signature_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    89) signature_fontsize (Integer) - Default=8. Fontsize of the graphic's signature text.
    
    90) signature_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the signature text box.
    
    91) signature_textbox_y_position (Float) - Default=-0.175. The y-position with respect to the plot axis of the signature text box.
    
    92) signature_text_new_lines (Boolean) - Default=False. When set to True, each section in the signature is on a new line.
        It is recommended to set this to True on plots that are longer from North to South than West to East. 
        
    93) reference_system_textbox_color (String) - Default='wheat'. The color of the textbox of the reference system.
    
    94) reference_system_textbox_style (String) - Default='round'. The style of the textbox of the reference system.
    
    95) reference_system_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    96) reference_system_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    97) reference_system_fontsize (Integer) - Default=6. Fontsize of the reference system label text.
    
    98) reference_system_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the reference system text box.
    
    99) reference_system_textbox_y_position (Float) - Default=0. The y-position with respect to the plot axis of the reference system text box.

    100) colorbar_shrink (Float or Integer) - Default=1. Fraction by which to multiply the size of the colorbar.
    
    101) colorbar_pad (Float) - Default=0.01. Fraction of original Axes between colorbar and new image Axes.
    
    102) tick_label_fontsize (Integer) - Default=9. The fontsize of the colorbar tick labels.
    
    103) colorbar_location (String) - Default='bottom'. The side of the plot axis where the colorbar will be displayed.
    
    104) colorbar_interval (Integer) - Default=10. The interval of tick marks on the colorbar.
    
    105) colorbar_aspect (Integer) - Default=50. Ratio of long to short dimensions.
    
    106) colormap (String) - Default='jet'. The Matplotlib colormap for filled contours being used OR set to 'custom' to create your own 
        custom colormapping. See the optional colors argument documentation (109) for more information on how to pass
        in a custom array of colors. 
        
    107) contourf_alpha (Float or Integer) - Default=0.5. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    108) contourf_zorder (Integer) - Default=2. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    109) colors (String List) - Default=['magenta',
                                        'orchid',
                                        'plum',
                                        'darkviolet',
                                        'darkslateblue',
                                        'blue',
                                        'cyan',
                                        'lawngreen',
                                        'greenyellow',
                                        'olive',
                                        'gold',
                                        'goldenrod',
                                        'darkorange',
                                        'deeppink',
                                        'crimson',
                                        'darkred',
                                        'grey']
                                        
            The array of colors being used when colormap='custom'. 
            
    110) ds (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds=ds. 
            
    111) western_bound (Float or Integer) - Default=-125. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    112) eastern_bound (Float or Integer) - Default=-65. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    113) southern_bound (Float or Integer) - Default=20. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    114) northern_bound (Float or Integer) - Default=50. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    115) pixel_query_value_fontsize (Integer) - Default=4. The fontsize of the pixel query values.
    
    116) pixel_query_value_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    117) pixel_query_value_foreground (String) - Default='white'. The color of the foreground on the station plot (pixel query value).
    
    118) pixel_query_value_fontcolor (String) - Default='black'. The font color of the pixel query values.
    
    119) pixel_query_stroke_linewidth (Float or Integer) - Default=1. The linewidth of the pixel query values text outline.
    
    120) path (String) - Default='FireWxPy Graphics/RTMA/Temperature'. The directory where the graphic will save.
    
    121) filename (String) - Default='RTMA Temperature.png'. The filename of the image.
    
    122) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    123) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
        
    124) clear_data (Boolean) - Default=True. When set to True, the data will be cleared with each run of the script.
        Set to False when downloading the data outside of the function and passing the data in. 
        
    125) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB data to a file.
    
    126) notifications (String) - Default='off'. Notifications throughout the process. 

    127) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    128) convert_from (String) - Default='kelvin'. Units we are converting from. (Only needed if not using WxData to download and process the data).
    
    129) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 

    130) custom_data_directory (String or None) - Default=None. The directory path where the data will be saved to. 

    131) mapcrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the map.
    
    132) datacrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the data.

    133) var_key (String) - Default='2m_temperature'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    134) time_coord_key (String) - Default='time'. The time coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    135) longitude_key (String) - Default='longitude'. The longitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
    
    136) latitude_key (String) - Default='latitude'. The latitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.

    Returns
    -------
    
    An image of the RTMA Temperature Analysis specified to the user's needs saved to {path}    
    """    
    
    _build_directory_branch(f"{path}/{region.upper()}/{reference_system.upper()}")
    
    _mpl.rcParams['xtick.labelsize'] = tick_label_fontsize
    _mpl.rcParams['ytick.labelsize'] = tick_label_fontsize
    
    primary_title_box = dict(boxstyle=primary_title_textbox_style, 
                            facecolor=primary_title_textbox_color, 
                            alpha=primary_title_textbox_alpha)
    
    secondary_title_box = dict(boxstyle=secondary_title_textbox_style, 
                            facecolor=secondary_title_textbox_color, 
                            alpha=secondary_title_textbox_alpha)
    
    signature_box = dict(boxstyle=signature_textbox_style, 
                            facecolor=signature_textbox_color, 
                            alpha=signature_textbox_alpha)
    
    reference_system_box = dict(boxstyle=reference_system_textbox_style, 
                            facecolor=reference_system_textbox_color, 
                            alpha=reference_system_textbox_alpha)
    
    levels = _np.arange(start, (stop + step), step)
    ticks = levels[::colorbar_interval]
    
    western_bound, eastern_bound, southern_bound, northern_bound = _bounding_box(region,
                                                                                 western_bound,
                                                                                 eastern_bound,
                                                                                 southern_bound,
                                                                                 northern_bound)
    
    if ds is None:
        ds = _rtma(proxies=proxies,
                   clear_recycle_bin=clear_recycle_bin,
                   clear_data=clear_data,
                   western_bound=western_bound,
                   eastern_bound=eastern_bound,
                   southern_bound=southern_bound,
                   northern_bound=northern_bound,
                   convert_temperature=convert_temperature,
                   convert_to=convert_to,
                   chunk_size=chunk_size,
                   notifications=notifications,
                   custom_directory=custom_data_directory)
    else:
        ds = ds
        if convert_temperature is True:
            if convert_from == 'kelvin':
                if convert_to == 'fahrenheit':
                    ds[var_key] = _kelvin_to_fahrenheit(ds[var_key])
                else:
                    ds[var_key] = _kelvin_to_celsius(ds[var_key])
            else:
                if convert_to == 'fahrenheit':
                    ds[var_key] = _celsius_to_fahrenheit(ds[var_key])
        
    if colormap == 'custom':
        cmap = _mcolors.LinearSegmentedColormap.from_list("temperature", colors)
    else:
        cmap = colormap
    
    valid_time = _pd.to_datetime(ds[time_coord_key].to_pandas())
    valid_time = valid_time.tz_localize('UTC')
    time = valid_time.astimezone(_to_zone)
    time_utc = time.astimezone(_from_zone)
    
    fig = _plt.figure(figsize=(figure_x_length, figure_y_length))
    fig.set_facecolor(facecolor)
    
    ax = fig.add_subplot(1,1,1, projection=mapcrs)
    ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax.add_feature(_cfeature.COASTLINE.with_scale('50m'), linewidth=coastline_linewidth, zorder=costline_zorder)
    ax.add_feature(_cfeature.LAND, color=land_color, zorder=land_zorder)
    ax.add_feature(_cfeature.OCEAN, color=ocean_color, zorder=ocean_zorder)
    ax.add_feature(_cfeature.LAKES, color=lakes_color, zorder=lakes_zorder)
    if show_rivers is True:
        ax.add_feature(_cfeature.RIVERS, color=rivers_color, zorder=rivers_zorder)
    if show_states is True:
        states = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_States_Territories.zip",
                                            f"Cartographic Files/US States",
                                            f"US_States_Territories.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            state_border_color,
                                            datacrs)
        
        ax.add_geometries(states, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=state_border_color, 
                          linewidth=state_border_linewidth, 
                          zorder=state_border_zorder)
    
    if show_counties is True:
        counties = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_Counties.zip",
                                            f"Cartographic Files/US Counties",
                                            f"US_Counties.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            county_border_color,
                                            datacrs)
        
        ax.add_geometries(counties, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=county_border_color, 
                          linewidth=county_border_linewidth, 
                          zorder=county_border_zorder)
        
    if show_gacc_boundaries is True:
        gacc = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/GACC_Boundaries_2026.zip",
                                            f"Cartographic Files/GACC Boundaries",
                                            f"GACC_Boundaries_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            gacc_border_color,
                                            datacrs)
        
        ax.add_geometries(gacc, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=gacc_border_color, 
                          linewidth=gacc_border_linewidth, 
                          zorder=gacc_border_zorder)
    
    if show_predictive_services_areas is True:
        psa = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/PSA_Boundaries.zip",
                                            f"Cartographic Files/PSA Boundaries",
                                            f"PSA_Boundaries.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            predictive_services_areas_color,
                                            datacrs)
        
        ax.add_geometries(psa, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=predictive_services_areas_color, 
                          linewidth=predictive_services_areas_linewidth, 
                          zorder=predictive_services_areas_zorder)
        
    if show_nws_public_zones is True:
        pz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Public_Zones_2026.zip",
                                            f"Cartographic Files/NWS Public Zones",
                                            f"NWS_Public_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_public_zones_color,
                                            datacrs)
        
        ax.add_geometries(pz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_public_zones_color, 
                          linewidth=nws_public_zones_linewidth, 
                          zorder=nws_public_zones_zorder)
        
    if show_nws_fire_weather_zones is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Fire_Weather_Zones_2026.zip",
                                            f"Cartographic Files/NWS Fire Weather Zones",
                                            f"NWS_Fire_Weather_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_fire_weather_zones_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_fire_weather_zones_color, 
                          linewidth=nws_fire_weather_zones_linewidth, 
                          zorder=nws_fire_weather_zones_zorder)
        
    if show_nws_cwa is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_CWA_2026.zip",
                                            f"Cartographic Files/NWS CWAs",
                                            f"NWS_CWA_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_cwa_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_cwa_color, 
                          linewidth=nws_cwa_linewidth, 
                          zorder=nws_cwa_zorder)
        
    if show_calfire_boundaries is True:
        calfire = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/CALFIRE/CalFire_Administrative_Units.zip",
                                            f"Cartographic Files/CalFire",
                                            f"CalFire_Administrative_Units.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            calfire_boundary_color,
                                            datacrs,
                                            convert_crs=True,
                                            convert_to='EPSG:4326')
        
        ax.add_geometries(calfire, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=calfire_boundary_color, 
                          linewidth=calfire_boundary_linewidth, 
                          zorder=calfire_boundary_zorder)
        
    if custom_shapefile_url is not None:
        
        fname = _get_filename_from_url(custom_shapefile_url)
        
        custom_shape = _import_shapefile_from_web(custom_shapefile_url,
                                            f"Cartographic Files/{custom_shapefile_folder_name}",
                                            fname,
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            custom_shapefile_file_extension,
                                            custom_shapefile_color,
                                            convert_crs=convert_custom_shapefile_crs)
        
        ax.add_geometries(custom_shape, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_color, 
                          linewidth=custom_shapefile_linewidth, 
                          zorder=custom_shapefile_zorder)
        
    if custom_geojson_url is not None:
        
        custom_json = _import_geojson_from_web(custom_geojson_url,
                                                f"Cartographic Files/{custom_geojson_folder_name}", 
                                                custom_geojson_filename, 
                                                proxies, 
                                                chunk_size,
                                                notifications, 
                                                refresh_cartographic_files)
        
        ax.add_geometries(custom_json, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_color, 
                          linewidth=custom_geojson_linewidth, 
                          zorder=custom_geojson_zorder)
        
    if custom_shapefile_local_path is not None:
        custom_local_shapefile = _import_shapefile_local(custom_shapefile_local_path,
                                                            custom_shapefile_local_color,
                                                            convert_crs=convert_local_custom_shapefile_crs)
        
        ax.add_geometries(custom_local_shapefile, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_local_color, 
                          linewidth=custom_shapefile_local_linewidth, 
                          zorder=custom_shapefile_local_zorder)
        
    if custom_geojson_local_path is not None:
        custom_local_geojson = _import_geojson_local(custom_geojson_local_path)
        
        ax.add_geometries(custom_local_geojson, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_local_color, 
                          linewidth=custom_geojson_local_linewidth, 
                          zorder=custom_geojson_local_zorder)
    
    cs = ax.contourf(ds[longitude_key],
                ds[latitude_key],
                ds[var_key],
                cmap=cmap,
                levels=levels,
                transform=datacrs,
                alpha=contourf_alpha,
                zorder=contourf_zorder,
                extend='both')
    
    fig.colorbar(cs, 
                shrink=colorbar_shrink, 
                pad=colorbar_pad, 
                location=colorbar_location,
                ticks=ticks,
                aspect=colorbar_aspect)
    
    _plt.title(f"{primary_title_text}", 
               fontsize=primary_title_fontsize, 
               fontweight='bold',
               bbox=primary_title_box,
               loc='left')
    
    if local_time is True:
        _plt.title(f"Valid: {time.strftime('%m/%d/%Y %H:00')} {_timezone}", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
    else:
        _plt.title(f"Valid: {time_utc.strftime('%m/%d/%Y %H:00')} UTC", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
        
    if signature_text_new_lines is False:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')} | Data Source: NCEP/NOMADS | Created: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    else:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')}\nData Source: NCEP/NOMADS\nCreated: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    
    ax.text(reference_system_textbox_x_position, 
            reference_system_textbox_y_position,
            f"Reference System: {reference_system}",
            fontsize=reference_system_fontsize,
            fontweight='bold',
            bbox=reference_system_box,
            transform=ax.transAxes,
            zorder=reference_system_textbox_zorder)
        
    
    vals = _fix_var_array(ds,
                    var_key,
                    0,
                    decimate)

    stn = _mpplots.StationPlot(ax, vals['longitude'], vals['latitude'],
                                transform=datacrs, 
                                fontsize=pixel_query_value_fontsize, 
                                zorder=pixel_query_value_zorder, 
                                clip_on=True)


    stn.plot_parameter('C', 
                       vals[var_key], 
                       color=pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)

  
    fig.savefig(f"{path}/{region.upper()}/{reference_system.upper()}/{filename}", bbox_inches='tight')
    _plt.close(fig)
    if notifications == 'on':
        print(f"{filename} saved to {path}/{region.upper()}")
        
        
def plot_dew_point(region='conus',
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=50,
                     start=-20,
                     stop=80,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER DEW POINT [°F]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=12,
                     secondary_title_fontsize=10,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=10,
                     colorbar_aspect=50,
                     colormap='terrain_r',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['saddlebrown',
                             'peru',
                             'darkorange',
                             'gold',
                             'olive',
                             'olivedrab',
                             'chartreuse',
                             'lime',
                             'forestgreen',
                             'mediumspringgreen',
                             'aqua'],
                     ds=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=4,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA/Dew Point',
                     filename='RTMA Dew Point.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     convert_temperature=True,
                     convert_from='kelvin',
                     convert_to='fahrenheit',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     var_key='2m_dew_point',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude'):
    
    """
    This function plots the latest Real Time Mesoscale Analysis (RTMA) for dew point.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Entire CONUS region.
            ii) 'terrain_r' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Required Arguments: None
    
    Optional Arguments:
    
    1) region (String) - Default='conus'. The region of the plot. Use the 2-letter state abbreviation or 4-letter GACC abbreviation.
        If the user wants a completely custom region where they define their own lat/lon bounds, set region='custom'. 
        
    2) show_states (Boolean) - Default=True. When set to True, U.S. state borders are shown. 
    
    3) state_border_color (String) - Default='black'. The color of the U.S. state borders.
    
    4) state_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the U.S. state borders.
    
    5) state_border_zorder (Integer) - Default=3. The z-order of the state borders. For state borders to be displayed
        the following condition must be met: state_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
        
    6) show_counties (Boolean) - Default=True. When set to True, U.S. county borders are shown. 
    
    7) county_border_color (String) - Default='black'. The color of the U.S. county borders.
    
    8) county_border_linewidth (Float or Integer) - Default=0.25. The linewidth of the U.S. county borders.
    
    9) county_border_zorder (Integer) - Default=3. The z-order of the county borders. For county borders to be displayed
        the following condition must be met: county_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
    
    10) show_gacc_boundaries (Boolean) - Default=False. When set to True, Geographic Area Coordination Center borders are shown. 
    
    11) gacc_border_color (String) - Default='black'. The color of the Geographic Area Coordination Center borders.
    
    12) gacc_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the Geographic Area Coordination Center borders.
    
    13) gacc_border_zorder (Integer) - Default=3. The z-order of the Geographic Area Coordination Center borders. 
       For Geographic Area Coordination Center borders to be displayed the following condition must be met: gacc_border_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
       
    14) show_predictive_services_areas (Boolean) - Default=False. When set to True, Predictive Services Areas borders are shown. 
    
    15) predictive_services_areas_color (String) - Default='black'. The color of the Predictive Services Areas borders.
    
    16) predictive_services_areas_linewidth (Float or Integer) - Default=0.25. The linewidth of the Predictive Services Areas borders.
    
    17) predictive_services_areas_zorder (Integer) - Default=3. The z-order of the Predictive Services Areas borders. 
       For Predictive Services Areas borders to be displayed the following condition must be met: predictive_services_areas_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    18) show_nws_public_zones (Boolean) - Default=False. When set to True, NWS Public Zone borders are shown. 
    
    19) nws_public_zones_color (String) - Default='black'. The color of the NWS Public Zone borders.
    
    20) nws_public_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Public Zone borders.
    
    21) nws_public_zones_zorder (Integer) - Default=3. The z-order of the NWS Public Zone borders. 
       For NWS Public Zone borders to be displayed the following condition must be met: nws_public_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    22) show_nws_fire_weather_zones (Boolean) - Default=False. When set to True, NWS Fire Weather Zone borders are shown. 
    
    23) nws_fire_weather_zones_color (String) - Default='black'. The color of the NWS Fire Weather Zone borders.
    
    24) nws_fire_weather_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Fire Weather Zone borders.
    
    25) nws_fire_weather_zones_zorder (Integer) - Default=3. The z-order of the NWS Fire Weather Zone borders. 
       For NWS Fire Weather Zone borders to be displayed the following condition must be met: nws_fire_weather_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    26) show_nws_cwa (Boolean) - Default=False. When set to True, NWS CWA borders are shown.
    
    27) nws_cwa_color (String) - Default='black'. The color of the NWS CWA borders.
    
    28) nws_cwa_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS CWA borders.
    
    29) nws_cwa_zorder (Integer) - Default=3. The z-order of the NWS CWA borders. 
       For NWS CWA borders to be displayed the following condition must be met: nws_cwa_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    30) show_calfire_boundaries (Boolean) - Default=False. When set to True, CalFire borders are shown.
    
    31) calfire_boundary_color (String) - Default='black'. The color of the CalFire borders.
    
    32) calfire_boundary_linewidth (Float or Integer) - Default=0.25. The linewidth of the CalFire borders.
    
    33) calfire_boundary_zorder (Integer) - Default=3. The z-order of the CalFire borders. 
       For CalFire borders to be displayed the following condition must be met: calfire_boundary_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.

    34) custom_shapefile_url (String or None) - Default=None. If the user wishes to set up an automation importing geometry from a shapefile that
        is not in the base version of FireWxPy, this is how to do that. The user will pass the download URL as a string by setting
        custom_shapefile_url='https"//shapefile_download_url.file_extension'. 
        
    35) custom_shapefile_file_extension (String) - Default='.zip'. This is the file extension of the zipped shapefile folder on the web
        server. 
        
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    36) custom_shapefile_color (String) - Default='black'. The color of the borders in the custom shapefile.
    
    37) custom_shapefile_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders in the custom shapefile.
    
    38) custom_shapefile_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    39) custom_geojson_url (String) - Default=None. If the user wishes to set up an automation with a publicly available
        geojson on the web, pass in the full download URL into this argument.
    
    40) custom_geojson_filename (String) - Default=None. The filename of the custom geojson file. 
    
    41) custom_geojson_folder_name (String) Default='Custom GeoJSON'. The folder where the custom geojson will be saved in.
    
    42) custom_geojson_color (String) - Default='black'. The edge color of the geometries in the custom geojson file.
    
    43) custom_geojson_linewidth (Integer or Float) - Default=0.5. The linewidth of the borders in the custom geojson. 
    
    44) custom_geojson_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    45) custom_shapefile_local_path (String) - Default=None. The path to a shapefile locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    46) custom_shapefile_local_color (String) - Default='black'. The edge color of the geometries in the shapefile.
    
    47) custom_shapefile_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    48) custom_shapefile_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    49) custom_geojson_local_path (String) - Default=None. The path to a geojson locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    50) custom_geojson_local_color (String) - Default='black'. The edge color of the geometries in the geojson.
    
    51) custom_geojson_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    52) custom_geojson_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    53) convert_custom_shapefile_crs (Boolean)- Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom shapefile. 
        
    54) convert_local_custom_shapefile_crs (Boolean) - Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom geojson.
        
    55)  refresh_cartographic_files (Boolean) - Default=True. Users that have automated pipelines set up for shapefiles. Having this set to
        True allows the client to delete and re-download the shapefiles with each run of the script. This is useful for shapefiles
        that have frequent geometry updates.
        
    56) reference_system (String) - Default='States & Counties'. The name of the borders overlaid onto the map.
    
    57) show_rivers (Boolean) - Default=False. Set to True to display rivers. 
    
    58) rivers_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    59) rivers_color (String) - Default='lightcyan'. The color of the river. 
    
    60) figure_x_length (Integer) - Default=12. The length of the figure in the x-direction.
    
    61) figure_y_length (Integer) - Default=12. The length of the figure in the y-direction.
    
    62) coastline_linewidth (Float or Integer) - Default=0.75. The linewidth of the coastline.
    
    63) land_color (String) - Default='beige'. The color of the land on a map.
    
    64) ocean_color (String) - Default='lightcyan'. The color of the ocean on a map.
    
    65) lakes_color (String) - Default='lightcyan'. The color of lakes on a map. 

    66) costline_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    67) ocean_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    68) lakes_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    69) land_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    70) decimate (Integer) - Default=50. This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. When set to 50, every 50 values will be queried. Use
        larger numbers for larger areas and smaller values for smaller areas. The default of 50 represents the setting for
        CONUS. 
        
    71) start (Integer) - Default=-30. The start of the filled contour range.
    
    72) stop (Integer) - Default=80. The end of the filled contour range. 
    
    73) step (Integer) - Default=1. The interval of the filled contours.
    
    74) facecolor (String) - Default='aliceblue'. The background color of the graphic. 
    
    75) primary_title_text (String) - Default='RTMA 2-METER DEW POINT [°F]'. The primary title
        of the graphic. 
        
    76) primary_title_textbox_color (String) - Default='wheat'. The color of the textbox of the primary title.
    
    77) primary_title_textbox_style (String) - Default='round'. The style of the textbox of the primary title.
    
    78) primary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    79) secondary_title_textbox_color (Float or Integer) Default='wheat'. The color of the textbox of the secondary title.
        
    80) secondary_title_textbox_style (String) - Default='round'. The style of the textbox of the secondary title.
    
    81) secondary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    82) primary_title_fontsize (Integer) - Default=12. Fontsize of the primary title text.
    
    83) secondary_title_fontsize (Integer) Default=10. Fontsize of the secondary title text.
    
    84) local_time (Boolean) - Default=True. Set to False for UTC time.
    
    85) signature_textbox_color (String) - Default='wheat'. The color of the textbox of the graphic's signature.
    
    86) signature_textbox_style (String) - Default='round'. The style of the textbox of the graphic's signature.
    
    87) signature_textbox_alpha (Float or Integer) - Default=1. A value between 0.5 and 1 representing transparency.

    88) signature_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    89) signature_fontsize (Integer) - Default=8. Fontsize of the graphic's signature text.
    
    90) signature_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the signature text box.
    
    91) signature_textbox_y_position (Float) - Default=-0.175. The y-position with respect to the plot axis of the signature text box.
    
    92) signature_text_new_lines (Boolean) - Default=False. When set to True, each section in the signature is on a new line.
        It is recommended to set this to True on plots that are longer from North to South than West to East. 
        
    93) reference_system_textbox_color (String) - Default='wheat'. The color of the textbox of the reference system.
    
    94) reference_system_textbox_style (String) - Default='round'. The style of the textbox of the reference system.
    
    95) reference_system_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    96) reference_system_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    97) reference_system_fontsize (Integer) - Default=6. Fontsize of the reference system label text.
    
    98) reference_system_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the reference system text box.
    
    99) reference_system_textbox_y_position (Float) - Default=0. The y-position with respect to the plot axis of the reference system text box.

    100) colorbar_shrink (Float or Integer) - Default=1. Fraction by which to multiply the size of the colorbar.
    
    101) colorbar_pad (Float) - Default=0.01. Fraction of original Axes between colorbar and new image Axes.
    
    102) tick_label_fontsize (Integer) - Default=9. The fontsize of the colorbar tick labels.
    
    103) colorbar_location (String) - Default='bottom'. The side of the plot axis where the colorbar will be displayed.
    
    104) colorbar_interval (Integer) - Default=10. The interval of tick marks on the colorbar.
    
    105) colorbar_aspect (Integer) - Default=50. Ratio of long to short dimensions.
    
    106) colormap (String) - Default='terrain_r'. The Matplotlib colormap for filled contours being used OR set to 'custom' to create your own 
        custom colormapping. See the optional colors argument documentation (109) for more information on how to pass
        in a custom array of colors. 
        
    107) contourf_alpha (Float or Integer) - Default=0.5. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    108) contourf_zorder (Integer) - Default=2. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    109) colors (String List) - Default=['saddlebrown',
                                        'peru',
                                        'darkorange',
                                        'gold',
                                        'olive',
                                        'olivedrab',
                                        'chartreuse',
                                        'lime',
                                        'forestgreen',
                                        'mediumspringgreen',
                                        'aqua']
                                        
            The array of colors being used when colormap='custom'. 
            
    110) ds (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds=ds. 
            
    111) western_bound (Float or Integer) - Default=-125. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    112) eastern_bound (Float or Integer) - Default=-65. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    113) southern_bound (Float or Integer) - Default=20. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    114) northern_bound (Float or Integer) - Default=50. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    115) pixel_query_value_fontsize (Integer) - Default=4. The fontsize of the pixel query values.
    
    116) pixel_query_value_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    117) pixel_query_value_foreground (String) - Default='white'. The color of the foreground on the station plot (pixel query value).
    
    118) pixel_query_value_fontcolor (String) - Default='black'. The font color of the pixel query values.
    
    119) pixel_query_stroke_linewidth (Float or Integer) - Default=1. The linewidth of the pixel query values text outline.
    
    120) path (String) - Default='FireWxPy Graphics/RTMA/Dew Point'. The directory where the graphic will save.
    
    121) filename (String) - Default='RTMA Dew Point.png'. The filename of the image.
    
    122) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    123) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
        
    124) clear_data (Boolean) - Default=True. When set to True, the data will be cleared with each run of the script.
        Set to False when downloading the data outside of the function and passing the data in. 
        
    125) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB data to a file.
    
    126) notifications (String) - Default='off'. Notifications throughout the process. 

    127) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    128) convert_from (String) - Default='kelvin'. Units we are converting from. (Only needed if not using WxData to download and process the data).
    
    129) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 

    130) custom_data_directory (String or None) - Default=None. The directory path where the data will be saved to. 

    131) mapcrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the map.
    
    132) datacrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the data.

    133) var_key (String) - Default='2m_dew_point'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    134) time_coord_key (String) - Default='time'. The time coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    135) longitude_key (String) - Default='longitude'. The longitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
    
    136) latitude_key (String) - Default='latitude'. The latitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.

    Returns
    -------
    
    An image of the RTMA Dew Point Analysis specified to the user's needs saved to {path}    
    """    
    
    _build_directory_branch(f"{path}/{region.upper()}/{reference_system.upper()}")
    
    _mpl.rcParams['xtick.labelsize'] = tick_label_fontsize
    _mpl.rcParams['ytick.labelsize'] = tick_label_fontsize
    
    primary_title_box = dict(boxstyle=primary_title_textbox_style, 
                            facecolor=primary_title_textbox_color, 
                            alpha=primary_title_textbox_alpha)
    
    secondary_title_box = dict(boxstyle=secondary_title_textbox_style, 
                            facecolor=secondary_title_textbox_color, 
                            alpha=secondary_title_textbox_alpha)
    
    signature_box = dict(boxstyle=signature_textbox_style, 
                            facecolor=signature_textbox_color, 
                            alpha=signature_textbox_alpha)
    
    reference_system_box = dict(boxstyle=reference_system_textbox_style, 
                            facecolor=reference_system_textbox_color, 
                            alpha=reference_system_textbox_alpha)
    
    levels = _np.arange(start, (stop + step), step)
    ticks = levels[::colorbar_interval]
    
    western_bound, eastern_bound, southern_bound, northern_bound = _bounding_box(region,
                                                                                 western_bound,
                                                                                 eastern_bound,
                                                                                 southern_bound,
                                                                                 northern_bound)
    
    if ds is None:
        ds = _rtma(proxies=proxies,
                   clear_recycle_bin=clear_recycle_bin,
                   clear_data=clear_data,
                   western_bound=western_bound,
                   eastern_bound=eastern_bound,
                   southern_bound=southern_bound,
                   northern_bound=northern_bound,
                   convert_temperature=convert_temperature,
                   convert_to=convert_to,
                   chunk_size=chunk_size,
                   notifications=notifications,
                   custom_directory=custom_data_directory)
    else:
        ds = ds
        if convert_temperature is True:
            if convert_from == 'kelvin':
                if convert_to == 'fahrenheit':
                    ds[var_key] = _kelvin_to_fahrenheit(ds[var_key])
                else:
                    ds[var_key] = _kelvin_to_celsius(ds[var_key])
            else:
                if convert_to == 'fahrenheit':
                    ds[var_key] = _celsius_to_fahrenheit(ds[var_key])
        
    if colormap == 'custom':
        cmap = _mcolors.LinearSegmentedColormap.from_list("dew point", colors)
    else:
        cmap = colormap
    
    valid_time = _pd.to_datetime(ds[time_coord_key].to_pandas())
    valid_time = valid_time.tz_localize('UTC')
    time = valid_time.astimezone(_to_zone)
    time_utc = time.astimezone(_from_zone)
    
    fig = _plt.figure(figsize=(figure_x_length, figure_y_length))
    fig.set_facecolor(facecolor)
    
    ax = fig.add_subplot(1,1,1, projection=mapcrs)
    ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax.add_feature(_cfeature.COASTLINE.with_scale('50m'), linewidth=coastline_linewidth, zorder=costline_zorder)
    ax.add_feature(_cfeature.LAND, color=land_color, zorder=land_zorder)
    ax.add_feature(_cfeature.OCEAN, color=ocean_color, zorder=ocean_zorder)
    ax.add_feature(_cfeature.LAKES, color=lakes_color, zorder=lakes_zorder)
    if show_rivers is True:
        ax.add_feature(_cfeature.RIVERS, color=rivers_color, zorder=rivers_zorder)
    if show_states is True:
        states = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_States_Territories.zip",
                                            f"Cartographic Files/US States",
                                            f"US_States_Territories.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            state_border_color,
                                            datacrs)
        
        ax.add_geometries(states, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=state_border_color, 
                          linewidth=state_border_linewidth, 
                          zorder=state_border_zorder)
    
    if show_counties is True:
        counties = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_Counties.zip",
                                            f"Cartographic Files/US Counties",
                                            f"US_Counties.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            county_border_color,
                                            datacrs)
        
        ax.add_geometries(counties, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=county_border_color, 
                          linewidth=county_border_linewidth, 
                          zorder=county_border_zorder)
        
    if show_gacc_boundaries is True:
        gacc = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/GACC_Boundaries_2026.zip",
                                            f"Cartographic Files/GACC Boundaries",
                                            f"GACC_Boundaries_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            gacc_border_color,
                                            datacrs)
        
        ax.add_geometries(gacc, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=gacc_border_color, 
                          linewidth=gacc_border_linewidth, 
                          zorder=gacc_border_zorder)
    
    if show_predictive_services_areas is True:
        psa = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/PSA_Boundaries.zip",
                                            f"Cartographic Files/PSA Boundaries",
                                            f"PSA_Boundaries.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            predictive_services_areas_color,
                                            datacrs)
        
        ax.add_geometries(psa, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=predictive_services_areas_color, 
                          linewidth=predictive_services_areas_linewidth, 
                          zorder=predictive_services_areas_zorder)
        
    if show_nws_public_zones is True:
        pz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Public_Zones_2026.zip",
                                            f"Cartographic Files/NWS Public Zones",
                                            f"NWS_Public_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_public_zones_color,
                                            datacrs)
        
        ax.add_geometries(pz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_public_zones_color, 
                          linewidth=nws_public_zones_linewidth, 
                          zorder=nws_public_zones_zorder)
        
    if show_nws_fire_weather_zones is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Fire_Weather_Zones_2026.zip",
                                            f"Cartographic Files/NWS Fire Weather Zones",
                                            f"NWS_Fire_Weather_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_fire_weather_zones_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_fire_weather_zones_color, 
                          linewidth=nws_fire_weather_zones_linewidth, 
                          zorder=nws_fire_weather_zones_zorder)
        
    if show_nws_cwa is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_CWA_2026.zip",
                                            f"Cartographic Files/NWS CWAs",
                                            f"NWS_CWA_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_cwa_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_cwa_color, 
                          linewidth=nws_cwa_linewidth, 
                          zorder=nws_cwa_zorder)
        
    if show_calfire_boundaries is True:
        calfire = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/CALFIRE/CalFire_Administrative_Units.zip",
                                            f"Cartographic Files/CalFire",
                                            f"CalFire_Administrative_Units.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            calfire_boundary_color,
                                            datacrs,
                                            convert_crs=True,
                                            convert_to='EPSG:4326')
        
        ax.add_geometries(calfire, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=calfire_boundary_color, 
                          linewidth=calfire_boundary_linewidth, 
                          zorder=calfire_boundary_zorder)
        
    if custom_shapefile_url is not None:
        
        fname = _get_filename_from_url(custom_shapefile_url)
        
        custom_shape = _import_shapefile_from_web(custom_shapefile_url,
                                            f"Cartographic Files/{custom_shapefile_folder_name}",
                                            fname,
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            custom_shapefile_file_extension,
                                            custom_shapefile_color,
                                            convert_crs=convert_custom_shapefile_crs)
        
        ax.add_geometries(custom_shape, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_color, 
                          linewidth=custom_shapefile_linewidth, 
                          zorder=custom_shapefile_zorder)
        
    if custom_geojson_url is not None:
        
        custom_json = _import_geojson_from_web(custom_geojson_url,
                                                f"Cartographic Files/{custom_geojson_folder_name}", 
                                                custom_geojson_filename, 
                                                proxies, 
                                                chunk_size,
                                                notifications, 
                                                refresh_cartographic_files)
        
        ax.add_geometries(custom_json, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_color, 
                          linewidth=custom_geojson_linewidth, 
                          zorder=custom_geojson_zorder)
        
    if custom_shapefile_local_path is not None:
        custom_local_shapefile = _import_shapefile_local(custom_shapefile_local_path,
                                                            custom_shapefile_local_color,
                                                            convert_crs=convert_local_custom_shapefile_crs)
        
        ax.add_geometries(custom_local_shapefile, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_local_color, 
                          linewidth=custom_shapefile_local_linewidth, 
                          zorder=custom_shapefile_local_zorder)
        
    if custom_geojson_local_path is not None:
        custom_local_geojson = _import_geojson_local(custom_geojson_local_path)
        
        ax.add_geometries(custom_local_geojson, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_local_color, 
                          linewidth=custom_geojson_local_linewidth, 
                          zorder=custom_geojson_local_zorder)
    
    cs = ax.contourf(ds[longitude_key],
                ds[latitude_key],
                ds[var_key],
                cmap=cmap,
                levels=levels,
                transform=datacrs,
                alpha=contourf_alpha,
                zorder=contourf_zorder,
                extend='both')
    
    fig.colorbar(cs, 
                shrink=colorbar_shrink, 
                pad=colorbar_pad, 
                location=colorbar_location,
                ticks=ticks,
                aspect=colorbar_aspect)
    
    _plt.title(f"{primary_title_text}", 
               fontsize=primary_title_fontsize, 
               fontweight='bold',
               bbox=primary_title_box,
               loc='left')
    
    if local_time is True:
        _plt.title(f"Valid: {time.strftime('%m/%d/%Y %H:00')} {_timezone}", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
    else:
        _plt.title(f"Valid: {time_utc.strftime('%m/%d/%Y %H:00')} UTC", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
        
    if signature_text_new_lines is False:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')} | Data Source: NCEP/NOMADS | Created: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    else:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')}\nData Source: NCEP/NOMADS\nCreated: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    
    ax.text(reference_system_textbox_x_position, 
            reference_system_textbox_y_position,
            f"Reference System: {reference_system}",
            fontsize=reference_system_fontsize,
            fontweight='bold',
            bbox=reference_system_box,
            transform=ax.transAxes,
            zorder=reference_system_textbox_zorder)
        
    vals = _fix_var_array(ds,
                    var_key,
                    0,
                    decimate)

    stn = _mpplots.StationPlot(ax, vals['longitude'], vals['latitude'],
                                transform=datacrs, 
                                fontsize=pixel_query_value_fontsize, 
                                zorder=pixel_query_value_zorder, 
                                clip_on=True)


    stn.plot_parameter('C', 
                       vals[var_key], 
                       color=pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)
    
    fig.savefig(f"{path}/{region.upper()}/{reference_system.upper()}/{filename}", bbox_inches='tight')
    _plt.close(fig)
    if notifications == 'on':
        print(f"{filename} saved to {path}/{region.upper()}")
        
def plot_dew_point_depression(region='conus',
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=50,
                     start=0,
                     stop=50,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER DEW POINT DEPRESSION [°F]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=12,
                     secondary_title_fontsize=10,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=10,
                     colorbar_aspect=50,
                     colormap='terrain',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['aqua',
                             'mediumspringgreen',
                             'forestgreen',
                             'lime',
                             'chartreuse',
                             'olivedrab',
                             'olive',
                             'gold',
                             'darkorange',
                             'peru',
                             'saddlebrown'],
                     ds=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=4,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA/Dew Point Depression',
                     filename='RTMA Dew Point Depression.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     convert_temperature=True,
                     convert_from='kelvin',
                     convert_to='fahrenheit',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     var_key='2m_dew_point_depression',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude'):
    
    """
    This function plots the latest Real Time Mesoscale Analysis (RTMA) for dew point depression.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Entire CONUS region.
            ii) 'terrain' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Required Arguments: None
    
    Optional Arguments:
    
    1) region (String) - Default='conus'. The region of the plot. Use the 2-letter state abbreviation or 4-letter GACC abbreviation.
        If the user wants a completely custom region where they define their own lat/lon bounds, set region='custom'. 
        
    2) show_states (Boolean) - Default=True. When set to True, U.S. state borders are shown. 
    
    3) state_border_color (String) - Default='black'. The color of the U.S. state borders.
    
    4) state_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the U.S. state borders.
    
    5) state_border_zorder (Integer) - Default=3. The z-order of the state borders. For state borders to be displayed
        the following condition must be met: state_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
        
    6) show_counties (Boolean) - Default=True. When set to True, U.S. county borders are shown. 
    
    7) county_border_color (String) - Default='black'. The color of the U.S. county borders.
    
    8) county_border_linewidth (Float or Integer) - Default=0.25. The linewidth of the U.S. county borders.
    
    9) county_border_zorder (Integer) - Default=3. The z-order of the county borders. For county borders to be displayed
        the following condition must be met: county_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
    
    10) show_gacc_boundaries (Boolean) - Default=False. When set to True, Geographic Area Coordination Center borders are shown. 
    
    11) gacc_border_color (String) - Default='black'. The color of the Geographic Area Coordination Center borders.
    
    12) gacc_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the Geographic Area Coordination Center borders.
    
    13) gacc_border_zorder (Integer) - Default=3. The z-order of the Geographic Area Coordination Center borders. 
       For Geographic Area Coordination Center borders to be displayed the following condition must be met: gacc_border_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
       
    14) show_predictive_services_areas (Boolean) - Default=False. When set to True, Predictive Services Areas borders are shown. 
    
    15) predictive_services_areas_color (String) - Default='black'. The color of the Predictive Services Areas borders.
    
    16) predictive_services_areas_linewidth (Float or Integer) - Default=0.25. The linewidth of the Predictive Services Areas borders.
    
    17) predictive_services_areas_zorder (Integer) - Default=3. The z-order of the Predictive Services Areas borders. 
       For Predictive Services Areas borders to be displayed the following condition must be met: predictive_services_areas_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    18) show_nws_public_zones (Boolean) - Default=False. When set to True, NWS Public Zone borders are shown. 
    
    19) nws_public_zones_color (String) - Default='black'. The color of the NWS Public Zone borders.
    
    20) nws_public_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Public Zone borders.
    
    21) nws_public_zones_zorder (Integer) - Default=3. The z-order of the NWS Public Zone borders. 
       For NWS Public Zone borders to be displayed the following condition must be met: nws_public_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    22) show_nws_fire_weather_zones (Boolean) - Default=False. When set to True, NWS Fire Weather Zone borders are shown. 
    
    23) nws_fire_weather_zones_color (String) - Default='black'. The color of the NWS Fire Weather Zone borders.
    
    24) nws_fire_weather_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Fire Weather Zone borders.
    
    25) nws_fire_weather_zones_zorder (Integer) - Default=3. The z-order of the NWS Fire Weather Zone borders. 
       For NWS Fire Weather Zone borders to be displayed the following condition must be met: nws_fire_weather_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    26) show_nws_cwa (Boolean) - Default=False. When set to True, NWS CWA borders are shown.
    
    27) nws_cwa_color (String) - Default='black'. The color of the NWS CWA borders.
    
    28) nws_cwa_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS CWA borders.
    
    29) nws_cwa_zorder (Integer) - Default=3. The z-order of the NWS CWA borders. 
       For NWS CWA borders to be displayed the following condition must be met: nws_cwa_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    30) show_calfire_boundaries (Boolean) - Default=False. When set to True, CalFire borders are shown.
    
    31) calfire_boundary_color (String) - Default='black'. The color of the CalFire borders.
    
    32) calfire_boundary_linewidth (Float or Integer) - Default=0.25. The linewidth of the CalFire borders.
    
    33) calfire_boundary_zorder (Integer) - Default=3. The z-order of the CalFire borders. 
       For CalFire borders to be displayed the following condition must be met: calfire_boundary_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.

    34) custom_shapefile_url (String or None) - Default=None. If the user wishes to set up an automation importing geometry from a shapefile that
        is not in the base version of FireWxPy, this is how to do that. The user will pass the download URL as a string by setting
        custom_shapefile_url='https"//shapefile_download_url.file_extension'. 
        
    35) custom_shapefile_file_extension (String) - Default='.zip'. This is the file extension of the zipped shapefile folder on the web
        server. 
        
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    36) custom_shapefile_color (String) - Default='black'. The color of the borders in the custom shapefile.
    
    37) custom_shapefile_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders in the custom shapefile.
    
    38) custom_shapefile_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    39) custom_geojson_url (String) - Default=None. If the user wishes to set up an automation with a publicly available
        geojson on the web, pass in the full download URL into this argument.
    
    40) custom_geojson_filename (String) - Default=None. The filename of the custom geojson file. 
    
    41) custom_geojson_folder_name (String) Default='Custom GeoJSON'. The folder where the custom geojson will be saved in.
    
    42) custom_geojson_color (String) - Default='black'. The edge color of the geometries in the custom geojson file.
    
    43) custom_geojson_linewidth (Integer or Float) - Default=0.5. The linewidth of the borders in the custom geojson. 
    
    44) custom_geojson_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    45) custom_shapefile_local_path (String) - Default=None. The path to a shapefile locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    46) custom_shapefile_local_color (String) - Default='black'. The edge color of the geometries in the shapefile.
    
    47) custom_shapefile_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    48) custom_shapefile_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    49) custom_geojson_local_path (String) - Default=None. The path to a geojson locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    50) custom_geojson_local_color (String) - Default='black'. The edge color of the geometries in the geojson.
    
    51) custom_geojson_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    52) custom_geojson_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    53) convert_custom_shapefile_crs (Boolean)- Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom shapefile. 
        
    54) convert_local_custom_shapefile_crs (Boolean) - Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom geojson.
        
    55)  refresh_cartographic_files (Boolean) - Default=True. Users that have automated pipelines set up for shapefiles. Having this set to
        True allows the client to delete and re-download the shapefiles with each run of the script. This is useful for shapefiles
        that have frequent geometry updates.
        
    56) reference_system (String) - Default='States & Counties'. The name of the borders overlaid onto the map.
    
    57) show_rivers (Boolean) - Default=False. Set to True to display rivers. 
    
    58) rivers_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    59) rivers_color (String) - Default='lightcyan'. The color of the river. 
    
    60) figure_x_length (Integer) - Default=12. The length of the figure in the x-direction.
    
    61) figure_y_length (Integer) - Default=12. The length of the figure in the y-direction.
    
    62) coastline_linewidth (Float or Integer) - Default=0.75. The linewidth of the coastline.
    
    63) land_color (String) - Default='beige'. The color of the land on a map.
    
    64) ocean_color (String) - Default='lightcyan'. The color of the ocean on a map.
    
    65) lakes_color (String) - Default='lightcyan'. The color of lakes on a map. 

    66) costline_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    67) ocean_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    68) lakes_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    69) land_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    70) decimate (Integer) - Default=50. This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. When set to 50, every 50 values will be queried. Use
        larger numbers for larger areas and smaller values for smaller areas. The default of 50 represents the setting for
        CONUS. 
        
    71) start (Integer) - Default=0. The start of the filled contour range.
    
    72) stop (Integer) - Default=50. The end of the filled contour range. 
    
    73) step (Integer) - Default=1. The interval of the filled contours.
    
    74) facecolor (String) - Default='aliceblue'. The background color of the graphic. 
    
    75) primary_title_text (String) - Default='RTMA 2-METER DEW POINT DEPRESSION [°F]'. The primary title
        of the graphic. 
        
    76) primary_title_textbox_color (String) - Default='wheat'. The color of the textbox of the primary title.
    
    77) primary_title_textbox_style (String) - Default='round'. The style of the textbox of the primary title.
    
    78) primary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    79) secondary_title_textbox_color (Float or Integer) Default='wheat'. The color of the textbox of the secondary title.
        
    80) secondary_title_textbox_style (String) - Default='round'. The style of the textbox of the secondary title.
    
    81) secondary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    82) primary_title_fontsize (Integer) - Default=12. Fontsize of the primary title text.
    
    83) secondary_title_fontsize (Integer) Default=10. Fontsize of the secondary title text.
    
    84) local_time (Boolean) - Default=True. Set to False for UTC time.
    
    85) signature_textbox_color (String) - Default='wheat'. The color of the textbox of the graphic's signature.
    
    86) signature_textbox_style (String) - Default='round'. The style of the textbox of the graphic's signature.
    
    87) signature_textbox_alpha (Float or Integer) - Default=1. A value between 0.5 and 1 representing transparency.

    88) signature_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    89) signature_fontsize (Integer) - Default=8. Fontsize of the graphic's signature text.
    
    90) signature_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the signature text box.
    
    91) signature_textbox_y_position (Float) - Default=-0.175. The y-position with respect to the plot axis of the signature text box.
    
    92) signature_text_new_lines (Boolean) - Default=False. When set to True, each section in the signature is on a new line.
        It is recommended to set this to True on plots that are longer from North to South than West to East. 
        
    93) reference_system_textbox_color (String) - Default='wheat'. The color of the textbox of the reference system.
    
    94) reference_system_textbox_style (String) - Default='round'. The style of the textbox of the reference system.
    
    95) reference_system_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    96) reference_system_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    97) reference_system_fontsize (Integer) - Default=6. Fontsize of the reference system label text.
    
    98) reference_system_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the reference system text box.
    
    99) reference_system_textbox_y_position (Float) - Default=0. The y-position with respect to the plot axis of the reference system text box.

    100) colorbar_shrink (Float or Integer) - Default=1. Fraction by which to multiply the size of the colorbar.
    
    101) colorbar_pad (Float) - Default=0.01. Fraction of original Axes between colorbar and new image Axes.
    
    102) tick_label_fontsize (Integer) - Default=9. The fontsize of the colorbar tick labels.
    
    103) colorbar_location (String) - Default='bottom'. The side of the plot axis where the colorbar will be displayed.
    
    104) colorbar_interval (Integer) - Default=10. The interval of tick marks on the colorbar.
    
    105) colorbar_aspect (Integer) - Default=50. Ratio of long to short dimensions.
    
    106) colormap (String) - Default='terrain'. The Matplotlib colormap for filled contours being used OR set to 'custom' to create your own 
        custom colormapping. See the optional colors argument documentation (109) for more information on how to pass
        in a custom array of colors. 
        
    107) contourf_alpha (Float or Integer) - Default=0.5. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    108) contourf_zorder (Integer) - Default=2. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    109) colors (String List) - Default=['aqua',
                                        'mediumspringgreen',
                                        'forestgreen',
                                        'lime',
                                        'chartreuse',
                                        'olivedrab',
                                        'olive',
                                        'gold',
                                        'darkorange',
                                        'peru',
                                        'saddlebrown']
                                        
            The array of colors being used when colormap='custom'. 
            
    110) ds (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds=ds. 
            
    111) western_bound (Float or Integer) - Default=-125. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    112) eastern_bound (Float or Integer) - Default=-65. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    113) southern_bound (Float or Integer) - Default=20. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    114) northern_bound (Float or Integer) - Default=50. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    115) pixel_query_value_fontsize (Integer) - Default=4. The fontsize of the pixel query values.
    
    116) pixel_query_value_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    117) pixel_query_value_foreground (String) - Default='white'. The color of the foreground on the station plot (pixel query value).
    
    118) pixel_query_value_fontcolor (String) - Default='black'. The font color of the pixel query values.
    
    119) pixel_query_stroke_linewidth (Float or Integer) - Default=1. The linewidth of the pixel query values text outline.
    
    120) path (String) - Default='FireWxPy Graphics/RTMA/Dew Point Depression'. The directory where the graphic will save.
    
    121) filename (String) - Default='RTMA Dew Point Depression.png'. The filename of the image.
    
    122) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    123) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
        
    124) clear_data (Boolean) - Default=True. When set to True, the data will be cleared with each run of the script.
        Set to False when downloading the data outside of the function and passing the data in. 
        
    125) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB data to a file.
    
    126) notifications (String) - Default='off'. Notifications throughout the process. 

    127) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    128) convert_from (String) - Default='kelvin'. Units we are converting from. (Only needed if not using WxData to download and process the data).
    
    129) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 

    130) custom_data_directory (String or None) - Default=None. The directory path where the data will be saved to. 

    131) mapcrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the map.
    
    132) datacrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the data.

    133) var_key (String) - Default='2m_dew_point_depression'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    134) time_coord_key (String) - Default='time'. The time coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    135) longitude_key (String) - Default='longitude'. The longitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
    
    136) latitude_key (String) - Default='latitude'. The latitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.

    Returns
    -------
    
    An image of the RTMA Dew Point Depression Analysis specified to the user's needs saved to {path}    
    """    
    
    _build_directory_branch(f"{path}/{region.upper()}/{reference_system.upper()}")
    
    _mpl.rcParams['xtick.labelsize'] = tick_label_fontsize
    _mpl.rcParams['ytick.labelsize'] = tick_label_fontsize
    
    primary_title_box = dict(boxstyle=primary_title_textbox_style, 
                            facecolor=primary_title_textbox_color, 
                            alpha=primary_title_textbox_alpha)
    
    secondary_title_box = dict(boxstyle=secondary_title_textbox_style, 
                            facecolor=secondary_title_textbox_color, 
                            alpha=secondary_title_textbox_alpha)
    
    signature_box = dict(boxstyle=signature_textbox_style, 
                            facecolor=signature_textbox_color, 
                            alpha=signature_textbox_alpha)
    
    reference_system_box = dict(boxstyle=reference_system_textbox_style, 
                            facecolor=reference_system_textbox_color, 
                            alpha=reference_system_textbox_alpha)
    
    levels = _np.arange(start, (stop + step), step)
    ticks = levels[::colorbar_interval]
    
    western_bound, eastern_bound, southern_bound, northern_bound = _bounding_box(region,
                                                                                 western_bound,
                                                                                 eastern_bound,
                                                                                 southern_bound,
                                                                                 northern_bound)
    
    if ds is None:
        ds = _rtma(proxies=proxies,
                   clear_recycle_bin=clear_recycle_bin,
                   clear_data=clear_data,
                   western_bound=western_bound,
                   eastern_bound=eastern_bound,
                   southern_bound=southern_bound,
                   northern_bound=northern_bound,
                   convert_temperature=convert_temperature,
                   convert_to=convert_to,
                   chunk_size=chunk_size,
                   notifications=notifications,
                   custom_directory=custom_data_directory)
    else:
        ds = ds
        if convert_temperature is True:
            if convert_from == 'kelvin':
                if convert_to == 'fahrenheit':
                    ds[var_key] = _kelvin_to_fahrenheit(ds[var_key])
                else:
                    ds[var_key] = _kelvin_to_celsius(ds[var_key])
            else:
                if convert_to == 'fahrenheit':
                    ds[var_key] = _celsius_to_fahrenheit(ds[var_key])
        
    if colormap == 'custom':
        cmap = _mcolors.LinearSegmentedColormap.from_list("dew point depression", colors)
    else:
        cmap = colormap
    
    valid_time = _pd.to_datetime(ds[time_coord_key].to_pandas())
    valid_time = valid_time.tz_localize('UTC')
    time = valid_time.astimezone(_to_zone)
    time_utc = time.astimezone(_from_zone)
    
    fig = _plt.figure(figsize=(figure_x_length, figure_y_length))
    fig.set_facecolor(facecolor)
    
    ax = fig.add_subplot(1,1,1, projection=mapcrs)
    ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax.add_feature(_cfeature.COASTLINE.with_scale('50m'), linewidth=coastline_linewidth, zorder=costline_zorder)
    ax.add_feature(_cfeature.LAND, color=land_color, zorder=land_zorder)
    ax.add_feature(_cfeature.OCEAN, color=ocean_color, zorder=ocean_zorder)
    ax.add_feature(_cfeature.LAKES, color=lakes_color, zorder=lakes_zorder)
    if show_rivers is True:
        ax.add_feature(_cfeature.RIVERS, color=rivers_color, zorder=rivers_zorder)
    if show_states is True:
        states = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_States_Territories.zip",
                                            f"Cartographic Files/US States",
                                            f"US_States_Territories.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            state_border_color,
                                            datacrs)
        
        ax.add_geometries(states, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=state_border_color, 
                          linewidth=state_border_linewidth, 
                          zorder=state_border_zorder)
    
    if show_counties is True:
        counties = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_Counties.zip",
                                            f"Cartographic Files/US Counties",
                                            f"US_Counties.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            county_border_color,
                                            datacrs)
        
        ax.add_geometries(counties, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=county_border_color, 
                          linewidth=county_border_linewidth, 
                          zorder=county_border_zorder)
        
    if show_gacc_boundaries is True:
        gacc = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/GACC_Boundaries_2026.zip",
                                            f"Cartographic Files/GACC Boundaries",
                                            f"GACC_Boundaries_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            gacc_border_color,
                                            datacrs)
        
        ax.add_geometries(gacc, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=gacc_border_color, 
                          linewidth=gacc_border_linewidth, 
                          zorder=gacc_border_zorder)
    
    if show_predictive_services_areas is True:
        psa = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/PSA_Boundaries.zip",
                                            f"Cartographic Files/PSA Boundaries",
                                            f"PSA_Boundaries.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            predictive_services_areas_color,
                                            datacrs)
        
        ax.add_geometries(psa, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=predictive_services_areas_color, 
                          linewidth=predictive_services_areas_linewidth, 
                          zorder=predictive_services_areas_zorder)
        
    if show_nws_public_zones is True:
        pz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Public_Zones_2026.zip",
                                            f"Cartographic Files/NWS Public Zones",
                                            f"NWS_Public_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_public_zones_color,
                                            datacrs)
        
        ax.add_geometries(pz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_public_zones_color, 
                          linewidth=nws_public_zones_linewidth, 
                          zorder=nws_public_zones_zorder)
        
    if show_nws_fire_weather_zones is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Fire_Weather_Zones_2026.zip",
                                            f"Cartographic Files/NWS Fire Weather Zones",
                                            f"NWS_Fire_Weather_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_fire_weather_zones_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_fire_weather_zones_color, 
                          linewidth=nws_fire_weather_zones_linewidth, 
                          zorder=nws_fire_weather_zones_zorder)
        
    if show_nws_cwa is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_CWA_2026.zip",
                                            f"Cartographic Files/NWS CWAs",
                                            f"NWS_CWA_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_cwa_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_cwa_color, 
                          linewidth=nws_cwa_linewidth, 
                          zorder=nws_cwa_zorder)
        
    if show_calfire_boundaries is True:
        calfire = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/CALFIRE/CalFire_Administrative_Units.zip",
                                            f"Cartographic Files/CalFire",
                                            f"CalFire_Administrative_Units.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            calfire_boundary_color,
                                            datacrs,
                                            convert_crs=True,
                                            convert_to='EPSG:4326')
        
        ax.add_geometries(calfire, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=calfire_boundary_color, 
                          linewidth=calfire_boundary_linewidth, 
                          zorder=calfire_boundary_zorder)
        
    if custom_shapefile_url is not None:
        
        fname = _get_filename_from_url(custom_shapefile_url)
        
        custom_shape = _import_shapefile_from_web(custom_shapefile_url,
                                            f"Cartographic Files/{custom_shapefile_folder_name}",
                                            fname,
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            custom_shapefile_file_extension,
                                            custom_shapefile_color,
                                            convert_crs=convert_custom_shapefile_crs)
        
        ax.add_geometries(custom_shape, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_color, 
                          linewidth=custom_shapefile_linewidth, 
                          zorder=custom_shapefile_zorder)
        
    if custom_geojson_url is not None:
        
        custom_json = _import_geojson_from_web(custom_geojson_url,
                                                f"Cartographic Files/{custom_geojson_folder_name}", 
                                                custom_geojson_filename, 
                                                proxies, 
                                                chunk_size,
                                                notifications, 
                                                refresh_cartographic_files)
        
        ax.add_geometries(custom_json, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_color, 
                          linewidth=custom_geojson_linewidth, 
                          zorder=custom_geojson_zorder)
        
    if custom_shapefile_local_path is not None:
        custom_local_shapefile = _import_shapefile_local(custom_shapefile_local_path,
                                                            custom_shapefile_local_color,
                                                            convert_crs=convert_local_custom_shapefile_crs)
        
        ax.add_geometries(custom_local_shapefile, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_local_color, 
                          linewidth=custom_shapefile_local_linewidth, 
                          zorder=custom_shapefile_local_zorder)
        
    if custom_geojson_local_path is not None:
        custom_local_geojson = _import_geojson_local(custom_geojson_local_path)
        
        ax.add_geometries(custom_local_geojson, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_local_color, 
                          linewidth=custom_geojson_local_linewidth, 
                          zorder=custom_geojson_local_zorder)
    
    cs = ax.contourf(ds[longitude_key],
                ds[latitude_key],
                ds[var_key],
                cmap=cmap,
                levels=levels,
                transform=datacrs,
                alpha=contourf_alpha,
                zorder=contourf_zorder,
                extend='both')
    
    fig.colorbar(cs, 
                shrink=colorbar_shrink, 
                pad=colorbar_pad, 
                location=colorbar_location,
                ticks=ticks,
                aspect=colorbar_aspect)
    
    _plt.title(f"{primary_title_text}", 
               fontsize=primary_title_fontsize, 
               fontweight='bold',
               bbox=primary_title_box,
               loc='left')
    
    if local_time is True:
        _plt.title(f"Valid: {time.strftime('%m/%d/%Y %H:00')} {_timezone}", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
    else:
        _plt.title(f"Valid: {time_utc.strftime('%m/%d/%Y %H:00')} UTC", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
        
    if signature_text_new_lines is False:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')} | Data Source: NCEP/NOMADS | Created: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    else:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')}\nData Source: NCEP/NOMADS\nCreated: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    
    ax.text(reference_system_textbox_x_position, 
            reference_system_textbox_y_position,
            f"Reference System: {reference_system}",
            fontsize=reference_system_fontsize,
            fontweight='bold',
            bbox=reference_system_box,
            transform=ax.transAxes,
            zorder=reference_system_textbox_zorder)
        
    vals = _fix_var_array(ds,
                    var_key,
                    0,
                    decimate)

    stn = _mpplots.StationPlot(ax, vals['longitude'], vals['latitude'],
                                transform=datacrs, 
                                fontsize=pixel_query_value_fontsize, 
                                zorder=pixel_query_value_zorder, 
                                clip_on=True)


    stn.plot_parameter('C', 
                       vals[var_key], 
                       color=pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)
    
    fig.savefig(f"{path}/{region.upper()}/{reference_system.upper()}/{filename}", bbox_inches='tight')
    _plt.close(fig)
    if notifications == 'on':
        print(f"{filename} saved to {path}/{region.upper()}")
        
def plot_relative_humidity(region='conus',
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=50,
                     start=0,
                     stop=100,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER RELATIVE HUMIDITY [%]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=12,
                     secondary_title_fontsize=10,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=10,
                     colorbar_aspect=50,
                     colormap='terrain_r',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['saddlebrown',
                             'peru',
                             'darkorange',
                             'gold',
                             'olive',
                             'olivedrab',
                             'chartreuse',
                             'lime',
                             'forestgreen',
                             'mediumspringgreen',
                             'aqua'],
                     ds=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=4,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA/Relative Humidity',
                     filename='RTMA Relative Humidity.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     convert_temperature=True,
                     convert_to='fahrenheit',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     var_key='2m_relative_humidity',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude'):
    
    """
    This function plots the latest Real Time Mesoscale Analysis (RTMA) for relative humidity.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Entire CONUS region.
            ii) 'terrain_r' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Required Arguments: None
    
    Optional Arguments:
    
    1) region (String) - Default='conus'. The region of the plot. Use the 2-letter state abbreviation or 4-letter GACC abbreviation.
        If the user wants a completely custom region where they define their own lat/lon bounds, set region='custom'. 
        
    2) show_states (Boolean) - Default=True. When set to True, U.S. state borders are shown. 
    
    3) state_border_color (String) - Default='black'. The color of the U.S. state borders.
    
    4) state_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the U.S. state borders.
    
    5) state_border_zorder (Integer) - Default=3. The z-order of the state borders. For state borders to be displayed
        the following condition must be met: state_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
        
    6) show_counties (Boolean) - Default=True. When set to True, U.S. county borders are shown. 
    
    7) county_border_color (String) - Default='black'. The color of the U.S. county borders.
    
    8) county_border_linewidth (Float or Integer) - Default=0.25. The linewidth of the U.S. county borders.
    
    9) county_border_zorder (Integer) - Default=3. The z-order of the county borders. For county borders to be displayed
        the following condition must be met: county_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
    
    10) show_gacc_boundaries (Boolean) - Default=False. When set to True, Geographic Area Coordination Center borders are shown. 
    
    11) gacc_border_color (String) - Default='black'. The color of the Geographic Area Coordination Center borders.
    
    12) gacc_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the Geographic Area Coordination Center borders.
    
    13) gacc_border_zorder (Integer) - Default=3. The z-order of the Geographic Area Coordination Center borders. 
       For Geographic Area Coordination Center borders to be displayed the following condition must be met: gacc_border_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
       
    14) show_predictive_services_areas (Boolean) - Default=False. When set to True, Predictive Services Areas borders are shown. 
    
    15) predictive_services_areas_color (String) - Default='black'. The color of the Predictive Services Areas borders.
    
    16) predictive_services_areas_linewidth (Float or Integer) - Default=0.25. The linewidth of the Predictive Services Areas borders.
    
    17) predictive_services_areas_zorder (Integer) - Default=3. The z-order of the Predictive Services Areas borders. 
       For Predictive Services Areas borders to be displayed the following condition must be met: predictive_services_areas_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    18) show_nws_public_zones (Boolean) - Default=False. When set to True, NWS Public Zone borders are shown. 
    
    19) nws_public_zones_color (String) - Default='black'. The color of the NWS Public Zone borders.
    
    20) nws_public_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Public Zone borders.
    
    21) nws_public_zones_zorder (Integer) - Default=3. The z-order of the NWS Public Zone borders. 
       For NWS Public Zone borders to be displayed the following condition must be met: nws_public_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    22) show_nws_fire_weather_zones (Boolean) - Default=False. When set to True, NWS Fire Weather Zone borders are shown. 
    
    23) nws_fire_weather_zones_color (String) - Default='black'. The color of the NWS Fire Weather Zone borders.
    
    24) nws_fire_weather_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Fire Weather Zone borders.
    
    25) nws_fire_weather_zones_zorder (Integer) - Default=3. The z-order of the NWS Fire Weather Zone borders. 
       For NWS Fire Weather Zone borders to be displayed the following condition must be met: nws_fire_weather_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    26) show_nws_cwa (Boolean) - Default=False. When set to True, NWS CWA borders are shown.
    
    27) nws_cwa_color (String) - Default='black'. The color of the NWS CWA borders.
    
    28) nws_cwa_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS CWA borders.
    
    29) nws_cwa_zorder (Integer) - Default=3. The z-order of the NWS CWA borders. 
       For NWS CWA borders to be displayed the following condition must be met: nws_cwa_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    30) show_calfire_boundaries (Boolean) - Default=False. When set to True, CalFire borders are shown.
    
    31) calfire_boundary_color (String) - Default='black'. The color of the CalFire borders.
    
    32) calfire_boundary_linewidth (Float or Integer) - Default=0.25. The linewidth of the CalFire borders.
    
    33) calfire_boundary_zorder (Integer) - Default=3. The z-order of the CalFire borders. 
       For CalFire borders to be displayed the following condition must be met: calfire_boundary_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.

    34) custom_shapefile_url (String or None) - Default=None. If the user wishes to set up an automation importing geometry from a shapefile that
        is not in the base version of FireWxPy, this is how to do that. The user will pass the download URL as a string by setting
        custom_shapefile_url='https"//shapefile_download_url.file_extension'. 
        
    35) custom_shapefile_file_extension (String) - Default='.zip'. This is the file extension of the zipped shapefile folder on the web
        server. 
        
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    36) custom_shapefile_color (String) - Default='black'. The color of the borders in the custom shapefile.
    
    37) custom_shapefile_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders in the custom shapefile.
    
    38) custom_shapefile_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    39) custom_geojson_url (String) - Default=None. If the user wishes to set up an automation with a publicly available
        geojson on the web, pass in the full download URL into this argument.
    
    40) custom_geojson_filename (String) - Default=None. The filename of the custom geojson file. 
    
    41) custom_geojson_folder_name (String) Default='Custom GeoJSON'. The folder where the custom geojson will be saved in.
    
    42) custom_geojson_color (String) - Default='black'. The edge color of the geometries in the custom geojson file.
    
    43) custom_geojson_linewidth (Integer or Float) - Default=0.5. The linewidth of the borders in the custom geojson. 
    
    44) custom_geojson_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    45) custom_shapefile_local_path (String) - Default=None. The path to a shapefile locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    46) custom_shapefile_local_color (String) - Default='black'. The edge color of the geometries in the shapefile.
    
    47) custom_shapefile_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    48) custom_shapefile_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    49) custom_geojson_local_path (String) - Default=None. The path to a geojson locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    50) custom_geojson_local_color (String) - Default='black'. The edge color of the geometries in the geojson.
    
    51) custom_geojson_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    52) custom_geojson_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    53) convert_custom_shapefile_crs (Boolean)- Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom shapefile. 
        
    54) convert_local_custom_shapefile_crs (Boolean) - Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom geojson.
        
    55)  refresh_cartographic_files (Boolean) - Default=True. Users that have automated pipelines set up for shapefiles. Having this set to
        True allows the client to delete and re-download the shapefiles with each run of the script. This is useful for shapefiles
        that have frequent geometry updates.
        
    56) reference_system (String) - Default='States & Counties'. The name of the borders overlaid onto the map.
    
    57) show_rivers (Boolean) - Default=False. Set to True to display rivers. 
    
    58) rivers_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    59) rivers_color (String) - Default='lightcyan'. The color of the river. 
    
    60) figure_x_length (Integer) - Default=12. The length of the figure in the x-direction.
    
    61) figure_y_length (Integer) - Default=12. The length of the figure in the y-direction.
    
    62) coastline_linewidth (Float or Integer) - Default=0.75. The linewidth of the coastline.
    
    63) land_color (String) - Default='beige'. The color of the land on a map.
    
    64) ocean_color (String) - Default='lightcyan'. The color of the ocean on a map.
    
    65) lakes_color (String) - Default='lightcyan'. The color of lakes on a map. 

    66) costline_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    67) ocean_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    68) lakes_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    69) land_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    70) decimate (Integer) - Default=50. This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. When set to 50, every 50 values will be queried. Use
        larger numbers for larger areas and smaller values for smaller areas. The default of 50 represents the setting for
        CONUS. 
        
    71) start (Integer) - Default=0. The start of the filled contour range.
    
    72) stop (Integer) - Default=100. The end of the filled contour range. 
    
    73) step (Integer) - Default=1. The interval of the filled contours.
    
    74) facecolor (String) - Default='aliceblue'. The background color of the graphic. 
    
    75) primary_title_text (String) - Default='RTMA 2-METER RELATIVE HUMIDITY [%]'. The primary title
        of the graphic. 
        
    76) primary_title_textbox_color (String) - Default='wheat'. The color of the textbox of the primary title.
    
    77) primary_title_textbox_style (String) - Default='round'. The style of the textbox of the primary title.
    
    78) primary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    79) secondary_title_textbox_color (Float or Integer) Default='wheat'. The color of the textbox of the secondary title.
        
    80) secondary_title_textbox_style (String) - Default='round'. The style of the textbox of the secondary title.
    
    81) secondary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    82) primary_title_fontsize (Integer) - Default=12. Fontsize of the primary title text.
    
    83) secondary_title_fontsize (Integer) Default=10. Fontsize of the secondary title text.
    
    84) local_time (Boolean) - Default=True. Set to False for UTC time.
    
    85) signature_textbox_color (String) - Default='wheat'. The color of the textbox of the graphic's signature.
    
    86) signature_textbox_style (String) - Default='round'. The style of the textbox of the graphic's signature.
    
    87) signature_textbox_alpha (Float or Integer) - Default=1. A value between 0.5 and 1 representing transparency.

    88) signature_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    89) signature_fontsize (Integer) - Default=8. Fontsize of the graphic's signature text.
    
    90) signature_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the signature text box.
    
    91) signature_textbox_y_position (Float) - Default=-0.175. The y-position with respect to the plot axis of the signature text box.
    
    92) signature_text_new_lines (Boolean) - Default=False. When set to True, each section in the signature is on a new line.
        It is recommended to set this to True on plots that are longer from North to South than West to East. 
        
    93) reference_system_textbox_color (String) - Default='wheat'. The color of the textbox of the reference system.
    
    94) reference_system_textbox_style (String) - Default='round'. The style of the textbox of the reference system.
    
    95) reference_system_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    96) reference_system_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    97) reference_system_fontsize (Integer) - Default=6. Fontsize of the reference system label text.
    
    98) reference_system_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the reference system text box.
    
    99) reference_system_textbox_y_position (Float) - Default=0. The y-position with respect to the plot axis of the reference system text box.

    100) colorbar_shrink (Float or Integer) - Default=1. Fraction by which to multiply the size of the colorbar.
    
    101) colorbar_pad (Float) - Default=0.01. Fraction of original Axes between colorbar and new image Axes.
    
    102) tick_label_fontsize (Integer) - Default=9. The fontsize of the colorbar tick labels.
    
    103) colorbar_location (String) - Default='bottom'. The side of the plot axis where the colorbar will be displayed.
    
    104) colorbar_interval (Integer) - Default=10. The interval of tick marks on the colorbar.
    
    105) colorbar_aspect (Integer) - Default=50. Ratio of long to short dimensions.
    
    106) colormap (String) - Default='terrain_r'. The Matplotlib colormap for filled contours being used OR set to 'custom' to create your own 
        custom colormapping. See the optional colors argument documentation (109) for more information on how to pass
        in a custom array of colors. 
        
    107) contourf_alpha (Float or Integer) - Default=0.5. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    108) contourf_zorder (Integer) - Default=2. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    109) colors (String List) - Default=['saddlebrown',
                                        'peru',
                                        'darkorange',
                                        'gold',
                                        'olive',
                                        'olivedrab',
                                        'chartreuse',
                                        'lime',
                                        'forestgreen',
                                        'mediumspringgreen',
                                        'aqua']
                                        
            The array of colors being used when colormap='custom'. 
            
    110) ds (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds=ds. 
            
    111) western_bound (Float or Integer) - Default=-125. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    112) eastern_bound (Float or Integer) - Default=-65. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    113) southern_bound (Float or Integer) - Default=20. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    114) northern_bound (Float or Integer) - Default=50. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    115) pixel_query_value_fontsize (Integer) - Default=4. The fontsize of the pixel query values.
    
    116) pixel_query_value_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    117) pixel_query_value_foreground (String) - Default='white'. The color of the foreground on the station plot (pixel query value).
    
    118) pixel_query_value_fontcolor (String) - Default='black'. The font color of the pixel query values.
    
    119) pixel_query_stroke_linewidth (Float or Integer) - Default=1. The linewidth of the pixel query values text outline.
    
    120) path (String) - Default='FireWxPy Graphics/RTMA/Relative Humidity'. The directory where the graphic will save.
    
    121) filename (String) - Default='RTMA Relative Humidity.png'. The filename of the image.
    
    122) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    123) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
        
    124) clear_data (Boolean) - Default=True. When set to True, the data will be cleared with each run of the script.
        Set to False when downloading the data outside of the function and passing the data in. 
        
    125) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB data to a file.
    
    126) notifications (String) - Default='off'. Notifications throughout the process. 

    127) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
            
    128) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 

    129) custom_data_directory (String or None) - Default=None. The directory path where the data will be saved to. 

    130) mapcrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the map.
    
    131) datacrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the data.

    132) var_key (String) - Default='2m_relative_humidity'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    133) time_coord_key (String) - Default='time'. The time coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    134) longitude_key (String) - Default='longitude'. The longitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
    
    135) latitude_key (String) - Default='latitude'. The latitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.

    Returns
    -------
    
    An image of the RTMA Relative Humidity Analysis specified to the user's needs saved to {path}    
    """    
    
    _build_directory_branch(f"{path}/{region.upper()}/{reference_system.upper()}")
    
    _mpl.rcParams['xtick.labelsize'] = tick_label_fontsize
    _mpl.rcParams['ytick.labelsize'] = tick_label_fontsize
    
    primary_title_box = dict(boxstyle=primary_title_textbox_style, 
                            facecolor=primary_title_textbox_color, 
                            alpha=primary_title_textbox_alpha)
    
    secondary_title_box = dict(boxstyle=secondary_title_textbox_style, 
                            facecolor=secondary_title_textbox_color, 
                            alpha=secondary_title_textbox_alpha)
    
    signature_box = dict(boxstyle=signature_textbox_style, 
                            facecolor=signature_textbox_color, 
                            alpha=signature_textbox_alpha)
    
    reference_system_box = dict(boxstyle=reference_system_textbox_style, 
                            facecolor=reference_system_textbox_color, 
                            alpha=reference_system_textbox_alpha)
    
    levels = _np.arange(start, (stop + step), step)
    ticks = levels[::colorbar_interval]
    
    western_bound, eastern_bound, southern_bound, northern_bound = _bounding_box(region,
                                                                                 western_bound,
                                                                                 eastern_bound,
                                                                                 southern_bound,
                                                                                 northern_bound)
    
    if ds is None:
        ds = _rtma(proxies=proxies,
                   clear_recycle_bin=clear_recycle_bin,
                   clear_data=clear_data,
                   western_bound=western_bound,
                   eastern_bound=eastern_bound,
                   southern_bound=southern_bound,
                   northern_bound=northern_bound,
                   convert_temperature=convert_temperature,
                   convert_to=convert_to,
                   chunk_size=chunk_size,
                   notifications=notifications,
                   custom_directory=custom_data_directory)
    else:
        ds = ds
        
    if colormap == 'custom':
        cmap = _mcolors.LinearSegmentedColormap.from_list("relative humidity", colors)
    else:
        cmap = colormap
    
    valid_time = _pd.to_datetime(ds[time_coord_key].to_pandas())
    valid_time = valid_time.tz_localize('UTC')
    time = valid_time.astimezone(_to_zone)
    time_utc = time.astimezone(_from_zone)
    
    fig = _plt.figure(figsize=(figure_x_length, figure_y_length))
    fig.set_facecolor(facecolor)
    
    ax = fig.add_subplot(1,1,1, projection=mapcrs)
    ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax.add_feature(_cfeature.COASTLINE.with_scale('50m'), linewidth=coastline_linewidth, zorder=costline_zorder)
    ax.add_feature(_cfeature.LAND, color=land_color, zorder=land_zorder)
    ax.add_feature(_cfeature.OCEAN, color=ocean_color, zorder=ocean_zorder)
    ax.add_feature(_cfeature.LAKES, color=lakes_color, zorder=lakes_zorder)
    if show_rivers is True:
        ax.add_feature(_cfeature.RIVERS, color=rivers_color, zorder=rivers_zorder)
    if show_states is True:
        states = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_States_Territories.zip",
                                            f"Cartographic Files/US States",
                                            f"US_States_Territories.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            state_border_color,
                                            datacrs)
        
        ax.add_geometries(states, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=state_border_color, 
                          linewidth=state_border_linewidth, 
                          zorder=state_border_zorder)
    
    if show_counties is True:
        counties = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_Counties.zip",
                                            f"Cartographic Files/US Counties",
                                            f"US_Counties.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            county_border_color,
                                            datacrs)
        
        ax.add_geometries(counties, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=county_border_color, 
                          linewidth=county_border_linewidth, 
                          zorder=county_border_zorder)
        
    if show_gacc_boundaries is True:
        gacc = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/GACC_Boundaries_2026.zip",
                                            f"Cartographic Files/GACC Boundaries",
                                            f"GACC_Boundaries_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            gacc_border_color,
                                            datacrs)
        
        ax.add_geometries(gacc, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=gacc_border_color, 
                          linewidth=gacc_border_linewidth, 
                          zorder=gacc_border_zorder)
    
    if show_predictive_services_areas is True:
        psa = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/PSA_Boundaries.zip",
                                            f"Cartographic Files/PSA Boundaries",
                                            f"PSA_Boundaries.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            predictive_services_areas_color,
                                            datacrs)
        
        ax.add_geometries(psa, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=predictive_services_areas_color, 
                          linewidth=predictive_services_areas_linewidth, 
                          zorder=predictive_services_areas_zorder)
        
    if show_nws_public_zones is True:
        pz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Public_Zones_2026.zip",
                                            f"Cartographic Files/NWS Public Zones",
                                            f"NWS_Public_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_public_zones_color,
                                            datacrs)
        
        ax.add_geometries(pz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_public_zones_color, 
                          linewidth=nws_public_zones_linewidth, 
                          zorder=nws_public_zones_zorder)
        
    if show_nws_fire_weather_zones is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Fire_Weather_Zones_2026.zip",
                                            f"Cartographic Files/NWS Fire Weather Zones",
                                            f"NWS_Fire_Weather_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_fire_weather_zones_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_fire_weather_zones_color, 
                          linewidth=nws_fire_weather_zones_linewidth, 
                          zorder=nws_fire_weather_zones_zorder)
        
    if show_nws_cwa is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_CWA_2026.zip",
                                            f"Cartographic Files/NWS CWAs",
                                            f"NWS_CWA_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_cwa_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_cwa_color, 
                          linewidth=nws_cwa_linewidth, 
                          zorder=nws_cwa_zorder)
        
    if show_calfire_boundaries is True:
        calfire = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/CALFIRE/CalFire_Administrative_Units.zip",
                                            f"Cartographic Files/CalFire",
                                            f"CalFire_Administrative_Units.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            calfire_boundary_color,
                                            datacrs,
                                            convert_crs=True,
                                            convert_to='EPSG:4326')
        
        ax.add_geometries(calfire, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=calfire_boundary_color, 
                          linewidth=calfire_boundary_linewidth, 
                          zorder=calfire_boundary_zorder)
        
    if custom_shapefile_url is not None:
        
        fname = _get_filename_from_url(custom_shapefile_url)
        
        custom_shape = _import_shapefile_from_web(custom_shapefile_url,
                                            f"Cartographic Files/{custom_shapefile_folder_name}",
                                            fname,
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            custom_shapefile_file_extension,
                                            custom_shapefile_color,
                                            convert_crs=convert_custom_shapefile_crs)
        
        ax.add_geometries(custom_shape, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_color, 
                          linewidth=custom_shapefile_linewidth, 
                          zorder=custom_shapefile_zorder)
        
    if custom_geojson_url is not None:
        
        custom_json = _import_geojson_from_web(custom_geojson_url,
                                                f"Cartographic Files/{custom_geojson_folder_name}", 
                                                custom_geojson_filename, 
                                                proxies, 
                                                chunk_size,
                                                notifications, 
                                                refresh_cartographic_files)
        
        ax.add_geometries(custom_json, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_color, 
                          linewidth=custom_geojson_linewidth, 
                          zorder=custom_geojson_zorder)
        
    if custom_shapefile_local_path is not None:
        custom_local_shapefile = _import_shapefile_local(custom_shapefile_local_path,
                                                            custom_shapefile_local_color,
                                                            convert_crs=convert_local_custom_shapefile_crs)
        
        ax.add_geometries(custom_local_shapefile, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_local_color, 
                          linewidth=custom_shapefile_local_linewidth, 
                          zorder=custom_shapefile_local_zorder)
        
    if custom_geojson_local_path is not None:
        custom_local_geojson = _import_geojson_local(custom_geojson_local_path)
        
        ax.add_geometries(custom_local_geojson, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_local_color, 
                          linewidth=custom_geojson_local_linewidth, 
                          zorder=custom_geojson_local_zorder)
    
    cs = ax.contourf(ds[longitude_key],
                ds[latitude_key],
                ds[var_key],
                cmap=cmap,
                levels=levels,
                transform=datacrs,
                alpha=contourf_alpha,
                zorder=contourf_zorder,
                extend='both')
    
    fig.colorbar(cs, 
                shrink=colorbar_shrink, 
                pad=colorbar_pad, 
                location=colorbar_location,
                ticks=ticks,
                aspect=colorbar_aspect)
    
    _plt.title(f"{primary_title_text}", 
               fontsize=primary_title_fontsize, 
               fontweight='bold',
               bbox=primary_title_box,
               loc='left')
    
    if local_time is True:
        _plt.title(f"Valid: {time.strftime('%m/%d/%Y %H:00')} {_timezone}", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
    else:
        _plt.title(f"Valid: {time_utc.strftime('%m/%d/%Y %H:00')} UTC", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
        
    if signature_text_new_lines is False:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')} | Data Source: NCEP/NOMADS | Created: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    else:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')}\nData Source: NCEP/NOMADS\nCreated: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    
    ax.text(reference_system_textbox_x_position, 
            reference_system_textbox_y_position,
            f"Reference System: {reference_system}",
            fontsize=reference_system_fontsize,
            fontweight='bold',
            bbox=reference_system_box,
            transform=ax.transAxes,
            zorder=reference_system_textbox_zorder)
        
        
    vals = _fix_var_array(ds,
                    var_key,
                    0,
                    decimate)

    stn = _mpplots.StationPlot(ax, vals['longitude'], vals['latitude'],
                                transform=datacrs, 
                                fontsize=pixel_query_value_fontsize, 
                                zorder=pixel_query_value_zorder, 
                                clip_on=True)


    stn.plot_parameter('C', 
                       vals[var_key], 
                       color=pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)


    fig.savefig(f"{path}/{region.upper()}/{reference_system.upper()}/{filename}", bbox_inches='tight')
    _plt.close(fig)
    if notifications == 'on':
        print(f"{filename} saved to {path}/{region.upper()}")
        
def plot_wind_speed(region='conus',
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=50,
                     start=0,
                     stop=70,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 10-METER WIND SPEED [MPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=12,
                     secondary_title_fontsize=10,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=10,
                     colorbar_aspect=50,
                     colormap='jet',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['lightblue',
                             'dodgerblue',
                             'lime',
                             'gold',
                             'darkorange',
                             'darkred',
                             'violet'],
                     ds=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=4,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA/Wind Speed',
                     filename='RTMA Wind Speed.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     var_key='10m_wind_speed',
                     u_var_key='10m_u_wind_component',
                     v_var_key='10m_v_wind_component',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_to='mph',
                     pixel_query_type='barbs',
                     barb_length=4.5,
                     barb_width=0.5,
                     barb_color='black',
                     barb_zorder=7):
    
    """
    This function plots the latest Real Time Mesoscale Analysis (RTMA) for sustained wind speed.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Entire CONUS region.
            ii) 'jet' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Required Arguments: None
    
    Optional Arguments:
    
    1) region (String) - Default='conus'. The region of the plot. Use the 2-letter state abbreviation or 4-letter GACC abbreviation.
        If the user wants a completely custom region where they define their own lat/lon bounds, set region='custom'. 
        
    2) show_states (Boolean) - Default=True. When set to True, U.S. state borders are shown. 
    
    3) state_border_color (String) - Default='black'. The color of the U.S. state borders.
    
    4) state_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the U.S. state borders.
    
    5) state_border_zorder (Integer) - Default=3. The z-order of the state borders. For state borders to be displayed
        the following condition must be met: state_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
        
    6) show_counties (Boolean) - Default=True. When set to True, U.S. county borders are shown. 
    
    7) county_border_color (String) - Default='black'. The color of the U.S. county borders.
    
    8) county_border_linewidth (Float or Integer) - Default=0.25. The linewidth of the U.S. county borders.
    
    9) county_border_zorder (Integer) - Default=3. The z-order of the county borders. For county borders to be displayed
        the following condition must be met: county_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
    
    10) show_gacc_boundaries (Boolean) - Default=False. When set to True, Geographic Area Coordination Center borders are shown. 
    
    11) gacc_border_color (String) - Default='black'. The color of the Geographic Area Coordination Center borders.
    
    12) gacc_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the Geographic Area Coordination Center borders.
    
    13) gacc_border_zorder (Integer) - Default=3. The z-order of the Geographic Area Coordination Center borders. 
       For Geographic Area Coordination Center borders to be displayed the following condition must be met: gacc_border_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
       
    14) show_predictive_services_areas (Boolean) - Default=False. When set to True, Predictive Services Areas borders are shown. 
    
    15) predictive_services_areas_color (String) - Default='black'. The color of the Predictive Services Areas borders.
    
    16) predictive_services_areas_linewidth (Float or Integer) - Default=0.25. The linewidth of the Predictive Services Areas borders.
    
    17) predictive_services_areas_zorder (Integer) - Default=3. The z-order of the Predictive Services Areas borders. 
       For Predictive Services Areas borders to be displayed the following condition must be met: predictive_services_areas_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    18) show_nws_public_zones (Boolean) - Default=False. When set to True, NWS Public Zone borders are shown. 
    
    19) nws_public_zones_color (String) - Default='black'. The color of the NWS Public Zone borders.
    
    20) nws_public_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Public Zone borders.
    
    21) nws_public_zones_zorder (Integer) - Default=3. The z-order of the NWS Public Zone borders. 
       For NWS Public Zone borders to be displayed the following condition must be met: nws_public_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    22) show_nws_fire_weather_zones (Boolean) - Default=False. When set to True, NWS Fire Weather Zone borders are shown. 
    
    23) nws_fire_weather_zones_color (String) - Default='black'. The color of the NWS Fire Weather Zone borders.
    
    24) nws_fire_weather_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Fire Weather Zone borders.
    
    25) nws_fire_weather_zones_zorder (Integer) - Default=3. The z-order of the NWS Fire Weather Zone borders. 
       For NWS Fire Weather Zone borders to be displayed the following condition must be met: nws_fire_weather_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    26) show_nws_cwa (Boolean) - Default=False. When set to True, NWS CWA borders are shown.
    
    27) nws_cwa_color (String) - Default='black'. The color of the NWS CWA borders.
    
    28) nws_cwa_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS CWA borders.
    
    29) nws_cwa_zorder (Integer) - Default=3. The z-order of the NWS CWA borders. 
       For NWS CWA borders to be displayed the following condition must be met: nws_cwa_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    30) show_calfire_boundaries (Boolean) - Default=False. When set to True, CalFire borders are shown.
    
    31) calfire_boundary_color (String) - Default='black'. The color of the CalFire borders.
    
    32) calfire_boundary_linewidth (Float or Integer) - Default=0.25. The linewidth of the CalFire borders.
    
    33) calfire_boundary_zorder (Integer) - Default=3. The z-order of the CalFire borders. 
       For CalFire borders to be displayed the following condition must be met: calfire_boundary_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.

    34) custom_shapefile_url (String or None) - Default=None. If the user wishes to set up an automation importing geometry from a shapefile that
        is not in the base version of FireWxPy, this is how to do that. The user will pass the download URL as a string by setting
        custom_shapefile_url='https"//shapefile_download_url.file_extension'. 
        
    35) custom_shapefile_file_extension (String) - Default='.zip'. This is the file extension of the zipped shapefile folder on the web
        server. 
        
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    36) custom_shapefile_color (String) - Default='black'. The color of the borders in the custom shapefile.
    
    37) custom_shapefile_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders in the custom shapefile.
    
    38) custom_shapefile_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    39) custom_geojson_url (String) - Default=None. If the user wishes to set up an automation with a publicly available
        geojson on the web, pass in the full download URL into this argument.
    
    40) custom_geojson_filename (String) - Default=None. The filename of the custom geojson file. 
    
    41) custom_geojson_folder_name (String) Default='Custom GeoJSON'. The folder where the custom geojson will be saved in.
    
    42) custom_geojson_color (String) - Default='black'. The edge color of the geometries in the custom geojson file.
    
    43) custom_geojson_linewidth (Integer or Float) - Default=0.5. The linewidth of the borders in the custom geojson. 
    
    44) custom_geojson_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    45) custom_shapefile_local_path (String) - Default=None. The path to a shapefile locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    46) custom_shapefile_local_color (String) - Default='black'. The edge color of the geometries in the shapefile.
    
    47) custom_shapefile_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    48) custom_shapefile_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    49) custom_geojson_local_path (String) - Default=None. The path to a geojson locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    50) custom_geojson_local_color (String) - Default='black'. The edge color of the geometries in the geojson.
    
    51) custom_geojson_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    52) custom_geojson_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    53) convert_custom_shapefile_crs (Boolean)- Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom shapefile. 
        
    54) convert_local_custom_shapefile_crs (Boolean) - Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom geojson.
        
    55)  refresh_cartographic_files (Boolean) - Default=True. Users that have automated pipelines set up for shapefiles. Having this set to
        True allows the client to delete and re-download the shapefiles with each run of the script. This is useful for shapefiles
        that have frequent geometry updates.
        
    56) reference_system (String) - Default='States & Counties'. The name of the borders overlaid onto the map.
    
    57) show_rivers (Boolean) - Default=False. Set to True to display rivers. 
    
    58) rivers_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    59) rivers_color (String) - Default='lightcyan'. The color of the river. 
    
    60) figure_x_length (Integer) - Default=12. The length of the figure in the x-direction.
    
    61) figure_y_length (Integer) - Default=12. The length of the figure in the y-direction.
    
    62) coastline_linewidth (Float or Integer) - Default=0.75. The linewidth of the coastline.
    
    63) land_color (String) - Default='beige'. The color of the land on a map.
    
    64) ocean_color (String) - Default='lightcyan'. The color of the ocean on a map.
    
    65) lakes_color (String) - Default='lightcyan'. The color of lakes on a map. 

    66) costline_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    67) ocean_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    68) lakes_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    69) land_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    70) decimate (Integer) - Default=50. This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. When set to 50, every 50 values will be queried. Use
        larger numbers for larger areas and smaller values for smaller areas. The default of 50 represents the setting for
        CONUS. 
        
    71) start (Integer) - Default=0. The start of the filled contour range.
    
    72) stop (Integer) - Default=70. The end of the filled contour range. 
    
    73) step (Integer) - Default=1. The interval of the filled contours.
    
    74) facecolor (String) - Default='aliceblue'. The background color of the graphic. 
    
    75) primary_title_text (String) - Default='RTMA 10-METER WIND SPEED [MPH]'. The primary title
        of the graphic. 
        
    76) primary_title_textbox_color (String) - Default='wheat'. The color of the textbox of the primary title.
    
    77) primary_title_textbox_style (String) - Default='round'. The style of the textbox of the primary title.
    
    78) primary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    79) secondary_title_textbox_color (Float or Integer) Default='wheat'. The color of the textbox of the secondary title.
        
    80) secondary_title_textbox_style (String) - Default='round'. The style of the textbox of the secondary title.
    
    81) secondary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    82) primary_title_fontsize (Integer) - Default=12. Fontsize of the primary title text.
    
    83) secondary_title_fontsize (Integer) Default=10. Fontsize of the secondary title text.
    
    84) local_time (Boolean) - Default=True. Set to False for UTC time.
    
    85) signature_textbox_color (String) - Default='wheat'. The color of the textbox of the graphic's signature.
    
    86) signature_textbox_style (String) - Default='round'. The style of the textbox of the graphic's signature.
    
    87) signature_textbox_alpha (Float or Integer) - Default=1. A value between 0.5 and 1 representing transparency.

    88) signature_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    89) signature_fontsize (Integer) - Default=8. Fontsize of the graphic's signature text.
    
    90) signature_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the signature text box.
    
    91) signature_textbox_y_position (Float) - Default=-0.175. The y-position with respect to the plot axis of the signature text box.
    
    92) signature_text_new_lines (Boolean) - Default=False. When set to True, each section in the signature is on a new line.
        It is recommended to set this to True on plots that are longer from North to South than West to East. 
        
    93) reference_system_textbox_color (String) - Default='wheat'. The color of the textbox of the reference system.
    
    94) reference_system_textbox_style (String) - Default='round'. The style of the textbox of the reference system.
    
    95) reference_system_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    96) reference_system_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    97) reference_system_fontsize (Integer) - Default=6. Fontsize of the reference system label text.
    
    98) reference_system_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the reference system text box.
    
    99) reference_system_textbox_y_position (Float) - Default=0. The y-position with respect to the plot axis of the reference system text box.

    100) colorbar_shrink (Float or Integer) - Default=1. Fraction by which to multiply the size of the colorbar.
    
    101) colorbar_pad (Float) - Default=0.01. Fraction of original Axes between colorbar and new image Axes.
    
    102) tick_label_fontsize (Integer) - Default=9. The fontsize of the colorbar tick labels.
    
    103) colorbar_location (String) - Default='bottom'. The side of the plot axis where the colorbar will be displayed.
    
    104) colorbar_interval (Integer) - Default=10. The interval of tick marks on the colorbar.
    
    105) colorbar_aspect (Integer) - Default=50. Ratio of long to short dimensions.
    
    106) colormap (String) - Default='jet'. The Matplotlib colormap for filled contours being used OR set to 'custom' to create your own 
        custom colormapping. See the optional colors argument documentation (109) for more information on how to pass
        in a custom array of colors. 
        
    107) contourf_alpha (Float or Integer) - Default=0.5. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    108) contourf_zorder (Integer) - Default=2. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    109) colors (String List) - Default=['lightblue',
                                        'dodgerblue',
                                        'lime',
                                        'gold',
                                        'darkorange',
                                        'darkred',
                                        'violet']
                                        
            The array of colors being used when colormap='custom'. 
            
    110) ds (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds=ds. 
            
    111) western_bound (Float or Integer) - Default=-125. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    112) eastern_bound (Float or Integer) - Default=-65. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    113) southern_bound (Float or Integer) - Default=20. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    114) northern_bound (Float or Integer) - Default=50. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    115) pixel_query_value_fontsize (Integer) - Default=4. The fontsize of the pixel query values.
    
    116) pixel_query_value_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    117) pixel_query_value_foreground (String) - Default='white'. The color of the foreground on the station plot (pixel query value).
    
    118) pixel_query_value_fontcolor (String) - Default='black'. The font color of the pixel query values.
    
    119) pixel_query_stroke_linewidth (Float or Integer) - Default=1. The linewidth of the pixel query values text outline.
    
    120) path (String) - Default='FireWxPy Graphics/RTMA/Wind Speed'. The directory where the graphic will save.
    
    121) filename (String) - Default='RTMA Wind Speed.png'. The filename of the image.
    
    122) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    123) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
        
    124) clear_data (Boolean) - Default=True. When set to True, the data will be cleared with each run of the script.
        Set to False when downloading the data outside of the function and passing the data in. 
        
    125) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB data to a file.
    
    126) notifications (String) - Default='off'. Notifications throughout the process. 

    127) custom_data_directory (String or None) - Default=None. The directory path where the data will be saved to. 

    128) mapcrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the map.
    
    129) datacrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the data.

    130) var_key (String) - Default='10m_wind_speed'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    130) u_var_key (String) - Default='10m_u_wind_component'. The variable key name of the u-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    130) v_var_key (String) - Default='10m_v_wind_component'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    131) time_coord_key (String) - Default='time'. The time coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    132) longitude_key (String) - Default='longitude'. The longitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
    
    133) latitude_key (String) - Default='latitude'. The latitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    134) convert_wind_speed (Boolean) - Default=True. Convert wind speed from m/s to either mph or kts.
    
    135) convert_to (String) - Default='mph'. Set to 'kts' for knots.
    
    136) pixel_query_type (String) - Default='barbs'. Display either wind barbs or numerical values.
    
    137) barb_length (Float or Integer) - Default=4.5. Length of wind barb.
    
    138) barb_width (Float or Integer) - Default=0.5. Width of wind barb. 
    
    139) barb_color (String) - Default='black'. Color of wind barb. 
    
    140) barb_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.

    Returns
    -------
    
    An image of the RTMA Wind Speed Analysis specified to the user's needs saved to {path}    
    """
    
    _build_directory_branch(f"{path}/{region.upper()}/{reference_system.upper()}")
    
    _mpl.rcParams['xtick.labelsize'] = tick_label_fontsize
    _mpl.rcParams['ytick.labelsize'] = tick_label_fontsize
    
    primary_title_box = dict(boxstyle=primary_title_textbox_style, 
                            facecolor=primary_title_textbox_color, 
                            alpha=primary_title_textbox_alpha)
    
    secondary_title_box = dict(boxstyle=secondary_title_textbox_style, 
                            facecolor=secondary_title_textbox_color, 
                            alpha=secondary_title_textbox_alpha)
    
    signature_box = dict(boxstyle=signature_textbox_style, 
                            facecolor=signature_textbox_color, 
                            alpha=signature_textbox_alpha)
    
    reference_system_box = dict(boxstyle=reference_system_textbox_style, 
                            facecolor=reference_system_textbox_color, 
                            alpha=reference_system_textbox_alpha)
    
    levels = _np.arange(start, (stop + step), step)
    ticks = levels[::colorbar_interval]
    
    western_bound, eastern_bound, southern_bound, northern_bound = _bounding_box(region,
                                                                                 western_bound,
                                                                                 eastern_bound,
                                                                                 southern_bound,
                                                                                 northern_bound)
    
    if ds is None:
        ds = _rtma(proxies=proxies,
                   clear_recycle_bin=clear_recycle_bin,
                   clear_data=clear_data,
                   western_bound=western_bound,
                   eastern_bound=eastern_bound,
                   southern_bound=southern_bound,
                   northern_bound=northern_bound,
                   convert_temperature=True,
                   convert_to='fahrenheit',
                   chunk_size=chunk_size,
                   notifications=notifications,
                   custom_directory=custom_data_directory)
    else:
        ds = ds
        
    if convert_wind_speed == True:
        if convert_to == 'mph':
            ds[var_key] = _calc.mps_to_mph(ds[var_key])
            ds[u_var_key] = _calc.mps_to_mph(ds[u_var_key])
            ds[v_var_key] = _calc.mps_to_mph(ds[v_var_key])
        else:
            ds[var_key] = _calc.mph_to_kts(ds[var_key])
            ds[u_var_key] = _calc.mph_to_kts(ds[u_var_key])
            ds[v_var_key] = _calc.mph_to_kts(ds[v_var_key])
            
    else:
        pass
        
    if colormap == 'custom':
        cmap = _mcolors.LinearSegmentedColormap.from_list("wind speed", colors)
    else:
        cmap = colormap
    
    valid_time = _pd.to_datetime(ds[time_coord_key].to_pandas())
    valid_time = valid_time.tz_localize('UTC')
    time = valid_time.astimezone(_to_zone)
    time_utc = time.astimezone(_from_zone)
    
    fig = _plt.figure(figsize=(figure_x_length, figure_y_length))
    fig.set_facecolor(facecolor)
    
    ax = fig.add_subplot(1,1,1, projection=mapcrs)
    ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax.add_feature(_cfeature.COASTLINE.with_scale('50m'), linewidth=coastline_linewidth, zorder=costline_zorder)
    ax.add_feature(_cfeature.LAND, color=land_color, zorder=land_zorder)
    ax.add_feature(_cfeature.OCEAN, color=ocean_color, zorder=ocean_zorder)
    ax.add_feature(_cfeature.LAKES, color=lakes_color, zorder=lakes_zorder)
    if show_rivers is True:
        ax.add_feature(_cfeature.RIVERS, color=rivers_color, zorder=rivers_zorder)
    if show_states is True:
        states = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_States_Territories.zip",
                                            f"Cartographic Files/US States",
                                            f"US_States_Territories.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            state_border_color,
                                            datacrs)
        
        ax.add_geometries(states, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=state_border_color, 
                          linewidth=state_border_linewidth, 
                          zorder=state_border_zorder)
    
    if show_counties is True:
        counties = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_Counties.zip",
                                            f"Cartographic Files/US Counties",
                                            f"US_Counties.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            county_border_color,
                                            datacrs)
        
        ax.add_geometries(counties, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=county_border_color, 
                          linewidth=county_border_linewidth, 
                          zorder=county_border_zorder)
        
    if show_gacc_boundaries is True:
        gacc = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/GACC_Boundaries_2026.zip",
                                            f"Cartographic Files/GACC Boundaries",
                                            f"GACC_Boundaries_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            gacc_border_color,
                                            datacrs)
        
        ax.add_geometries(gacc, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=gacc_border_color, 
                          linewidth=gacc_border_linewidth, 
                          zorder=gacc_border_zorder)
    
    if show_predictive_services_areas is True:
        psa = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/PSA_Boundaries.zip",
                                            f"Cartographic Files/PSA Boundaries",
                                            f"PSA_Boundaries.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            predictive_services_areas_color,
                                            datacrs)
        
        ax.add_geometries(psa, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=predictive_services_areas_color, 
                          linewidth=predictive_services_areas_linewidth, 
                          zorder=predictive_services_areas_zorder)
        
    if show_nws_public_zones is True:
        pz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Public_Zones_2026.zip",
                                            f"Cartographic Files/NWS Public Zones",
                                            f"NWS_Public_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_public_zones_color,
                                            datacrs)
        
        ax.add_geometries(pz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_public_zones_color, 
                          linewidth=nws_public_zones_linewidth, 
                          zorder=nws_public_zones_zorder)
        
    if show_nws_fire_weather_zones is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Fire_Weather_Zones_2026.zip",
                                            f"Cartographic Files/NWS Fire Weather Zones",
                                            f"NWS_Fire_Weather_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_fire_weather_zones_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_fire_weather_zones_color, 
                          linewidth=nws_fire_weather_zones_linewidth, 
                          zorder=nws_fire_weather_zones_zorder)
        
    if show_nws_cwa is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_CWA_2026.zip",
                                            f"Cartographic Files/NWS CWAs",
                                            f"NWS_CWA_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_cwa_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_cwa_color, 
                          linewidth=nws_cwa_linewidth, 
                          zorder=nws_cwa_zorder)
        
    if show_calfire_boundaries is True:
        calfire = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/CALFIRE/CalFire_Administrative_Units.zip",
                                            f"Cartographic Files/CalFire",
                                            f"CalFire_Administrative_Units.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            calfire_boundary_color,
                                            datacrs,
                                            convert_crs=True,
                                            convert_to='EPSG:4326')
        
        ax.add_geometries(calfire, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=calfire_boundary_color, 
                          linewidth=calfire_boundary_linewidth, 
                          zorder=calfire_boundary_zorder)
        
    if custom_shapefile_url is not None:
        
        fname = _get_filename_from_url(custom_shapefile_url)
        
        custom_shape = _import_shapefile_from_web(custom_shapefile_url,
                                            f"Cartographic Files/{custom_shapefile_folder_name}",
                                            fname,
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            custom_shapefile_file_extension,
                                            custom_shapefile_color,
                                            convert_crs=convert_custom_shapefile_crs)
        
        ax.add_geometries(custom_shape, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_color, 
                          linewidth=custom_shapefile_linewidth, 
                          zorder=custom_shapefile_zorder)
        
    if custom_geojson_url is not None:
        
        custom_json = _import_geojson_from_web(custom_geojson_url,
                                                f"Cartographic Files/{custom_geojson_folder_name}", 
                                                custom_geojson_filename, 
                                                proxies, 
                                                chunk_size,
                                                notifications, 
                                                refresh_cartographic_files)
        
        ax.add_geometries(custom_json, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_color, 
                          linewidth=custom_geojson_linewidth, 
                          zorder=custom_geojson_zorder)
        
    if custom_shapefile_local_path is not None:
        custom_local_shapefile = _import_shapefile_local(custom_shapefile_local_path,
                                                            custom_shapefile_local_color,
                                                            convert_crs=convert_local_custom_shapefile_crs)
        
        ax.add_geometries(custom_local_shapefile, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_local_color, 
                          linewidth=custom_shapefile_local_linewidth, 
                          zorder=custom_shapefile_local_zorder)
        
    if custom_geojson_local_path is not None:
        custom_local_geojson = _import_geojson_local(custom_geojson_local_path)
        
        ax.add_geometries(custom_local_geojson, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_local_color, 
                          linewidth=custom_geojson_local_linewidth, 
                          zorder=custom_geojson_local_zorder)
    
    cs = ax.contourf(ds[longitude_key],
                ds[latitude_key],
                ds[var_key],
                cmap=cmap,
                levels=levels,
                transform=datacrs,
                alpha=contourf_alpha,
                zorder=contourf_zorder,
                extend='both')
    
    fig.colorbar(cs, 
                shrink=colorbar_shrink, 
                pad=colorbar_pad, 
                location=colorbar_location,
                ticks=ticks,
                aspect=colorbar_aspect)
    
    _plt.title(f"{primary_title_text}", 
               fontsize=primary_title_fontsize, 
               fontweight='bold',
               bbox=primary_title_box,
               loc='left')
    
    if local_time is True:
        _plt.title(f"Valid: {time.strftime('%m/%d/%Y %H:00')} {_timezone}", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
    else:
        _plt.title(f"Valid: {time_utc.strftime('%m/%d/%Y %H:00')} UTC", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
        
    if signature_text_new_lines is False:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')} | Data Source: NCEP/NOMADS | Created: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    else:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')}\nData Source: NCEP/NOMADS\nCreated: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    
    ax.text(reference_system_textbox_x_position, 
            reference_system_textbox_y_position,
            f"Reference System: {reference_system}",
            fontsize=reference_system_fontsize,
            fontweight='bold',
            bbox=reference_system_box,
            transform=ax.transAxes,
            zorder=reference_system_textbox_zorder)
        
    
        
    vals = _fix_var_array(ds,
                    var_key,
                    0,
                    decimate)
    
    u_vals = _fix_var_array(ds,
                    u_var_key,
                    0,
                    decimate)
    
    v_vals = _fix_var_array(ds,
                    v_var_key,
                    0,
                    decimate)

    stn = _mpplots.StationPlot(ax, vals['longitude'], vals['latitude'],
                                transform=datacrs, 
                                fontsize=pixel_query_value_fontsize, 
                                zorder=pixel_query_value_zorder, 
                                clip_on=True)

    if pixel_query_type != 'barbs':
        stn.plot_parameter('C', 
                            vals[var_key], 
                            color=pixel_query_value_fontcolor, 
                            path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                        foreground=pixel_query_value_foreground)], 
                            zorder=pixel_query_value_zorder)

    else:
        stn.plot_barb(u_vals[u_var_key], 
                        v_vals[v_var_key],
                        color=barb_color, 
                        length=barb_length, 
                        linewidth=barb_width,
                        zorder=barb_zorder)

    fig.savefig(f"{path}/{region.upper()}/{reference_system.upper()}/{filename}", bbox_inches='tight')
    _plt.close(fig)
    if notifications == 'on':
        print(f"{filename} saved to {path}/{region.upper()}")
        
def plot_wind_gust(region='conus',
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=50,
                     start=0,
                     stop=70,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 10-METER WIND GUST [MPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=12,
                     secondary_title_fontsize=10,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=10,
                     colorbar_aspect=50,
                     colormap='jet',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['lightblue',
                             'dodgerblue',
                             'lime',
                             'gold',
                             'darkorange',
                             'darkred',
                             'violet'],
                     ds=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=4,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA/Wind Gust',
                     filename='RTMA Wind Gust.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     var_key='10m_wind_gust',
                     u_var_key='10m_u_wind_component',
                     v_var_key='10m_v_wind_component',
                     wind_direction_var_key='10m_wind_direction',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_to='mph',
                     pixel_query_type='barbs',
                     barb_length=4.5,
                     barb_width=0.5,
                     barb_color='black',
                     barb_zorder=7):
    
    """
    This function plots the latest Real Time Mesoscale Analysis (RTMA) for wind gust.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Entire CONUS region.
            ii) 'jet' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Required Arguments: None
    
    Optional Arguments:
    
    1) region (String) - Default='conus'. The region of the plot. Use the 2-letter state abbreviation or 4-letter GACC abbreviation.
        If the user wants a completely custom region where they define their own lat/lon bounds, set region='custom'. 
        
    2) show_states (Boolean) - Default=True. When set to True, U.S. state borders are shown. 
    
    3) state_border_color (String) - Default='black'. The color of the U.S. state borders.
    
    4) state_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the U.S. state borders.
    
    5) state_border_zorder (Integer) - Default=3. The z-order of the state borders. For state borders to be displayed
        the following condition must be met: state_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
        
    6) show_counties (Boolean) - Default=True. When set to True, U.S. county borders are shown. 
    
    7) county_border_color (String) - Default='black'. The color of the U.S. county borders.
    
    8) county_border_linewidth (Float or Integer) - Default=0.25. The linewidth of the U.S. county borders.
    
    9) county_border_zorder (Integer) - Default=3. The z-order of the county borders. For county borders to be displayed
        the following condition must be met: county_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
    
    10) show_gacc_boundaries (Boolean) - Default=False. When set to True, Geographic Area Coordination Center borders are shown. 
    
    11) gacc_border_color (String) - Default='black'. The color of the Geographic Area Coordination Center borders.
    
    12) gacc_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the Geographic Area Coordination Center borders.
    
    13) gacc_border_zorder (Integer) - Default=3. The z-order of the Geographic Area Coordination Center borders. 
       For Geographic Area Coordination Center borders to be displayed the following condition must be met: gacc_border_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
       
    14) show_predictive_services_areas (Boolean) - Default=False. When set to True, Predictive Services Areas borders are shown. 
    
    15) predictive_services_areas_color (String) - Default='black'. The color of the Predictive Services Areas borders.
    
    16) predictive_services_areas_linewidth (Float or Integer) - Default=0.25. The linewidth of the Predictive Services Areas borders.
    
    17) predictive_services_areas_zorder (Integer) - Default=3. The z-order of the Predictive Services Areas borders. 
       For Predictive Services Areas borders to be displayed the following condition must be met: predictive_services_areas_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    18) show_nws_public_zones (Boolean) - Default=False. When set to True, NWS Public Zone borders are shown. 
    
    19) nws_public_zones_color (String) - Default='black'. The color of the NWS Public Zone borders.
    
    20) nws_public_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Public Zone borders.
    
    21) nws_public_zones_zorder (Integer) - Default=3. The z-order of the NWS Public Zone borders. 
       For NWS Public Zone borders to be displayed the following condition must be met: nws_public_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    22) show_nws_fire_weather_zones (Boolean) - Default=False. When set to True, NWS Fire Weather Zone borders are shown. 
    
    23) nws_fire_weather_zones_color (String) - Default='black'. The color of the NWS Fire Weather Zone borders.
    
    24) nws_fire_weather_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Fire Weather Zone borders.
    
    25) nws_fire_weather_zones_zorder (Integer) - Default=3. The z-order of the NWS Fire Weather Zone borders. 
       For NWS Fire Weather Zone borders to be displayed the following condition must be met: nws_fire_weather_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    26) show_nws_cwa (Boolean) - Default=False. When set to True, NWS CWA borders are shown.
    
    27) nws_cwa_color (String) - Default='black'. The color of the NWS CWA borders.
    
    28) nws_cwa_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS CWA borders.
    
    29) nws_cwa_zorder (Integer) - Default=3. The z-order of the NWS CWA borders. 
       For NWS CWA borders to be displayed the following condition must be met: nws_cwa_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    30) show_calfire_boundaries (Boolean) - Default=False. When set to True, CalFire borders are shown.
    
    31) calfire_boundary_color (String) - Default='black'. The color of the CalFire borders.
    
    32) calfire_boundary_linewidth (Float or Integer) - Default=0.25. The linewidth of the CalFire borders.
    
    33) calfire_boundary_zorder (Integer) - Default=3. The z-order of the CalFire borders. 
       For CalFire borders to be displayed the following condition must be met: calfire_boundary_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.

    34) custom_shapefile_url (String or None) - Default=None. If the user wishes to set up an automation importing geometry from a shapefile that
        is not in the base version of FireWxPy, this is how to do that. The user will pass the download URL as a string by setting
        custom_shapefile_url='https"//shapefile_download_url.file_extension'. 
        
    35) custom_shapefile_file_extension (String) - Default='.zip'. This is the file extension of the zipped shapefile folder on the web
        server. 
        
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    36) custom_shapefile_color (String) - Default='black'. The color of the borders in the custom shapefile.
    
    37) custom_shapefile_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders in the custom shapefile.
    
    38) custom_shapefile_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    39) custom_geojson_url (String) - Default=None. If the user wishes to set up an automation with a publicly available
        geojson on the web, pass in the full download URL into this argument.
    
    40) custom_geojson_filename (String) - Default=None. The filename of the custom geojson file. 
    
    41) custom_geojson_folder_name (String) Default='Custom GeoJSON'. The folder where the custom geojson will be saved in.
    
    42) custom_geojson_color (String) - Default='black'. The edge color of the geometries in the custom geojson file.
    
    43) custom_geojson_linewidth (Integer or Float) - Default=0.5. The linewidth of the borders in the custom geojson. 
    
    44) custom_geojson_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    45) custom_shapefile_local_path (String) - Default=None. The path to a shapefile locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    46) custom_shapefile_local_color (String) - Default='black'. The edge color of the geometries in the shapefile.
    
    47) custom_shapefile_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    48) custom_shapefile_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    49) custom_geojson_local_path (String) - Default=None. The path to a geojson locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    50) custom_geojson_local_color (String) - Default='black'. The edge color of the geometries in the geojson.
    
    51) custom_geojson_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    52) custom_geojson_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    53) convert_custom_shapefile_crs (Boolean)- Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom shapefile. 
        
    54) convert_local_custom_shapefile_crs (Boolean) - Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom geojson.
        
    55)  refresh_cartographic_files (Boolean) - Default=True. Users that have automated pipelines set up for shapefiles. Having this set to
        True allows the client to delete and re-download the shapefiles with each run of the script. This is useful for shapefiles
        that have frequent geometry updates.
        
    56) reference_system (String) - Default='States & Counties'. The name of the borders overlaid onto the map.
    
    57) show_rivers (Boolean) - Default=False. Set to True to display rivers. 
    
    58) rivers_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    59) rivers_color (String) - Default='lightcyan'. The color of the river. 
    
    60) figure_x_length (Integer) - Default=12. The length of the figure in the x-direction.
    
    61) figure_y_length (Integer) - Default=12. The length of the figure in the y-direction.
    
    62) coastline_linewidth (Float or Integer) - Default=0.75. The linewidth of the coastline.
    
    63) land_color (String) - Default='beige'. The color of the land on a map.
    
    64) ocean_color (String) - Default='lightcyan'. The color of the ocean on a map.
    
    65) lakes_color (String) - Default='lightcyan'. The color of lakes on a map. 

    66) costline_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    67) ocean_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    68) lakes_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    69) land_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    70) decimate (Integer) - Default=50. This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. When set to 50, every 50 values will be queried. Use
        larger numbers for larger areas and smaller values for smaller areas. The default of 50 represents the setting for
        CONUS. 
        
    71) start (Integer) - Default=0. The start of the filled contour range.
    
    72) stop (Integer) - Default=70. The end of the filled contour range. 
    
    73) step (Integer) - Default=1. The interval of the filled contours.
    
    74) facecolor (String) - Default='aliceblue'. The background color of the graphic. 
    
    75) primary_title_text (String) - Default='RTMA 10-METER WIND GUST [MPH]'. The primary title
        of the graphic. 
        
    76) primary_title_textbox_color (String) - Default='wheat'. The color of the textbox of the primary title.
    
    77) primary_title_textbox_style (String) - Default='round'. The style of the textbox of the primary title.
    
    78) primary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    79) secondary_title_textbox_color (Float or Integer) Default='wheat'. The color of the textbox of the secondary title.
        
    80) secondary_title_textbox_style (String) - Default='round'. The style of the textbox of the secondary title.
    
    81) secondary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    82) primary_title_fontsize (Integer) - Default=12. Fontsize of the primary title text.
    
    83) secondary_title_fontsize (Integer) Default=10. Fontsize of the secondary title text.
    
    84) local_time (Boolean) - Default=True. Set to False for UTC time.
    
    85) signature_textbox_color (String) - Default='wheat'. The color of the textbox of the graphic's signature.
    
    86) signature_textbox_style (String) - Default='round'. The style of the textbox of the graphic's signature.
    
    87) signature_textbox_alpha (Float or Integer) - Default=1. A value between 0.5 and 1 representing transparency.

    88) signature_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    89) signature_fontsize (Integer) - Default=8. Fontsize of the graphic's signature text.
    
    90) signature_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the signature text box.
    
    91) signature_textbox_y_position (Float) - Default=-0.175. The y-position with respect to the plot axis of the signature text box.
    
    92) signature_text_new_lines (Boolean) - Default=False. When set to True, each section in the signature is on a new line.
        It is recommended to set this to True on plots that are longer from North to South than West to East. 
        
    93) reference_system_textbox_color (String) - Default='wheat'. The color of the textbox of the reference system.
    
    94) reference_system_textbox_style (String) - Default='round'. The style of the textbox of the reference system.
    
    95) reference_system_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    96) reference_system_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    97) reference_system_fontsize (Integer) - Default=6. Fontsize of the reference system label text.
    
    98) reference_system_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the reference system text box.
    
    99) reference_system_textbox_y_position (Float) - Default=0. The y-position with respect to the plot axis of the reference system text box.

    100) colorbar_shrink (Float or Integer) - Default=1. Fraction by which to multiply the size of the colorbar.
    
    101) colorbar_pad (Float) - Default=0.01. Fraction of original Axes between colorbar and new image Axes.
    
    102) tick_label_fontsize (Integer) - Default=9. The fontsize of the colorbar tick labels.
    
    103) colorbar_location (String) - Default='bottom'. The side of the plot axis where the colorbar will be displayed.
    
    104) colorbar_interval (Integer) - Default=10. The interval of tick marks on the colorbar.
    
    105) colorbar_aspect (Integer) - Default=50. Ratio of long to short dimensions.
    
    106) colormap (String) - Default='jet'. The Matplotlib colormap for filled contours being used OR set to 'custom' to create your own 
        custom colormapping. See the optional colors argument documentation (109) for more information on how to pass
        in a custom array of colors. 
        
    107) contourf_alpha (Float or Integer) - Default=0.5. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    108) contourf_zorder (Integer) - Default=2. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    109) colors (String List) - Default=['lightblue',
                                        'dodgerblue',
                                        'lime',
                                        'gold',
                                        'darkorange',
                                        'darkred',
                                        'violet']
                                        
            The array of colors being used when colormap='custom'. 
            
    110) ds (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds=ds. 
            
    111) western_bound (Float or Integer) - Default=-125. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    112) eastern_bound (Float or Integer) - Default=-65. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    113) southern_bound (Float or Integer) - Default=20. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    114) northern_bound (Float or Integer) - Default=50. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    115) pixel_query_value_fontsize (Integer) - Default=4. The fontsize of the pixel query values.
    
    116) pixel_query_value_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    117) pixel_query_value_foreground (String) - Default='white'. The color of the foreground on the station plot (pixel query value).
    
    118) pixel_query_value_fontcolor (String) - Default='black'. The font color of the pixel query values.
    
    119) pixel_query_stroke_linewidth (Float or Integer) - Default=1. The linewidth of the pixel query values text outline.
    
    120) path (String) - Default='FireWxPy Graphics/RTMA/Wind Gust'. The directory where the graphic will save.
    
    121) filename (String) - Default='RTMA Wind Gust.png'. The filename of the image.
    
    122) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    123) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
        
    124) clear_data (Boolean) - Default=True. When set to True, the data will be cleared with each run of the script.
        Set to False when downloading the data outside of the function and passing the data in. 
        
    125) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB data to a file.
    
    126) notifications (String) - Default='off'. Notifications throughout the process. 

    127) custom_data_directory (String or None) - Default=None. The directory path where the data will be saved to. 

    128) mapcrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the map.
    
    129) datacrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the data.

    130) var_key (String) - Default='10m_wind_speed'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    130) u_var_key (String) - Default='10m_u_wind_component'. The variable key name of the u-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    130) v_var_key (String) - Default='10m_v_wind_component'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    131) wind_direction_var_key (String) - Default='10m_wind_direction'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    132) time_coord_key (String) - Default='time'. The time coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    133) longitude_key (String) - Default='longitude'. The longitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
    
    134) latitude_key (String) - Default='latitude'. The latitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    135) convert_wind_speed (Boolean) - Default=True. Convert wind speed from m/s to either mph or kts.
    
    136) convert_to (String) - Default='mph'. Set to 'kts' for knots.
    
    137) pixel_query_type (String) - Default='barbs'. Display either wind barbs or numerical values.
    
    138) barb_length (Float or Integer) - Default=4.5. Length of wind barb.
    
    139) barb_width (Float or Integer) - Default=0.5. Width of wind barb. 
    
    140) barb_color (String) - Default='black'. Color of wind barb. 
    
    141) barb_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.

    Returns
    -------
    
    An image of the RTMA Wind Gust Analysis specified to the user's needs saved to {path}    
    """
    
    _build_directory_branch(f"{path}/{region.upper()}/{reference_system.upper()}")
    
    _mpl.rcParams['xtick.labelsize'] = tick_label_fontsize
    _mpl.rcParams['ytick.labelsize'] = tick_label_fontsize
    
    primary_title_box = dict(boxstyle=primary_title_textbox_style, 
                            facecolor=primary_title_textbox_color, 
                            alpha=primary_title_textbox_alpha)
    
    secondary_title_box = dict(boxstyle=secondary_title_textbox_style, 
                            facecolor=secondary_title_textbox_color, 
                            alpha=secondary_title_textbox_alpha)
    
    signature_box = dict(boxstyle=signature_textbox_style, 
                            facecolor=signature_textbox_color, 
                            alpha=signature_textbox_alpha)
    
    reference_system_box = dict(boxstyle=reference_system_textbox_style, 
                            facecolor=reference_system_textbox_color, 
                            alpha=reference_system_textbox_alpha)
    
    levels = _np.arange(start, (stop + step), step)
    ticks = levels[::colorbar_interval]
    
    western_bound, eastern_bound, southern_bound, northern_bound = _bounding_box(region,
                                                                                 western_bound,
                                                                                 eastern_bound,
                                                                                 southern_bound,
                                                                                 northern_bound)
    
    if ds is None:
        ds = _rtma(proxies=proxies,
                   clear_recycle_bin=clear_recycle_bin,
                   clear_data=clear_data,
                   western_bound=western_bound,
                   eastern_bound=eastern_bound,
                   southern_bound=southern_bound,
                   northern_bound=northern_bound,
                   convert_temperature=True,
                   convert_to='fahrenheit',
                   chunk_size=chunk_size,
                   notifications=notifications,
                   custom_directory=custom_data_directory)
    else:
        ds = ds
        
    if convert_wind_speed == True:
        if convert_to == 'mph':
            ds[var_key] = _calc.mps_to_mph(ds[var_key])
            ds[u_var_key] = _calc.mps_to_mph(ds[u_var_key])
            ds[v_var_key] = _calc.mps_to_mph(ds[v_var_key])
        else:
            ds[var_key] = _calc.mph_to_kts(ds[var_key])
            ds[u_var_key] = _calc.mph_to_kts(ds[u_var_key])
            ds[v_var_key] = _calc.mph_to_kts(ds[v_var_key])
            
    else:
        pass
    
    ds = _calc.u_v_components(ds,
                            u_var_key,
                            v_var_key,
                            wind_direction_var_key,
                            var_key)
        
    if colormap == 'custom':
        cmap = _mcolors.LinearSegmentedColormap.from_list("wind gust", colors)
    else:
        cmap = colormap
    
    valid_time = _pd.to_datetime(ds[time_coord_key].to_pandas())
    valid_time = valid_time.tz_localize('UTC')
    time = valid_time.astimezone(_to_zone)
    time_utc = time.astimezone(_from_zone)
    
    fig = _plt.figure(figsize=(figure_x_length, figure_y_length))
    fig.set_facecolor(facecolor)
    
    ax = fig.add_subplot(1,1,1, projection=mapcrs)
    ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax.add_feature(_cfeature.COASTLINE.with_scale('50m'), linewidth=coastline_linewidth, zorder=costline_zorder)
    ax.add_feature(_cfeature.LAND, color=land_color, zorder=land_zorder)
    ax.add_feature(_cfeature.OCEAN, color=ocean_color, zorder=ocean_zorder)
    ax.add_feature(_cfeature.LAKES, color=lakes_color, zorder=lakes_zorder)
    if show_rivers is True:
        ax.add_feature(_cfeature.RIVERS, color=rivers_color, zorder=rivers_zorder)
    if show_states is True:
        states = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_States_Territories.zip",
                                            f"Cartographic Files/US States",
                                            f"US_States_Territories.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            state_border_color,
                                            datacrs)
        
        ax.add_geometries(states, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=state_border_color, 
                          linewidth=state_border_linewidth, 
                          zorder=state_border_zorder)
    
    if show_counties is True:
        counties = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_Counties.zip",
                                            f"Cartographic Files/US Counties",
                                            f"US_Counties.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            county_border_color,
                                            datacrs)
        
        ax.add_geometries(counties, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=county_border_color, 
                          linewidth=county_border_linewidth, 
                          zorder=county_border_zorder)
        
    if show_gacc_boundaries is True:
        gacc = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/GACC_Boundaries_2026.zip",
                                            f"Cartographic Files/GACC Boundaries",
                                            f"GACC_Boundaries_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            gacc_border_color,
                                            datacrs)
        
        ax.add_geometries(gacc, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=gacc_border_color, 
                          linewidth=gacc_border_linewidth, 
                          zorder=gacc_border_zorder)
    
    if show_predictive_services_areas is True:
        psa = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/PSA_Boundaries.zip",
                                            f"Cartographic Files/PSA Boundaries",
                                            f"PSA_Boundaries.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            predictive_services_areas_color,
                                            datacrs)
        
        ax.add_geometries(psa, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=predictive_services_areas_color, 
                          linewidth=predictive_services_areas_linewidth, 
                          zorder=predictive_services_areas_zorder)
        
    if show_nws_public_zones is True:
        pz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Public_Zones_2026.zip",
                                            f"Cartographic Files/NWS Public Zones",
                                            f"NWS_Public_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_public_zones_color,
                                            datacrs)
        
        ax.add_geometries(pz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_public_zones_color, 
                          linewidth=nws_public_zones_linewidth, 
                          zorder=nws_public_zones_zorder)
        
    if show_nws_fire_weather_zones is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Fire_Weather_Zones_2026.zip",
                                            f"Cartographic Files/NWS Fire Weather Zones",
                                            f"NWS_Fire_Weather_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_fire_weather_zones_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_fire_weather_zones_color, 
                          linewidth=nws_fire_weather_zones_linewidth, 
                          zorder=nws_fire_weather_zones_zorder)
        
    if show_nws_cwa is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_CWA_2026.zip",
                                            f"Cartographic Files/NWS CWAs",
                                            f"NWS_CWA_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_cwa_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_cwa_color, 
                          linewidth=nws_cwa_linewidth, 
                          zorder=nws_cwa_zorder)
        
    if show_calfire_boundaries is True:
        calfire = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/CALFIRE/CalFire_Administrative_Units.zip",
                                            f"Cartographic Files/CalFire",
                                            f"CalFire_Administrative_Units.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            calfire_boundary_color,
                                            datacrs,
                                            convert_crs=True,
                                            convert_to='EPSG:4326')
        
        ax.add_geometries(calfire, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=calfire_boundary_color, 
                          linewidth=calfire_boundary_linewidth, 
                          zorder=calfire_boundary_zorder)
        
    if custom_shapefile_url is not None:
        
        fname = _get_filename_from_url(custom_shapefile_url)
        
        custom_shape = _import_shapefile_from_web(custom_shapefile_url,
                                            f"Cartographic Files/{custom_shapefile_folder_name}",
                                            fname,
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            custom_shapefile_file_extension,
                                            custom_shapefile_color,
                                            convert_crs=convert_custom_shapefile_crs)
        
        ax.add_geometries(custom_shape, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_color, 
                          linewidth=custom_shapefile_linewidth, 
                          zorder=custom_shapefile_zorder)
        
    if custom_geojson_url is not None:
        
        custom_json = _import_geojson_from_web(custom_geojson_url,
                                                f"Cartographic Files/{custom_geojson_folder_name}", 
                                                custom_geojson_filename, 
                                                proxies, 
                                                chunk_size,
                                                notifications, 
                                                refresh_cartographic_files)
        
        ax.add_geometries(custom_json, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_color, 
                          linewidth=custom_geojson_linewidth, 
                          zorder=custom_geojson_zorder)
        
    if custom_shapefile_local_path is not None:
        custom_local_shapefile = _import_shapefile_local(custom_shapefile_local_path,
                                                            custom_shapefile_local_color,
                                                            convert_crs=convert_local_custom_shapefile_crs)
        
        ax.add_geometries(custom_local_shapefile, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_local_color, 
                          linewidth=custom_shapefile_local_linewidth, 
                          zorder=custom_shapefile_local_zorder)
        
    if custom_geojson_local_path is not None:
        custom_local_geojson = _import_geojson_local(custom_geojson_local_path)
        
        ax.add_geometries(custom_local_geojson, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_local_color, 
                          linewidth=custom_geojson_local_linewidth, 
                          zorder=custom_geojson_local_zorder)
    
    cs = ax.contourf(ds[longitude_key],
                ds[latitude_key],
                ds[var_key],
                cmap=cmap,
                levels=levels,
                transform=datacrs,
                alpha=contourf_alpha,
                zorder=contourf_zorder,
                extend='both')
    
    fig.colorbar(cs, 
                shrink=colorbar_shrink, 
                pad=colorbar_pad, 
                location=colorbar_location,
                ticks=ticks,
                aspect=colorbar_aspect)
    
    _plt.title(f"{primary_title_text}", 
               fontsize=primary_title_fontsize, 
               fontweight='bold',
               bbox=primary_title_box,
               loc='left')
    
    if local_time is True:
        _plt.title(f"Valid: {time.strftime('%m/%d/%Y %H:00')} {_timezone}", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
    else:
        _plt.title(f"Valid: {time_utc.strftime('%m/%d/%Y %H:00')} UTC", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
        
    if signature_text_new_lines is False:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')} | Data Source: NCEP/NOMADS | Created: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    else:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')}\nData Source: NCEP/NOMADS\nCreated: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    
    ax.text(reference_system_textbox_x_position, 
            reference_system_textbox_y_position,
            f"Reference System: {reference_system}",
            fontsize=reference_system_fontsize,
            fontweight='bold',
            bbox=reference_system_box,
            transform=ax.transAxes,
            zorder=reference_system_textbox_zorder)
        
    
        
    vals = _fix_var_array(ds,
                    var_key,
                    0,
                    decimate)
    
    u_vals = _fix_var_array(ds,
                    u_var_key,
                    0,
                    decimate)
    
    v_vals = _fix_var_array(ds,
                    v_var_key,
                    0,
                    decimate)

    stn = _mpplots.StationPlot(ax, vals['longitude'], vals['latitude'],
                                transform=datacrs, 
                                fontsize=pixel_query_value_fontsize, 
                                zorder=pixel_query_value_zorder, 
                                clip_on=True)

    if pixel_query_type != 'barbs':
        stn.plot_parameter('C', 
                            vals[var_key], 
                            color=pixel_query_value_fontcolor, 
                            path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                        foreground=pixel_query_value_foreground)], 
                            zorder=pixel_query_value_zorder)

    else:
        stn.plot_barb(u_vals[u_var_key], 
                        v_vals[v_var_key],
                        color=barb_color, 
                        length=barb_length, 
                        linewidth=barb_width,
                        zorder=barb_zorder)

    fig.savefig(f"{path}/{region.upper()}/{reference_system.upper()}/{filename}", bbox_inches='tight')
    _plt.close(fig)
    if notifications == 'on':
        print(f"{filename} saved to {path}/{region.upper()}")
        
        
def plot_temperature_and_wind(region='conus',
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=150,
                     start=-30,
                     stop=130,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER TEMPERATURE [°F] & 10-METER WIND [MPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=12,
                     secondary_title_fontsize=10,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=10,
                     colorbar_aspect=50,
                     colormap='jet',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['magenta',
                             'orchid',
                             'plum',
                             'darkviolet',
                             'darkslateblue',
                             'blue',
                             'cyan',
                             'lawngreen',
                             'greenyellow',
                             'olive',
                             'gold',
                             'goldenrod',
                             'darkorange',
                             'deeppink',
                             'crimson',
                             'darkred',
                             'grey'],
                     ds=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     temperature_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA/Temperature',
                     filename='RTMA Temperature and Wind.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     temperature_var_key='2m_temperature',
                     wind_speed_var_key='10m_wind_speed',
                     u_var_key='10m_u_wind_component',
                     v_var_key='10m_v_wind_component',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_to='mph',
                     barb_length=4,
                     barb_width=0.5,
                     barb_color='black',
                     barb_zorder=7):
    
    """
    This function plots the latest Real Time Mesoscale Analysis (RTMA) for temperature + wind.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Entire CONUS region.
            ii) 'jet' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Required Arguments: None
    
    Optional Arguments:
    
    1) region (String) - Default='conus'. The region of the plot. Use the 2-letter state abbreviation or 4-letter GACC abbreviation.
        If the user wants a completely custom region where they define their own lat/lon bounds, set region='custom'. 
        
    2) show_states (Boolean) - Default=True. When set to True, U.S. state borders are shown. 
    
    3) state_border_color (String) - Default='black'. The color of the U.S. state borders.
    
    4) state_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the U.S. state borders.
    
    5) state_border_zorder (Integer) - Default=3. The z-order of the state borders. For state borders to be displayed
        the following condition must be met: state_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
        
    6) show_counties (Boolean) - Default=True. When set to True, U.S. county borders are shown. 
    
    7) county_border_color (String) - Default='black'. The color of the U.S. county borders.
    
    8) county_border_linewidth (Float or Integer) - Default=0.25. The linewidth of the U.S. county borders.
    
    9) county_border_zorder (Integer) - Default=3. The z-order of the county borders. For county borders to be displayed
        the following condition must be met: county_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
    
    10) show_gacc_boundaries (Boolean) - Default=False. When set to True, Geographic Area Coordination Center borders are shown. 
    
    11) gacc_border_color (String) - Default='black'. The color of the Geographic Area Coordination Center borders.
    
    12) gacc_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the Geographic Area Coordination Center borders.
    
    13) gacc_border_zorder (Integer) - Default=3. The z-order of the Geographic Area Coordination Center borders. 
       For Geographic Area Coordination Center borders to be displayed the following condition must be met: gacc_border_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
       
    14) show_predictive_services_areas (Boolean) - Default=False. When set to True, Predictive Services Areas borders are shown. 
    
    15) predictive_services_areas_color (String) - Default='black'. The color of the Predictive Services Areas borders.
    
    16) predictive_services_areas_linewidth (Float or Integer) - Default=0.25. The linewidth of the Predictive Services Areas borders.
    
    17) predictive_services_areas_zorder (Integer) - Default=3. The z-order of the Predictive Services Areas borders. 
       For Predictive Services Areas borders to be displayed the following condition must be met: predictive_services_areas_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    18) show_nws_public_zones (Boolean) - Default=False. When set to True, NWS Public Zone borders are shown. 
    
    19) nws_public_zones_color (String) - Default='black'. The color of the NWS Public Zone borders.
    
    20) nws_public_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Public Zone borders.
    
    21) nws_public_zones_zorder (Integer) - Default=3. The z-order of the NWS Public Zone borders. 
       For NWS Public Zone borders to be displayed the following condition must be met: nws_public_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    22) show_nws_fire_weather_zones (Boolean) - Default=False. When set to True, NWS Fire Weather Zone borders are shown. 
    
    23) nws_fire_weather_zones_color (String) - Default='black'. The color of the NWS Fire Weather Zone borders.
    
    24) nws_fire_weather_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Fire Weather Zone borders.
    
    25) nws_fire_weather_zones_zorder (Integer) - Default=3. The z-order of the NWS Fire Weather Zone borders. 
       For NWS Fire Weather Zone borders to be displayed the following condition must be met: nws_fire_weather_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    26) show_nws_cwa (Boolean) - Default=False. When set to True, NWS CWA borders are shown.
    
    27) nws_cwa_color (String) - Default='black'. The color of the NWS CWA borders.
    
    28) nws_cwa_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS CWA borders.
    
    29) nws_cwa_zorder (Integer) - Default=3. The z-order of the NWS CWA borders. 
       For NWS CWA borders to be displayed the following condition must be met: nws_cwa_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    30) show_calfire_boundaries (Boolean) - Default=False. When set to True, CalFire borders are shown.
    
    31) calfire_boundary_color (String) - Default='black'. The color of the CalFire borders.
    
    32) calfire_boundary_linewidth (Float or Integer) - Default=0.25. The linewidth of the CalFire borders.
    
    33) calfire_boundary_zorder (Integer) - Default=3. The z-order of the CalFire borders. 
       For CalFire borders to be displayed the following condition must be met: calfire_boundary_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.

    34) custom_shapefile_url (String or None) - Default=None. If the user wishes to set up an automation importing geometry from a shapefile that
        is not in the base version of FireWxPy, this is how to do that. The user will pass the download URL as a string by setting
        custom_shapefile_url='https"//shapefile_download_url.file_extension'. 
        
    35) custom_shapefile_file_extension (String) - Default='.zip'. This is the file extension of the zipped shapefile folder on the web
        server. 
        
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    36) custom_shapefile_color (String) - Default='black'. The color of the borders in the custom shapefile.
    
    37) custom_shapefile_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders in the custom shapefile.
    
    38) custom_shapefile_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    39) custom_geojson_url (String) - Default=None. If the user wishes to set up an automation with a publicly available
        geojson on the web, pass in the full download URL into this argument.
    
    40) custom_geojson_filename (String) - Default=None. The filename of the custom geojson file. 
    
    41) custom_geojson_folder_name (String) Default='Custom GeoJSON'. The folder where the custom geojson will be saved in.
    
    42) custom_geojson_color (String) - Default='black'. The edge color of the geometries in the custom geojson file.
    
    43) custom_geojson_linewidth (Integer or Float) - Default=0.5. The linewidth of the borders in the custom geojson. 
    
    44) custom_geojson_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    45) custom_shapefile_local_path (String) - Default=None. The path to a shapefile locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    46) custom_shapefile_local_color (String) - Default='black'. The edge color of the geometries in the shapefile.
    
    47) custom_shapefile_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    48) custom_shapefile_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    49) custom_geojson_local_path (String) - Default=None. The path to a geojson locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    50) custom_geojson_local_color (String) - Default='black'. The edge color of the geometries in the geojson.
    
    51) custom_geojson_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    52) custom_geojson_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    53) convert_custom_shapefile_crs (Boolean)- Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom shapefile. 
        
    54) convert_local_custom_shapefile_crs (Boolean) - Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom geojson.
        
    55)  refresh_cartographic_files (Boolean) - Default=True. Users that have automated pipelines set up for shapefiles. Having this set to
        True allows the client to delete and re-download the shapefiles with each run of the script. This is useful for shapefiles
        that have frequent geometry updates.
        
    56) reference_system (String) - Default='States & Counties'. The name of the borders overlaid onto the map.
    
    57) show_rivers (Boolean) - Default=False. Set to True to display rivers. 
    
    58) rivers_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    59) rivers_color (String) - Default='lightcyan'. The color of the river. 
    
    60) figure_x_length (Integer) - Default=12. The length of the figure in the x-direction.
    
    61) figure_y_length (Integer) - Default=12. The length of the figure in the y-direction.
    
    62) coastline_linewidth (Float or Integer) - Default=0.75. The linewidth of the coastline.
    
    63) land_color (String) - Default='beige'. The color of the land on a map.
    
    64) ocean_color (String) - Default='lightcyan'. The color of the ocean on a map.
    
    65) lakes_color (String) - Default='lightcyan'. The color of lakes on a map. 

    66) costline_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    67) ocean_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    68) lakes_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    69) land_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    70) decimate (Integer) - Default=150. This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. When set to 50, every 50 values will be queried. Use
        larger numbers for larger areas and smaller values for smaller areas. The default of 50 represents the setting for
        CONUS. 
        
    71) start (Integer) - Default=-30. The start of the filled contour range.
    
    72) stop (Integer) - Default=130. The end of the filled contour range. 
    
    73) step (Integer) - Default=1. The interval of the filled contours.
    
    74) facecolor (String) - Default='aliceblue'. The background color of the graphic. 
    
    75) primary_title_text (String) - Default='RTMA 2-METER TEMPERATURE [°F] & 10-METER WIND [MPH]'. The primary title
        of the graphic. 
        
    76) primary_title_textbox_color (String) - Default='wheat'. The color of the textbox of the primary title.
    
    77) primary_title_textbox_style (String) - Default='round'. The style of the textbox of the primary title.
    
    78) primary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    79) secondary_title_textbox_color (Float or Integer) Default='wheat'. The color of the textbox of the secondary title.
        
    80) secondary_title_textbox_style (String) - Default='round'. The style of the textbox of the secondary title.
    
    81) secondary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    82) primary_title_fontsize (Integer) - Default=12. Fontsize of the primary title text.
    
    83) secondary_title_fontsize (Integer) Default=10. Fontsize of the secondary title text.
    
    84) local_time (Boolean) - Default=True. Set to False for UTC time.
    
    85) signature_textbox_color (String) - Default='wheat'. The color of the textbox of the graphic's signature.
    
    86) signature_textbox_style (String) - Default='round'. The style of the textbox of the graphic's signature.
    
    87) signature_textbox_alpha (Float or Integer) - Default=1. A value between 0.5 and 1 representing transparency.

    88) signature_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    89) signature_fontsize (Integer) - Default=8. Fontsize of the graphic's signature text.
    
    90) signature_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the signature text box.
    
    91) signature_textbox_y_position (Float) - Default=-0.175. The y-position with respect to the plot axis of the signature text box.
    
    92) signature_text_new_lines (Boolean) - Default=False. When set to True, each section in the signature is on a new line.
        It is recommended to set this to True on plots that are longer from North to South than West to East. 
        
    93) reference_system_textbox_color (String) - Default='wheat'. The color of the textbox of the reference system.
    
    94) reference_system_textbox_style (String) - Default='round'. The style of the textbox of the reference system.
    
    95) reference_system_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    96) reference_system_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    97) reference_system_fontsize (Integer) - Default=6. Fontsize of the reference system label text.
    
    98) reference_system_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the reference system text box.
    
    99) reference_system_textbox_y_position (Float) - Default=0. The y-position with respect to the plot axis of the reference system text box.

    100) colorbar_shrink (Float or Integer) - Default=1. Fraction by which to multiply the size of the colorbar.
    
    101) colorbar_pad (Float) - Default=0.01. Fraction of original Axes between colorbar and new image Axes.
    
    102) tick_label_fontsize (Integer) - Default=9. The fontsize of the colorbar tick labels.
    
    103) colorbar_location (String) - Default='bottom'. The side of the plot axis where the colorbar will be displayed.
    
    104) colorbar_interval (Integer) - Default=10. The interval of tick marks on the colorbar.
    
    105) colorbar_aspect (Integer) - Default=50. Ratio of long to short dimensions.
    
    106) colormap (String) - Default='jet'. The Matplotlib colormap for filled contours being used OR set to 'custom' to create your own 
        custom colormapping. See the optional colors argument documentation (109) for more information on how to pass
        in a custom array of colors. 
        
    107) contourf_alpha (Float or Integer) - Default=0.5. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    108) contourf_zorder (Integer) - Default=2. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    109) colors (String List) - Default=colors=['magenta',
                                                'orchid',
                                                'plum',
                                                'darkviolet',
                                                'darkslateblue',
                                                'blue',
                                                'cyan',
                                                'lawngreen',
                                                'greenyellow',
                                                'olive',
                                                'gold',
                                                'goldenrod',
                                                'darkorange',
                                                'deeppink',
                                                'crimson',
                                                'darkred',
                                                'grey']
                                        
            The array of colors being used when colormap='custom'. 
            
    110) ds (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds=ds. 
            
    111) western_bound (Float or Integer) - Default=-125. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    112) eastern_bound (Float or Integer) - Default=-65. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    113) southern_bound (Float or Integer) - Default=20. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    114) northern_bound (Float or Integer) - Default=50. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    115) pixel_query_value_fontsize (Integer) - Default=4. The fontsize of the pixel query values.
    
    116) pixel_query_value_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    117) pixel_query_value_foreground (String) - Default='white'. The color of the foreground on the station plot (pixel query value).
    
    118) pixel_query_value_fontcolor (String) - Default='black'. The font color of the pixel query values.
    
    119) pixel_query_stroke_linewidth (Float or Integer) - Default=1. The linewidth of the pixel query values text outline.
    
    120) path (String) - Default='FireWxPy Graphics/RTMA/Temperature'. The directory where the graphic will save.
    
    121) filename (String) - Default='RTMA Temperature and Wind.png'. The filename of the image.
    
    122) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    123) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
        
    124) clear_data (Boolean) - Default=True. When set to True, the data will be cleared with each run of the script.
        Set to False when downloading the data outside of the function and passing the data in. 
        
    125) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB data to a file.
    
    126) notifications (String) - Default='off'. Notifications throughout the process. 

    127) custom_data_directory (String or None) - Default=None. The directory path where the data will be saved to. 

    128) mapcrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the map.
    
    129) datacrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the data.

    130) temperature_var_key (String) - Default='2m_temperature'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    131) wind_speed_var_key (String) - Default='10m_wind_speed'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    132) u_var_key (String) - Default='10m_u_wind_component'. The variable key name of the u-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    133) v_var_key (String) - Default='10m_v_wind_component'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    134) wind_direction_var_key (String) - Default='10m_wind_direction'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    135) time_coord_key (String) - Default='time'. The time coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    136) longitude_key (String) - Default='longitude'. The longitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
    
    137) latitude_key (String) - Default='latitude'. The latitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    138) convert_wind_speed (Boolean) - Default=True. Convert wind speed from m/s to either mph or kts.
    
    139) convert_to (String) - Default='mph'. Set to 'kts' for knots.
    
    140) pixel_query_type (String) - Default='barbs'. Display either wind barbs or numerical values.
    
    141) barb_length (Float or Integer) - Default=2. Length of wind barb.
    
    142) barb_width (Float or Integer) - Default=0.25. Width of wind barb. 
    
    143) barb_color (String) - Default='black'. Color of wind barb. 
    
    144) barb_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.

    Returns
    -------
    
    An image of the RTMA Temperature + Wind Analysis specified to the user's needs saved to {path}    
    """
    
    _build_directory_branch(f"{path}/{region.upper()}/{reference_system.upper()}")
    
    _mpl.rcParams['xtick.labelsize'] = tick_label_fontsize
    _mpl.rcParams['ytick.labelsize'] = tick_label_fontsize
    
    primary_title_box = dict(boxstyle=primary_title_textbox_style, 
                            facecolor=primary_title_textbox_color, 
                            alpha=primary_title_textbox_alpha)
    
    secondary_title_box = dict(boxstyle=secondary_title_textbox_style, 
                            facecolor=secondary_title_textbox_color, 
                            alpha=secondary_title_textbox_alpha)
    
    signature_box = dict(boxstyle=signature_textbox_style, 
                            facecolor=signature_textbox_color, 
                            alpha=signature_textbox_alpha)
    
    reference_system_box = dict(boxstyle=reference_system_textbox_style, 
                            facecolor=reference_system_textbox_color, 
                            alpha=reference_system_textbox_alpha)
    
    levels = _np.arange(start, (stop + step), step)
    ticks = levels[::colorbar_interval]
    
    western_bound, eastern_bound, southern_bound, northern_bound = _bounding_box(region,
                                                                                 western_bound,
                                                                                 eastern_bound,
                                                                                 southern_bound,
                                                                                 northern_bound)
    
    if ds is None:
        ds = _rtma(proxies=proxies,
                   clear_recycle_bin=clear_recycle_bin,
                   clear_data=clear_data,
                   western_bound=western_bound,
                   eastern_bound=eastern_bound,
                   southern_bound=southern_bound,
                   northern_bound=northern_bound,
                   convert_temperature=True,
                   convert_to='fahrenheit',
                   chunk_size=chunk_size,
                   notifications=notifications,
                   custom_directory=custom_data_directory)
    else:
        ds = ds
        
    if convert_wind_speed == True:
        if convert_to == 'mph':
            ds[wind_speed_var_key] = _calc.mps_to_mph(ds[wind_speed_var_key])
            ds[u_var_key] = _calc.mps_to_mph(ds[u_var_key])
            ds[v_var_key] = _calc.mps_to_mph(ds[v_var_key])
        else:
            ds[wind_speed_var_key] = _calc.mph_to_kts(ds[wind_speed_var_key])
            ds[u_var_key] = _calc.mph_to_kts(ds[u_var_key])
            ds[v_var_key] = _calc.mph_to_kts(ds[v_var_key])
            
    else:
        pass
        
    if colormap == 'custom':
        cmap = _mcolors.LinearSegmentedColormap.from_list("wind gust", colors)
    else:
        cmap = colormap
    
    valid_time = _pd.to_datetime(ds[time_coord_key].to_pandas())
    valid_time = valid_time.tz_localize('UTC')
    time = valid_time.astimezone(_to_zone)
    time_utc = time.astimezone(_from_zone)
    
    fig = _plt.figure(figsize=(figure_x_length, figure_y_length))
    fig.set_facecolor(facecolor)
    
    ax = fig.add_subplot(1,1,1, projection=mapcrs)
    ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax.add_feature(_cfeature.COASTLINE.with_scale('50m'), linewidth=coastline_linewidth, zorder=costline_zorder)
    ax.add_feature(_cfeature.LAND, color=land_color, zorder=land_zorder)
    ax.add_feature(_cfeature.OCEAN, color=ocean_color, zorder=ocean_zorder)
    ax.add_feature(_cfeature.LAKES, color=lakes_color, zorder=lakes_zorder)
    if show_rivers is True:
        ax.add_feature(_cfeature.RIVERS, color=rivers_color, zorder=rivers_zorder)
    if show_states is True:
        states = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_States_Territories.zip",
                                            f"Cartographic Files/US States",
                                            f"US_States_Territories.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            state_border_color,
                                            datacrs)
        
        ax.add_geometries(states, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=state_border_color, 
                          linewidth=state_border_linewidth, 
                          zorder=state_border_zorder)
    
    if show_counties is True:
        counties = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_Counties.zip",
                                            f"Cartographic Files/US Counties",
                                            f"US_Counties.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            county_border_color,
                                            datacrs)
        
        ax.add_geometries(counties, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=county_border_color, 
                          linewidth=county_border_linewidth, 
                          zorder=county_border_zorder)
        
    if show_gacc_boundaries is True:
        gacc = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/GACC_Boundaries_2026.zip",
                                            f"Cartographic Files/GACC Boundaries",
                                            f"GACC_Boundaries_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            gacc_border_color,
                                            datacrs)
        
        ax.add_geometries(gacc, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=gacc_border_color, 
                          linewidth=gacc_border_linewidth, 
                          zorder=gacc_border_zorder)
    
    if show_predictive_services_areas is True:
        psa = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/PSA_Boundaries.zip",
                                            f"Cartographic Files/PSA Boundaries",
                                            f"PSA_Boundaries.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            predictive_services_areas_color,
                                            datacrs)
        
        ax.add_geometries(psa, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=predictive_services_areas_color, 
                          linewidth=predictive_services_areas_linewidth, 
                          zorder=predictive_services_areas_zorder)
        
    if show_nws_public_zones is True:
        pz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Public_Zones_2026.zip",
                                            f"Cartographic Files/NWS Public Zones",
                                            f"NWS_Public_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_public_zones_color,
                                            datacrs)
        
        ax.add_geometries(pz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_public_zones_color, 
                          linewidth=nws_public_zones_linewidth, 
                          zorder=nws_public_zones_zorder)
        
    if show_nws_fire_weather_zones is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Fire_Weather_Zones_2026.zip",
                                            f"Cartographic Files/NWS Fire Weather Zones",
                                            f"NWS_Fire_Weather_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_fire_weather_zones_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_fire_weather_zones_color, 
                          linewidth=nws_fire_weather_zones_linewidth, 
                          zorder=nws_fire_weather_zones_zorder)
        
    if show_nws_cwa is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_CWA_2026.zip",
                                            f"Cartographic Files/NWS CWAs",
                                            f"NWS_CWA_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_cwa_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_cwa_color, 
                          linewidth=nws_cwa_linewidth, 
                          zorder=nws_cwa_zorder)
        
    if show_calfire_boundaries is True:
        calfire = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/CALFIRE/CalFire_Administrative_Units.zip",
                                            f"Cartographic Files/CalFire",
                                            f"CalFire_Administrative_Units.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            calfire_boundary_color,
                                            datacrs,
                                            convert_crs=True,
                                            convert_to='EPSG:4326')
        
        ax.add_geometries(calfire, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=calfire_boundary_color, 
                          linewidth=calfire_boundary_linewidth, 
                          zorder=calfire_boundary_zorder)
        
    if custom_shapefile_url is not None:
        
        fname = _get_filename_from_url(custom_shapefile_url)
        
        custom_shape = _import_shapefile_from_web(custom_shapefile_url,
                                            f"Cartographic Files/{custom_shapefile_folder_name}",
                                            fname,
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            custom_shapefile_file_extension,
                                            custom_shapefile_color,
                                            convert_crs=convert_custom_shapefile_crs)
        
        ax.add_geometries(custom_shape, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_color, 
                          linewidth=custom_shapefile_linewidth, 
                          zorder=custom_shapefile_zorder)
        
    if custom_geojson_url is not None:
        
        custom_json = _import_geojson_from_web(custom_geojson_url,
                                                f"Cartographic Files/{custom_geojson_folder_name}", 
                                                custom_geojson_filename, 
                                                proxies, 
                                                chunk_size,
                                                notifications, 
                                                refresh_cartographic_files)
        
        ax.add_geometries(custom_json, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_color, 
                          linewidth=custom_geojson_linewidth, 
                          zorder=custom_geojson_zorder)
        
    if custom_shapefile_local_path is not None:
        custom_local_shapefile = _import_shapefile_local(custom_shapefile_local_path,
                                                            custom_shapefile_local_color,
                                                            convert_crs=convert_local_custom_shapefile_crs)
        
        ax.add_geometries(custom_local_shapefile, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_local_color, 
                          linewidth=custom_shapefile_local_linewidth, 
                          zorder=custom_shapefile_local_zorder)
        
    if custom_geojson_local_path is not None:
        custom_local_geojson = _import_geojson_local(custom_geojson_local_path)
        
        ax.add_geometries(custom_local_geojson, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_local_color, 
                          linewidth=custom_geojson_local_linewidth, 
                          zorder=custom_geojson_local_zorder)
    
    cs = ax.contourf(ds[longitude_key],
                ds[latitude_key],
                ds[temperature_var_key],
                cmap=cmap,
                levels=levels,
                transform=datacrs,
                alpha=contourf_alpha,
                zorder=contourf_zorder,
                extend='both')
    
    fig.colorbar(cs, 
                shrink=colorbar_shrink, 
                pad=colorbar_pad, 
                location=colorbar_location,
                ticks=ticks,
                aspect=colorbar_aspect)
    
    _plt.title(f"{primary_title_text}", 
               fontsize=primary_title_fontsize, 
               fontweight='bold',
               bbox=primary_title_box,
               loc='left')
    
    if local_time is True:
        _plt.title(f"Valid: {time.strftime('%m/%d/%Y %H:00')} {_timezone}", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
    else:
        _plt.title(f"Valid: {time_utc.strftime('%m/%d/%Y %H:00')} UTC", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
        
    if signature_text_new_lines is False:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')} | Data Source: NCEP/NOMADS | Created: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    else:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')}\nData Source: NCEP/NOMADS\nCreated: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    
    ax.text(reference_system_textbox_x_position, 
            reference_system_textbox_y_position,
            f"Reference System: {reference_system}",
            fontsize=reference_system_fontsize,
            fontweight='bold',
            bbox=reference_system_box,
            transform=ax.transAxes,
            zorder=reference_system_textbox_zorder)
        
    
        
    temp_vals = _fix_var_array(ds,
                    temperature_var_key,
                    0,
                    decimate)
    
    u_vals = _fix_var_array(ds,
                    u_var_key,
                    0,
                    decimate)
    
    v_vals = _fix_var_array(ds,
                    v_var_key,
                    0,
                    decimate)
    
    ws_vals = _fix_var_array(ds,
                    wind_speed_var_key,
                    0,
                    decimate)

    stn = _mpplots.StationPlot(ax, temp_vals['longitude'], temp_vals['latitude'],
                                transform=datacrs, 
                                fontsize=pixel_query_value_fontsize, 
                                zorder=pixel_query_value_zorder, 
                                clip_on=True)


    stn.plot_parameter('NW', 
                       temp_vals[temperature_var_key], 
                       color=temperature_pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)
    
    stn.plot_parameter('NE', 
                       ws_vals[wind_speed_var_key], 
                       color= wind_speed_pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)

    stn.plot_barb(u_vals[u_var_key], 
                    v_vals[v_var_key],
                    color=barb_color, 
                    length=barb_length, 
                    linewidth=barb_width,
                    zorder=barb_zorder)

    fig.savefig(f"{path}/{region.upper()}/{reference_system.upper()}/{filename}", bbox_inches='tight')
    _plt.close(fig)
    if notifications == 'on':
        print(f"{filename} saved to {path}/{region.upper()}")
        
        
def plot_temperature_and_gust(region='conus',
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=150,
                     start=-30,
                     stop=130,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER TEMPERATURE [°F] & 10-METER GUST [MPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=12,
                     secondary_title_fontsize=10,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=10,
                     colorbar_aspect=50,
                     colormap='jet',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['magenta',
                             'orchid',
                             'plum',
                             'darkviolet',
                             'darkslateblue',
                             'blue',
                             'cyan',
                             'lawngreen',
                             'greenyellow',
                             'olive',
                             'gold',
                             'goldenrod',
                             'darkorange',
                             'deeppink',
                             'crimson',
                             'darkred',
                             'grey'],
                     ds=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     temperature_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA/Temperature',
                     filename='RTMA Temperature and Gust.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     temperature_var_key='2m_temperature',
                     wind_gust_var_key='10m_wind_gust',
                     u_var_key='10m_u_wind_component',
                     v_var_key='10m_v_wind_component',
                     wind_direction_var_key='10m_wind_direction',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_to='mph',
                     barb_length=4,
                     barb_width=0.5,
                     barb_color='black',
                     barb_zorder=7):
    
    """
    This function plots the latest Real Time Mesoscale Analysis (RTMA) for temperature + gust.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Entire CONUS region.
            ii) 'jet' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Required Arguments: None
    
    Optional Arguments:
    
    1) region (String) - Default='conus'. The region of the plot. Use the 2-letter state abbreviation or 4-letter GACC abbreviation.
        If the user wants a completely custom region where they define their own lat/lon bounds, set region='custom'. 
        
    2) show_states (Boolean) - Default=True. When set to True, U.S. state borders are shown. 
    
    3) state_border_color (String) - Default='black'. The color of the U.S. state borders.
    
    4) state_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the U.S. state borders.
    
    5) state_border_zorder (Integer) - Default=3. The z-order of the state borders. For state borders to be displayed
        the following condition must be met: state_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
        
    6) show_counties (Boolean) - Default=True. When set to True, U.S. county borders are shown. 
    
    7) county_border_color (String) - Default='black'. The color of the U.S. county borders.
    
    8) county_border_linewidth (Float or Integer) - Default=0.25. The linewidth of the U.S. county borders.
    
    9) county_border_zorder (Integer) - Default=3. The z-order of the county borders. For county borders to be displayed
        the following condition must be met: county_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
    
    10) show_gacc_boundaries (Boolean) - Default=False. When set to True, Geographic Area Coordination Center borders are shown. 
    
    11) gacc_border_color (String) - Default='black'. The color of the Geographic Area Coordination Center borders.
    
    12) gacc_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the Geographic Area Coordination Center borders.
    
    13) gacc_border_zorder (Integer) - Default=3. The z-order of the Geographic Area Coordination Center borders. 
       For Geographic Area Coordination Center borders to be displayed the following condition must be met: gacc_border_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
       
    14) show_predictive_services_areas (Boolean) - Default=False. When set to True, Predictive Services Areas borders are shown. 
    
    15) predictive_services_areas_color (String) - Default='black'. The color of the Predictive Services Areas borders.
    
    16) predictive_services_areas_linewidth (Float or Integer) - Default=0.25. The linewidth of the Predictive Services Areas borders.
    
    17) predictive_services_areas_zorder (Integer) - Default=3. The z-order of the Predictive Services Areas borders. 
       For Predictive Services Areas borders to be displayed the following condition must be met: predictive_services_areas_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    18) show_nws_public_zones (Boolean) - Default=False. When set to True, NWS Public Zone borders are shown. 
    
    19) nws_public_zones_color (String) - Default='black'. The color of the NWS Public Zone borders.
    
    20) nws_public_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Public Zone borders.
    
    21) nws_public_zones_zorder (Integer) - Default=3. The z-order of the NWS Public Zone borders. 
       For NWS Public Zone borders to be displayed the following condition must be met: nws_public_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    22) show_nws_fire_weather_zones (Boolean) - Default=False. When set to True, NWS Fire Weather Zone borders are shown. 
    
    23) nws_fire_weather_zones_color (String) - Default='black'. The color of the NWS Fire Weather Zone borders.
    
    24) nws_fire_weather_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Fire Weather Zone borders.
    
    25) nws_fire_weather_zones_zorder (Integer) - Default=3. The z-order of the NWS Fire Weather Zone borders. 
       For NWS Fire Weather Zone borders to be displayed the following condition must be met: nws_fire_weather_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    26) show_nws_cwa (Boolean) - Default=False. When set to True, NWS CWA borders are shown.
    
    27) nws_cwa_color (String) - Default='black'. The color of the NWS CWA borders.
    
    28) nws_cwa_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS CWA borders.
    
    29) nws_cwa_zorder (Integer) - Default=3. The z-order of the NWS CWA borders. 
       For NWS CWA borders to be displayed the following condition must be met: nws_cwa_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    30) show_calfire_boundaries (Boolean) - Default=False. When set to True, CalFire borders are shown.
    
    31) calfire_boundary_color (String) - Default='black'. The color of the CalFire borders.
    
    32) calfire_boundary_linewidth (Float or Integer) - Default=0.25. The linewidth of the CalFire borders.
    
    33) calfire_boundary_zorder (Integer) - Default=3. The z-order of the CalFire borders. 
       For CalFire borders to be displayed the following condition must be met: calfire_boundary_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.

    34) custom_shapefile_url (String or None) - Default=None. If the user wishes to set up an automation importing geometry from a shapefile that
        is not in the base version of FireWxPy, this is how to do that. The user will pass the download URL as a string by setting
        custom_shapefile_url='https"//shapefile_download_url.file_extension'. 
        
    35) custom_shapefile_file_extension (String) - Default='.zip'. This is the file extension of the zipped shapefile folder on the web
        server. 
        
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    36) custom_shapefile_color (String) - Default='black'. The color of the borders in the custom shapefile.
    
    37) custom_shapefile_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders in the custom shapefile.
    
    38) custom_shapefile_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    39) custom_geojson_url (String) - Default=None. If the user wishes to set up an automation with a publicly available
        geojson on the web, pass in the full download URL into this argument.
    
    40) custom_geojson_filename (String) - Default=None. The filename of the custom geojson file. 
    
    41) custom_geojson_folder_name (String) Default='Custom GeoJSON'. The folder where the custom geojson will be saved in.
    
    42) custom_geojson_color (String) - Default='black'. The edge color of the geometries in the custom geojson file.
    
    43) custom_geojson_linewidth (Integer or Float) - Default=0.5. The linewidth of the borders in the custom geojson. 
    
    44) custom_geojson_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    45) custom_shapefile_local_path (String) - Default=None. The path to a shapefile locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    46) custom_shapefile_local_color (String) - Default='black'. The edge color of the geometries in the shapefile.
    
    47) custom_shapefile_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    48) custom_shapefile_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    49) custom_geojson_local_path (String) - Default=None. The path to a geojson locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    50) custom_geojson_local_color (String) - Default='black'. The edge color of the geometries in the geojson.
    
    51) custom_geojson_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    52) custom_geojson_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    53) convert_custom_shapefile_crs (Boolean)- Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom shapefile. 
        
    54) convert_local_custom_shapefile_crs (Boolean) - Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom geojson.
        
    55)  refresh_cartographic_files (Boolean) - Default=True. Users that have automated pipelines set up for shapefiles. Having this set to
        True allows the client to delete and re-download the shapefiles with each run of the script. This is useful for shapefiles
        that have frequent geometry updates.
        
    56) reference_system (String) - Default='States & Counties'. The name of the borders overlaid onto the map.
    
    57) show_rivers (Boolean) - Default=False. Set to True to display rivers. 
    
    58) rivers_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    59) rivers_color (String) - Default='lightcyan'. The color of the river. 
    
    60) figure_x_length (Integer) - Default=12. The length of the figure in the x-direction.
    
    61) figure_y_length (Integer) - Default=12. The length of the figure in the y-direction.
    
    62) coastline_linewidth (Float or Integer) - Default=0.75. The linewidth of the coastline.
    
    63) land_color (String) - Default='beige'. The color of the land on a map.
    
    64) ocean_color (String) - Default='lightcyan'. The color of the ocean on a map.
    
    65) lakes_color (String) - Default='lightcyan'. The color of lakes on a map. 

    66) costline_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    67) ocean_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    68) lakes_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    69) land_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    70) decimate (Integer) - Default=150. This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. When set to 50, every 50 values will be queried. Use
        larger numbers for larger areas and smaller values for smaller areas. The default of 50 represents the setting for
        CONUS. 
        
    71) start (Integer) - Default=-30. The start of the filled contour range.
    
    72) stop (Integer) - Default=130. The end of the filled contour range. 
    
    73) step (Integer) - Default=1. The interval of the filled contours.
    
    74) facecolor (String) - Default='aliceblue'. The background color of the graphic. 
    
    75) primary_title_text (String) - Default='RTMA 2-METER TEMPERATURE [°F] & 10-METER GUST [MPH]'. The primary title
        of the graphic. 
        
    76) primary_title_textbox_color (String) - Default='wheat'. The color of the textbox of the primary title.
    
    77) primary_title_textbox_style (String) - Default='round'. The style of the textbox of the primary title.
    
    78) primary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    79) secondary_title_textbox_color (Float or Integer) Default='wheat'. The color of the textbox of the secondary title.
        
    80) secondary_title_textbox_style (String) - Default='round'. The style of the textbox of the secondary title.
    
    81) secondary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    82) primary_title_fontsize (Integer) - Default=12. Fontsize of the primary title text.
    
    83) secondary_title_fontsize (Integer) Default=10. Fontsize of the secondary title text.
    
    84) local_time (Boolean) - Default=True. Set to False for UTC time.
    
    85) signature_textbox_color (String) - Default='wheat'. The color of the textbox of the graphic's signature.
    
    86) signature_textbox_style (String) - Default='round'. The style of the textbox of the graphic's signature.
    
    87) signature_textbox_alpha (Float or Integer) - Default=1. A value between 0.5 and 1 representing transparency.

    88) signature_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    89) signature_fontsize (Integer) - Default=8. Fontsize of the graphic's signature text.
    
    90) signature_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the signature text box.
    
    91) signature_textbox_y_position (Float) - Default=-0.175. The y-position with respect to the plot axis of the signature text box.
    
    92) signature_text_new_lines (Boolean) - Default=False. When set to True, each section in the signature is on a new line.
        It is recommended to set this to True on plots that are longer from North to South than West to East. 
        
    93) reference_system_textbox_color (String) - Default='wheat'. The color of the textbox of the reference system.
    
    94) reference_system_textbox_style (String) - Default='round'. The style of the textbox of the reference system.
    
    95) reference_system_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    96) reference_system_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    97) reference_system_fontsize (Integer) - Default=6. Fontsize of the reference system label text.
    
    98) reference_system_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the reference system text box.
    
    99) reference_system_textbox_y_position (Float) - Default=0. The y-position with respect to the plot axis of the reference system text box.

    100) colorbar_shrink (Float or Integer) - Default=1. Fraction by which to multiply the size of the colorbar.
    
    101) colorbar_pad (Float) - Default=0.01. Fraction of original Axes between colorbar and new image Axes.
    
    102) tick_label_fontsize (Integer) - Default=9. The fontsize of the colorbar tick labels.
    
    103) colorbar_location (String) - Default='bottom'. The side of the plot axis where the colorbar will be displayed.
    
    104) colorbar_interval (Integer) - Default=10. The interval of tick marks on the colorbar.
    
    105) colorbar_aspect (Integer) - Default=50. Ratio of long to short dimensions.
    
    106) colormap (String) - Default='jet'. The Matplotlib colormap for filled contours being used OR set to 'custom' to create your own 
        custom colormapping. See the optional colors argument documentation (109) for more information on how to pass
        in a custom array of colors. 
        
    107) contourf_alpha (Float or Integer) - Default=0.5. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    108) contourf_zorder (Integer) - Default=2. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    109) colors (String List) - Default=colors=['magenta',
                                                'orchid',
                                                'plum',
                                                'darkviolet',
                                                'darkslateblue',
                                                'blue',
                                                'cyan',
                                                'lawngreen',
                                                'greenyellow',
                                                'olive',
                                                'gold',
                                                'goldenrod',
                                                'darkorange',
                                                'deeppink',
                                                'crimson',
                                                'darkred',
                                                'grey']
                                        
            The array of colors being used when colormap='custom'. 
            
    110) ds (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds=ds. 
            
    111) western_bound (Float or Integer) - Default=-125. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    112) eastern_bound (Float or Integer) - Default=-65. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    113) southern_bound (Float or Integer) - Default=20. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    114) northern_bound (Float or Integer) - Default=50. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    115) pixel_query_value_fontsize (Integer) - Default=4. The fontsize of the pixel query values.
    
    116) pixel_query_value_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    117) pixel_query_value_foreground (String) - Default='white'. The color of the foreground on the station plot (pixel query value).
    
    118) pixel_query_value_fontcolor (String) - Default='black'. The font color of the pixel query values.
    
    119) pixel_query_stroke_linewidth (Float or Integer) - Default=1. The linewidth of the pixel query values text outline.
    
    120) path (String) - Default='FireWxPy Graphics/RTMA/Temperature'. The directory where the graphic will save.
    
    121) filename (String) - Default='RTMA Temperature and Gust.png'. The filename of the image.
    
    122) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    123) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
        
    124) clear_data (Boolean) - Default=True. When set to True, the data will be cleared with each run of the script.
        Set to False when downloading the data outside of the function and passing the data in. 
        
    125) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB data to a file.
    
    126) notifications (String) - Default='off'. Notifications throughout the process. 

    127) custom_data_directory (String or None) - Default=None. The directory path where the data will be saved to. 

    128) mapcrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the map.
    
    129) datacrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the data.

    130) temperature_var_key (String) - Default='2m_temperature'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    131) wind_gust_var_key (String) - Default='10m_wind_gust'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    132) u_var_key (String) - Default='10m_u_wind_component'. The variable key name of the u-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    133) v_var_key (String) - Default='10m_v_wind_component'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    134) wind_direction_var_key (String) - Default='10m_wind_direction'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    135) time_coord_key (String) - Default='time'. The time coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    136) longitude_key (String) - Default='longitude'. The longitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
    
    137) latitude_key (String) - Default='latitude'. The latitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    138) convert_wind_speed (Boolean) - Default=True. Convert wind speed from m/s to either mph or kts.
    
    139) convert_to (String) - Default='mph'. Set to 'kts' for knots.
    
    140) pixel_query_type (String) - Default='barbs'. Display either wind barbs or numerical values.
    
    141) barb_length (Float or Integer) - Default=2. Length of wind barb.
    
    142) barb_width (Float or Integer) - Default=0.25. Width of wind barb. 
    
    143) barb_color (String) - Default='black'. Color of wind barb. 
    
    144) barb_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.

    Returns
    -------
    
    An image of the RTMA Temperature + Gust Analysis specified to the user's needs saved to {path}    
    """
    
    _build_directory_branch(f"{path}/{region.upper()}/{reference_system.upper()}")
    
    _mpl.rcParams['xtick.labelsize'] = tick_label_fontsize
    _mpl.rcParams['ytick.labelsize'] = tick_label_fontsize
    
    primary_title_box = dict(boxstyle=primary_title_textbox_style, 
                            facecolor=primary_title_textbox_color, 
                            alpha=primary_title_textbox_alpha)
    
    secondary_title_box = dict(boxstyle=secondary_title_textbox_style, 
                            facecolor=secondary_title_textbox_color, 
                            alpha=secondary_title_textbox_alpha)
    
    signature_box = dict(boxstyle=signature_textbox_style, 
                            facecolor=signature_textbox_color, 
                            alpha=signature_textbox_alpha)
    
    reference_system_box = dict(boxstyle=reference_system_textbox_style, 
                            facecolor=reference_system_textbox_color, 
                            alpha=reference_system_textbox_alpha)
    
    levels = _np.arange(start, (stop + step), step)
    ticks = levels[::colorbar_interval]
    
    western_bound, eastern_bound, southern_bound, northern_bound = _bounding_box(region,
                                                                                 western_bound,
                                                                                 eastern_bound,
                                                                                 southern_bound,
                                                                                 northern_bound)
    
    if ds is None:
        ds = _rtma(proxies=proxies,
                   clear_recycle_bin=clear_recycle_bin,
                   clear_data=clear_data,
                   western_bound=western_bound,
                   eastern_bound=eastern_bound,
                   southern_bound=southern_bound,
                   northern_bound=northern_bound,
                   convert_temperature=True,
                   convert_to='fahrenheit',
                   chunk_size=chunk_size,
                   notifications=notifications,
                   custom_directory=custom_data_directory)
    else:
        ds = ds
        
    if convert_wind_speed == True:
        if convert_to == 'mph':
            ds[wind_gust_var_key] = _calc.mps_to_mph(ds[wind_gust_var_key])
            ds[u_var_key] = _calc.mps_to_mph(ds[u_var_key])
            ds[v_var_key] = _calc.mps_to_mph(ds[v_var_key])
        else:
            ds[wind_gust_var_key] = _calc.mph_to_kts(ds[wind_gust_var_key])
            ds[u_var_key] = _calc.mph_to_kts(ds[u_var_key])
            ds[v_var_key] = _calc.mph_to_kts(ds[v_var_key])
            
    else:
        pass
    
    ds = _calc.u_v_components(ds,
                            u_var_key,
                            v_var_key,
                            wind_direction_var_key,
                            wind_gust_var_key)
        
    if colormap == 'custom':
        cmap = _mcolors.LinearSegmentedColormap.from_list("wind gust", colors)
    else:
        cmap = colormap
    
    valid_time = _pd.to_datetime(ds[time_coord_key].to_pandas())
    valid_time = valid_time.tz_localize('UTC')
    time = valid_time.astimezone(_to_zone)
    time_utc = time.astimezone(_from_zone)
    
    fig = _plt.figure(figsize=(figure_x_length, figure_y_length))
    fig.set_facecolor(facecolor)
    
    ax = fig.add_subplot(1,1,1, projection=mapcrs)
    ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax.add_feature(_cfeature.COASTLINE.with_scale('50m'), linewidth=coastline_linewidth, zorder=costline_zorder)
    ax.add_feature(_cfeature.LAND, color=land_color, zorder=land_zorder)
    ax.add_feature(_cfeature.OCEAN, color=ocean_color, zorder=ocean_zorder)
    ax.add_feature(_cfeature.LAKES, color=lakes_color, zorder=lakes_zorder)
    if show_rivers is True:
        ax.add_feature(_cfeature.RIVERS, color=rivers_color, zorder=rivers_zorder)
    if show_states is True:
        states = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_States_Territories.zip",
                                            f"Cartographic Files/US States",
                                            f"US_States_Territories.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            state_border_color,
                                            datacrs)
        
        ax.add_geometries(states, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=state_border_color, 
                          linewidth=state_border_linewidth, 
                          zorder=state_border_zorder)
    
    if show_counties is True:
        counties = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_Counties.zip",
                                            f"Cartographic Files/US Counties",
                                            f"US_Counties.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            county_border_color,
                                            datacrs)
        
        ax.add_geometries(counties, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=county_border_color, 
                          linewidth=county_border_linewidth, 
                          zorder=county_border_zorder)
        
    if show_gacc_boundaries is True:
        gacc = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/GACC_Boundaries_2026.zip",
                                            f"Cartographic Files/GACC Boundaries",
                                            f"GACC_Boundaries_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            gacc_border_color,
                                            datacrs)
        
        ax.add_geometries(gacc, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=gacc_border_color, 
                          linewidth=gacc_border_linewidth, 
                          zorder=gacc_border_zorder)
    
    if show_predictive_services_areas is True:
        psa = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/PSA_Boundaries.zip",
                                            f"Cartographic Files/PSA Boundaries",
                                            f"PSA_Boundaries.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            predictive_services_areas_color,
                                            datacrs)
        
        ax.add_geometries(psa, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=predictive_services_areas_color, 
                          linewidth=predictive_services_areas_linewidth, 
                          zorder=predictive_services_areas_zorder)
        
    if show_nws_public_zones is True:
        pz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Public_Zones_2026.zip",
                                            f"Cartographic Files/NWS Public Zones",
                                            f"NWS_Public_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_public_zones_color,
                                            datacrs)
        
        ax.add_geometries(pz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_public_zones_color, 
                          linewidth=nws_public_zones_linewidth, 
                          zorder=nws_public_zones_zorder)
        
    if show_nws_fire_weather_zones is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Fire_Weather_Zones_2026.zip",
                                            f"Cartographic Files/NWS Fire Weather Zones",
                                            f"NWS_Fire_Weather_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_fire_weather_zones_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_fire_weather_zones_color, 
                          linewidth=nws_fire_weather_zones_linewidth, 
                          zorder=nws_fire_weather_zones_zorder)
        
    if show_nws_cwa is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_CWA_2026.zip",
                                            f"Cartographic Files/NWS CWAs",
                                            f"NWS_CWA_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_cwa_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_cwa_color, 
                          linewidth=nws_cwa_linewidth, 
                          zorder=nws_cwa_zorder)
        
    if show_calfire_boundaries is True:
        calfire = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/CALFIRE/CalFire_Administrative_Units.zip",
                                            f"Cartographic Files/CalFire",
                                            f"CalFire_Administrative_Units.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            calfire_boundary_color,
                                            datacrs,
                                            convert_crs=True,
                                            convert_to='EPSG:4326')
        
        ax.add_geometries(calfire, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=calfire_boundary_color, 
                          linewidth=calfire_boundary_linewidth, 
                          zorder=calfire_boundary_zorder)
        
    if custom_shapefile_url is not None:
        
        fname = _get_filename_from_url(custom_shapefile_url)
        
        custom_shape = _import_shapefile_from_web(custom_shapefile_url,
                                            f"Cartographic Files/{custom_shapefile_folder_name}",
                                            fname,
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            custom_shapefile_file_extension,
                                            custom_shapefile_color,
                                            convert_crs=convert_custom_shapefile_crs)
        
        ax.add_geometries(custom_shape, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_color, 
                          linewidth=custom_shapefile_linewidth, 
                          zorder=custom_shapefile_zorder)
        
    if custom_geojson_url is not None:
        
        custom_json = _import_geojson_from_web(custom_geojson_url,
                                                f"Cartographic Files/{custom_geojson_folder_name}", 
                                                custom_geojson_filename, 
                                                proxies, 
                                                chunk_size,
                                                notifications, 
                                                refresh_cartographic_files)
        
        ax.add_geometries(custom_json, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_color, 
                          linewidth=custom_geojson_linewidth, 
                          zorder=custom_geojson_zorder)
        
    if custom_shapefile_local_path is not None:
        custom_local_shapefile = _import_shapefile_local(custom_shapefile_local_path,
                                                            custom_shapefile_local_color,
                                                            convert_crs=convert_local_custom_shapefile_crs)
        
        ax.add_geometries(custom_local_shapefile, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_local_color, 
                          linewidth=custom_shapefile_local_linewidth, 
                          zorder=custom_shapefile_local_zorder)
        
    if custom_geojson_local_path is not None:
        custom_local_geojson = _import_geojson_local(custom_geojson_local_path)
        
        ax.add_geometries(custom_local_geojson, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_local_color, 
                          linewidth=custom_geojson_local_linewidth, 
                          zorder=custom_geojson_local_zorder)
    
    cs = ax.contourf(ds[longitude_key],
                ds[latitude_key],
                ds[temperature_var_key],
                cmap=cmap,
                levels=levels,
                transform=datacrs,
                alpha=contourf_alpha,
                zorder=contourf_zorder,
                extend='both')
    
    fig.colorbar(cs, 
                shrink=colorbar_shrink, 
                pad=colorbar_pad, 
                location=colorbar_location,
                ticks=ticks,
                aspect=colorbar_aspect)
    
    _plt.title(f"{primary_title_text}", 
               fontsize=primary_title_fontsize, 
               fontweight='bold',
               bbox=primary_title_box,
               loc='left')
    
    if local_time is True:
        _plt.title(f"Valid: {time.strftime('%m/%d/%Y %H:00')} {_timezone}", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
    else:
        _plt.title(f"Valid: {time_utc.strftime('%m/%d/%Y %H:00')} UTC", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
        
    if signature_text_new_lines is False:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')} | Data Source: NCEP/NOMADS | Created: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    else:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')}\nData Source: NCEP/NOMADS\nCreated: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    
    ax.text(reference_system_textbox_x_position, 
            reference_system_textbox_y_position,
            f"Reference System: {reference_system}",
            fontsize=reference_system_fontsize,
            fontweight='bold',
            bbox=reference_system_box,
            transform=ax.transAxes,
            zorder=reference_system_textbox_zorder)
        
    
        
    temp_vals = _fix_var_array(ds,
                    temperature_var_key,
                    0,
                    decimate)
    
    u_vals = _fix_var_array(ds,
                    u_var_key,
                    0,
                    decimate)
    
    v_vals = _fix_var_array(ds,
                    v_var_key,
                    0,
                    decimate)
    
    wg_vals = _fix_var_array(ds,
                    wind_gust_var_key,
                    0,
                    decimate)

    stn = _mpplots.StationPlot(ax, temp_vals['longitude'], temp_vals['latitude'],
                                transform=datacrs, 
                                fontsize=pixel_query_value_fontsize, 
                                zorder=pixel_query_value_zorder, 
                                clip_on=True)


    stn.plot_parameter('NW', 
                       temp_vals[temperature_var_key], 
                       color=temperature_pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)
    
    stn.plot_parameter('NE', 
                       wg_vals[wind_gust_var_key], 
                       color= wind_speed_pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)

    stn.plot_barb(u_vals[u_var_key], 
                    v_vals[v_var_key],
                    color=barb_color, 
                    length=barb_length, 
                    linewidth=barb_width,
                    zorder=barb_zorder)

    fig.savefig(f"{path}/{region.upper()}/{reference_system.upper()}/{filename}", bbox_inches='tight')
    _plt.close(fig)
    if notifications == 'on':
        print(f"{filename} saved to {path}/{region.upper()}")
        
def plot_relative_humidity_and_wind(region='conus',
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=150,
                     start=-30,
                     stop=130,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER relative_humidity [°F] & 10-METER WIND [MPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=12,
                     secondary_title_fontsize=10,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=10,
                     colorbar_aspect=50,
                     colormap='jet',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['magenta',
                             'orchid',
                             'plum',
                             'darkviolet',
                             'darkslateblue',
                             'blue',
                             'cyan',
                             'lawngreen',
                             'greenyellow',
                             'olive',
                             'gold',
                             'goldenrod',
                             'darkorange',
                             'deeppink',
                             'crimson',
                             'darkred',
                             'grey'],
                     ds=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     relative_humidity_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA/relative_humidity',
                     filename='RTMA relative_humidity and Wind.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     relative_humidity_var_key='2m_relative_humidity',
                     wind_speed_var_key='10m_wind_speed',
                     u_var_key='10m_u_wind_component',
                     v_var_key='10m_v_wind_component',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_to='mph',
                     barb_length=4,
                     barb_width=0.5,
                     barb_color='black',
                     barb_zorder=7):
    
    """
    This function plots the latest Real Time Mesoscale Analysis (RTMA) for relative_humidity + wind.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Entire CONUS region.
            ii) 'jet' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Required Arguments: None
    
    Optional Arguments:
    
    1) region (String) - Default='conus'. The region of the plot. Use the 2-letter state abbreviation or 4-letter GACC abbreviation.
        If the user wants a completely custom region where they define their own lat/lon bounds, set region='custom'. 
        
    2) show_states (Boolean) - Default=True. When set to True, U.S. state borders are shown. 
    
    3) state_border_color (String) - Default='black'. The color of the U.S. state borders.
    
    4) state_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the U.S. state borders.
    
    5) state_border_zorder (Integer) - Default=3. The z-order of the state borders. For state borders to be displayed
        the following condition must be met: state_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
        
    6) show_counties (Boolean) - Default=True. When set to True, U.S. county borders are shown. 
    
    7) county_border_color (String) - Default='black'. The color of the U.S. county borders.
    
    8) county_border_linewidth (Float or Integer) - Default=0.25. The linewidth of the U.S. county borders.
    
    9) county_border_zorder (Integer) - Default=3. The z-order of the county borders. For county borders to be displayed
        the following condition must be met: county_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
    
    10) show_gacc_boundaries (Boolean) - Default=False. When set to True, Geographic Area Coordination Center borders are shown. 
    
    11) gacc_border_color (String) - Default='black'. The color of the Geographic Area Coordination Center borders.
    
    12) gacc_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the Geographic Area Coordination Center borders.
    
    13) gacc_border_zorder (Integer) - Default=3. The z-order of the Geographic Area Coordination Center borders. 
       For Geographic Area Coordination Center borders to be displayed the following condition must be met: gacc_border_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
       
    14) show_predictive_services_areas (Boolean) - Default=False. When set to True, Predictive Services Areas borders are shown. 
    
    15) predictive_services_areas_color (String) - Default='black'. The color of the Predictive Services Areas borders.
    
    16) predictive_services_areas_linewidth (Float or Integer) - Default=0.25. The linewidth of the Predictive Services Areas borders.
    
    17) predictive_services_areas_zorder (Integer) - Default=3. The z-order of the Predictive Services Areas borders. 
       For Predictive Services Areas borders to be displayed the following condition must be met: predictive_services_areas_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    18) show_nws_public_zones (Boolean) - Default=False. When set to True, NWS Public Zone borders are shown. 
    
    19) nws_public_zones_color (String) - Default='black'. The color of the NWS Public Zone borders.
    
    20) nws_public_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Public Zone borders.
    
    21) nws_public_zones_zorder (Integer) - Default=3. The z-order of the NWS Public Zone borders. 
       For NWS Public Zone borders to be displayed the following condition must be met: nws_public_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    22) show_nws_fire_weather_zones (Boolean) - Default=False. When set to True, NWS Fire Weather Zone borders are shown. 
    
    23) nws_fire_weather_zones_color (String) - Default='black'. The color of the NWS Fire Weather Zone borders.
    
    24) nws_fire_weather_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Fire Weather Zone borders.
    
    25) nws_fire_weather_zones_zorder (Integer) - Default=3. The z-order of the NWS Fire Weather Zone borders. 
       For NWS Fire Weather Zone borders to be displayed the following condition must be met: nws_fire_weather_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    26) show_nws_cwa (Boolean) - Default=False. When set to True, NWS CWA borders are shown.
    
    27) nws_cwa_color (String) - Default='black'. The color of the NWS CWA borders.
    
    28) nws_cwa_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS CWA borders.
    
    29) nws_cwa_zorder (Integer) - Default=3. The z-order of the NWS CWA borders. 
       For NWS CWA borders to be displayed the following condition must be met: nws_cwa_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    30) show_calfire_boundaries (Boolean) - Default=False. When set to True, CalFire borders are shown.
    
    31) calfire_boundary_color (String) - Default='black'. The color of the CalFire borders.
    
    32) calfire_boundary_linewidth (Float or Integer) - Default=0.25. The linewidth of the CalFire borders.
    
    33) calfire_boundary_zorder (Integer) - Default=3. The z-order of the CalFire borders. 
       For CalFire borders to be displayed the following condition must be met: calfire_boundary_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.

    34) custom_shapefile_url (String or None) - Default=None. If the user wishes to set up an automation importing geometry from a shapefile that
        is not in the base version of FireWxPy, this is how to do that. The user will pass the download URL as a string by setting
        custom_shapefile_url='https"//shapefile_download_url.file_extension'. 
        
    35) custom_shapefile_file_extension (String) - Default='.zip'. This is the file extension of the zipped shapefile folder on the web
        server. 
        
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    36) custom_shapefile_color (String) - Default='black'. The color of the borders in the custom shapefile.
    
    37) custom_shapefile_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders in the custom shapefile.
    
    38) custom_shapefile_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    39) custom_geojson_url (String) - Default=None. If the user wishes to set up an automation with a publicly available
        geojson on the web, pass in the full download URL into this argument.
    
    40) custom_geojson_filename (String) - Default=None. The filename of the custom geojson file. 
    
    41) custom_geojson_folder_name (String) Default='Custom GeoJSON'. The folder where the custom geojson will be saved in.
    
    42) custom_geojson_color (String) - Default='black'. The edge color of the geometries in the custom geojson file.
    
    43) custom_geojson_linewidth (Integer or Float) - Default=0.5. The linewidth of the borders in the custom geojson. 
    
    44) custom_geojson_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    45) custom_shapefile_local_path (String) - Default=None. The path to a shapefile locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    46) custom_shapefile_local_color (String) - Default='black'. The edge color of the geometries in the shapefile.
    
    47) custom_shapefile_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    48) custom_shapefile_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    49) custom_geojson_local_path (String) - Default=None. The path to a geojson locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    50) custom_geojson_local_color (String) - Default='black'. The edge color of the geometries in the geojson.
    
    51) custom_geojson_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    52) custom_geojson_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    53) convert_custom_shapefile_crs (Boolean)- Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom shapefile. 
        
    54) convert_local_custom_shapefile_crs (Boolean) - Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom geojson.
        
    55)  refresh_cartographic_files (Boolean) - Default=True. Users that have automated pipelines set up for shapefiles. Having this set to
        True allows the client to delete and re-download the shapefiles with each run of the script. This is useful for shapefiles
        that have frequent geometry updates.
        
    56) reference_system (String) - Default='States & Counties'. The name of the borders overlaid onto the map.
    
    57) show_rivers (Boolean) - Default=False. Set to True to display rivers. 
    
    58) rivers_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    59) rivers_color (String) - Default='lightcyan'. The color of the river. 
    
    60) figure_x_length (Integer) - Default=12. The length of the figure in the x-direction.
    
    61) figure_y_length (Integer) - Default=12. The length of the figure in the y-direction.
    
    62) coastline_linewidth (Float or Integer) - Default=0.75. The linewidth of the coastline.
    
    63) land_color (String) - Default='beige'. The color of the land on a map.
    
    64) ocean_color (String) - Default='lightcyan'. The color of the ocean on a map.
    
    65) lakes_color (String) - Default='lightcyan'. The color of lakes on a map. 

    66) costline_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    67) ocean_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    68) lakes_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    69) land_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    70) decimate (Integer) - Default=150. This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. When set to 50, every 50 values will be queried. Use
        larger numbers for larger areas and smaller values for smaller areas. The default of 50 represents the setting for
        CONUS. 
        
    71) start (Integer) - Default=-30. The start of the filled contour range.
    
    72) stop (Integer) - Default=130. The end of the filled contour range. 
    
    73) step (Integer) - Default=1. The interval of the filled contours.
    
    74) facecolor (String) - Default='aliceblue'. The background color of the graphic. 
    
    75) primary_title_text (String) - Default='RTMA 2-METER relative_humidity [°F] & 10-METER WIND [MPH]'. The primary title
        of the graphic. 
        
    76) primary_title_textbox_color (String) - Default='wheat'. The color of the textbox of the primary title.
    
    77) primary_title_textbox_style (String) - Default='round'. The style of the textbox of the primary title.
    
    78) primary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    79) secondary_title_textbox_color (Float or Integer) Default='wheat'. The color of the textbox of the secondary title.
        
    80) secondary_title_textbox_style (String) - Default='round'. The style of the textbox of the secondary title.
    
    81) secondary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    82) primary_title_fontsize (Integer) - Default=12. Fontsize of the primary title text.
    
    83) secondary_title_fontsize (Integer) Default=10. Fontsize of the secondary title text.
    
    84) local_time (Boolean) - Default=True. Set to False for UTC time.
    
    85) signature_textbox_color (String) - Default='wheat'. The color of the textbox of the graphic's signature.
    
    86) signature_textbox_style (String) - Default='round'. The style of the textbox of the graphic's signature.
    
    87) signature_textbox_alpha (Float or Integer) - Default=1. A value between 0.5 and 1 representing transparency.

    88) signature_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    89) signature_fontsize (Integer) - Default=8. Fontsize of the graphic's signature text.
    
    90) signature_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the signature text box.
    
    91) signature_textbox_y_position (Float) - Default=-0.175. The y-position with respect to the plot axis of the signature text box.
    
    92) signature_text_new_lines (Boolean) - Default=False. When set to True, each section in the signature is on a new line.
        It is recommended to set this to True on plots that are longer from North to South than West to East. 
        
    93) reference_system_textbox_color (String) - Default='wheat'. The color of the textbox of the reference system.
    
    94) reference_system_textbox_style (String) - Default='round'. The style of the textbox of the reference system.
    
    95) reference_system_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    96) reference_system_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    97) reference_system_fontsize (Integer) - Default=6. Fontsize of the reference system label text.
    
    98) reference_system_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the reference system text box.
    
    99) reference_system_textbox_y_position (Float) - Default=0. The y-position with respect to the plot axis of the reference system text box.

    100) colorbar_shrink (Float or Integer) - Default=1. Fraction by which to multiply the size of the colorbar.
    
    101) colorbar_pad (Float) - Default=0.01. Fraction of original Axes between colorbar and new image Axes.
    
    102) tick_label_fontsize (Integer) - Default=9. The fontsize of the colorbar tick labels.
    
    103) colorbar_location (String) - Default='bottom'. The side of the plot axis where the colorbar will be displayed.
    
    104) colorbar_interval (Integer) - Default=10. The interval of tick marks on the colorbar.
    
    105) colorbar_aspect (Integer) - Default=50. Ratio of long to short dimensions.
    
    106) colormap (String) - Default='jet'. The Matplotlib colormap for filled contours being used OR set to 'custom' to create your own 
        custom colormapping. See the optional colors argument documentation (109) for more information on how to pass
        in a custom array of colors. 
        
    107) contourf_alpha (Float or Integer) - Default=0.5. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    108) contourf_zorder (Integer) - Default=2. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    109) colors (String List) - Default=colors=['magenta',
                                                'orchid',
                                                'plum',
                                                'darkviolet',
                                                'darkslateblue',
                                                'blue',
                                                'cyan',
                                                'lawngreen',
                                                'greenyellow',
                                                'olive',
                                                'gold',
                                                'goldenrod',
                                                'darkorange',
                                                'deeppink',
                                                'crimson',
                                                'darkred',
                                                'grey']
                                        
            The array of colors being used when colormap='custom'. 
            
    110) ds (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds=ds. 
            
    111) western_bound (Float or Integer) - Default=-125. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    112) eastern_bound (Float or Integer) - Default=-65. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    113) southern_bound (Float or Integer) - Default=20. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    114) northern_bound (Float or Integer) - Default=50. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    115) pixel_query_value_fontsize (Integer) - Default=4. The fontsize of the pixel query values.
    
    116) pixel_query_value_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    117) pixel_query_value_foreground (String) - Default='white'. The color of the foreground on the station plot (pixel query value).
    
    118) pixel_query_value_fontcolor (String) - Default='black'. The font color of the pixel query values.
    
    119) pixel_query_stroke_linewidth (Float or Integer) - Default=1. The linewidth of the pixel query values text outline.
    
    120) path (String) - Default='FireWxPy Graphics/RTMA/relative_humidity'. The directory where the graphic will save.
    
    121) filename (String) - Default='RTMA relative_humidity and Wind.png'. The filename of the image.
    
    122) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    123) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
        
    124) clear_data (Boolean) - Default=True. When set to True, the data will be cleared with each run of the script.
        Set to False when downloading the data outside of the function and passing the data in. 
        
    125) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB data to a file.
    
    126) notifications (String) - Default='off'. Notifications throughout the process. 

    127) custom_data_directory (String or None) - Default=None. The directory path where the data will be saved to. 

    128) mapcrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the map.
    
    129) datacrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the data.

    130) relative_humidity_var_key (String) - Default='2m_relative_humidity'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    131) wind_speed_var_key (String) - Default='10m_wind_speed'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    132) u_var_key (String) - Default='10m_u_wind_component'. The variable key name of the u-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    133) v_var_key (String) - Default='10m_v_wind_component'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    134) wind_direction_var_key (String) - Default='10m_wind_direction'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    135) time_coord_key (String) - Default='time'. The time coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    136) longitude_key (String) - Default='longitude'. The longitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
    
    137) latitude_key (String) - Default='latitude'. The latitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    138) convert_wind_speed (Boolean) - Default=True. Convert wind speed from m/s to either mph or kts.
    
    139) convert_to (String) - Default='mph'. Set to 'kts' for knots.
    
    140) pixel_query_type (String) - Default='barbs'. Display either wind barbs or numerical values.
    
    141) barb_length (Float or Integer) - Default=2. Length of wind barb.
    
    142) barb_width (Float or Integer) - Default=0.25. Width of wind barb. 
    
    143) barb_color (String) - Default='black'. Color of wind barb. 
    
    144) barb_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.

    Returns
    -------
    
    An image of the RTMA relative_humidity + Wind Analysis specified to the user's needs saved to {path}    
    """
    
    _build_directory_branch(f"{path}/{region.upper()}/{reference_system.upper()}")
    
    _mpl.rcParams['xtick.labelsize'] = tick_label_fontsize
    _mpl.rcParams['ytick.labelsize'] = tick_label_fontsize
    
    primary_title_box = dict(boxstyle=primary_title_textbox_style, 
                            facecolor=primary_title_textbox_color, 
                            alpha=primary_title_textbox_alpha)
    
    secondary_title_box = dict(boxstyle=secondary_title_textbox_style, 
                            facecolor=secondary_title_textbox_color, 
                            alpha=secondary_title_textbox_alpha)
    
    signature_box = dict(boxstyle=signature_textbox_style, 
                            facecolor=signature_textbox_color, 
                            alpha=signature_textbox_alpha)
    
    reference_system_box = dict(boxstyle=reference_system_textbox_style, 
                            facecolor=reference_system_textbox_color, 
                            alpha=reference_system_textbox_alpha)
    
    levels = _np.arange(start, (stop + step), step)
    ticks = levels[::colorbar_interval]
    
    western_bound, eastern_bound, southern_bound, northern_bound = _bounding_box(region,
                                                                                 western_bound,
                                                                                 eastern_bound,
                                                                                 southern_bound,
                                                                                 northern_bound)
    
    if ds is None:
        ds = _rtma(proxies=proxies,
                   clear_recycle_bin=clear_recycle_bin,
                   clear_data=clear_data,
                   western_bound=western_bound,
                   eastern_bound=eastern_bound,
                   southern_bound=southern_bound,
                   northern_bound=northern_bound,
                   convert_temperature=True,
                   convert_to='fahrenheit',
                   chunk_size=chunk_size,
                   notifications=notifications,
                   custom_directory=custom_data_directory)
    else:
        ds = ds
        
    if convert_wind_speed == True:
        if convert_to == 'mph':
            ds[wind_speed_var_key] = _calc.mps_to_mph(ds[wind_speed_var_key])
            ds[u_var_key] = _calc.mps_to_mph(ds[u_var_key])
            ds[v_var_key] = _calc.mps_to_mph(ds[v_var_key])
        else:
            ds[wind_speed_var_key] = _calc.mph_to_kts(ds[wind_speed_var_key])
            ds[u_var_key] = _calc.mph_to_kts(ds[u_var_key])
            ds[v_var_key] = _calc.mph_to_kts(ds[v_var_key])
            
    else:
        pass
        
    if colormap == 'custom':
        cmap = _mcolors.LinearSegmentedColormap.from_list("wind gust", colors)
    else:
        cmap = colormap
    
    valid_time = _pd.to_datetime(ds[time_coord_key].to_pandas())
    valid_time = valid_time.tz_localize('UTC')
    time = valid_time.astimezone(_to_zone)
    time_utc = time.astimezone(_from_zone)
    
    fig = _plt.figure(figsize=(figure_x_length, figure_y_length))
    fig.set_facecolor(facecolor)
    
    ax = fig.add_subplot(1,1,1, projection=mapcrs)
    ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax.add_feature(_cfeature.COASTLINE.with_scale('50m'), linewidth=coastline_linewidth, zorder=costline_zorder)
    ax.add_feature(_cfeature.LAND, color=land_color, zorder=land_zorder)
    ax.add_feature(_cfeature.OCEAN, color=ocean_color, zorder=ocean_zorder)
    ax.add_feature(_cfeature.LAKES, color=lakes_color, zorder=lakes_zorder)
    if show_rivers is True:
        ax.add_feature(_cfeature.RIVERS, color=rivers_color, zorder=rivers_zorder)
    if show_states is True:
        states = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_States_Territories.zip",
                                            f"Cartographic Files/US States",
                                            f"US_States_Territories.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            state_border_color,
                                            datacrs)
        
        ax.add_geometries(states, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=state_border_color, 
                          linewidth=state_border_linewidth, 
                          zorder=state_border_zorder)
    
    if show_counties is True:
        counties = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_Counties.zip",
                                            f"Cartographic Files/US Counties",
                                            f"US_Counties.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            county_border_color,
                                            datacrs)
        
        ax.add_geometries(counties, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=county_border_color, 
                          linewidth=county_border_linewidth, 
                          zorder=county_border_zorder)
        
    if show_gacc_boundaries is True:
        gacc = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/GACC_Boundaries_2026.zip",
                                            f"Cartographic Files/GACC Boundaries",
                                            f"GACC_Boundaries_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            gacc_border_color,
                                            datacrs)
        
        ax.add_geometries(gacc, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=gacc_border_color, 
                          linewidth=gacc_border_linewidth, 
                          zorder=gacc_border_zorder)
    
    if show_predictive_services_areas is True:
        psa = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/PSA_Boundaries.zip",
                                            f"Cartographic Files/PSA Boundaries",
                                            f"PSA_Boundaries.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            predictive_services_areas_color,
                                            datacrs)
        
        ax.add_geometries(psa, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=predictive_services_areas_color, 
                          linewidth=predictive_services_areas_linewidth, 
                          zorder=predictive_services_areas_zorder)
        
    if show_nws_public_zones is True:
        pz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Public_Zones_2026.zip",
                                            f"Cartographic Files/NWS Public Zones",
                                            f"NWS_Public_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_public_zones_color,
                                            datacrs)
        
        ax.add_geometries(pz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_public_zones_color, 
                          linewidth=nws_public_zones_linewidth, 
                          zorder=nws_public_zones_zorder)
        
    if show_nws_fire_weather_zones is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Fire_Weather_Zones_2026.zip",
                                            f"Cartographic Files/NWS Fire Weather Zones",
                                            f"NWS_Fire_Weather_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_fire_weather_zones_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_fire_weather_zones_color, 
                          linewidth=nws_fire_weather_zones_linewidth, 
                          zorder=nws_fire_weather_zones_zorder)
        
    if show_nws_cwa is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_CWA_2026.zip",
                                            f"Cartographic Files/NWS CWAs",
                                            f"NWS_CWA_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_cwa_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_cwa_color, 
                          linewidth=nws_cwa_linewidth, 
                          zorder=nws_cwa_zorder)
        
    if show_calfire_boundaries is True:
        calfire = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/CALFIRE/CalFire_Administrative_Units.zip",
                                            f"Cartographic Files/CalFire",
                                            f"CalFire_Administrative_Units.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            calfire_boundary_color,
                                            datacrs,
                                            convert_crs=True,
                                            convert_to='EPSG:4326')
        
        ax.add_geometries(calfire, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=calfire_boundary_color, 
                          linewidth=calfire_boundary_linewidth, 
                          zorder=calfire_boundary_zorder)
        
    if custom_shapefile_url is not None:
        
        fname = _get_filename_from_url(custom_shapefile_url)
        
        custom_shape = _import_shapefile_from_web(custom_shapefile_url,
                                            f"Cartographic Files/{custom_shapefile_folder_name}",
                                            fname,
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            custom_shapefile_file_extension,
                                            custom_shapefile_color,
                                            convert_crs=convert_custom_shapefile_crs)
        
        ax.add_geometries(custom_shape, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_color, 
                          linewidth=custom_shapefile_linewidth, 
                          zorder=custom_shapefile_zorder)
        
    if custom_geojson_url is not None:
        
        custom_json = _import_geojson_from_web(custom_geojson_url,
                                                f"Cartographic Files/{custom_geojson_folder_name}", 
                                                custom_geojson_filename, 
                                                proxies, 
                                                chunk_size,
                                                notifications, 
                                                refresh_cartographic_files)
        
        ax.add_geometries(custom_json, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_color, 
                          linewidth=custom_geojson_linewidth, 
                          zorder=custom_geojson_zorder)
        
    if custom_shapefile_local_path is not None:
        custom_local_shapefile = _import_shapefile_local(custom_shapefile_local_path,
                                                            custom_shapefile_local_color,
                                                            convert_crs=convert_local_custom_shapefile_crs)
        
        ax.add_geometries(custom_local_shapefile, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_local_color, 
                          linewidth=custom_shapefile_local_linewidth, 
                          zorder=custom_shapefile_local_zorder)
        
    if custom_geojson_local_path is not None:
        custom_local_geojson = _import_geojson_local(custom_geojson_local_path)
        
        ax.add_geometries(custom_local_geojson, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_local_color, 
                          linewidth=custom_geojson_local_linewidth, 
                          zorder=custom_geojson_local_zorder)
    
    cs = ax.contourf(ds[longitude_key],
                ds[latitude_key],
                ds[relative_humidity_var_key],
                cmap=cmap,
                levels=levels,
                transform=datacrs,
                alpha=contourf_alpha,
                zorder=contourf_zorder,
                extend='both')
    
    fig.colorbar(cs, 
                shrink=colorbar_shrink, 
                pad=colorbar_pad, 
                location=colorbar_location,
                ticks=ticks,
                aspect=colorbar_aspect)
    
    _plt.title(f"{primary_title_text}", 
               fontsize=primary_title_fontsize, 
               fontweight='bold',
               bbox=primary_title_box,
               loc='left')
    
    if local_time is True:
        _plt.title(f"Valid: {time.strftime('%m/%d/%Y %H:00')} {_timezone}", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
    else:
        _plt.title(f"Valid: {time_utc.strftime('%m/%d/%Y %H:00')} UTC", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
        
    if signature_text_new_lines is False:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')} | Data Source: NCEP/NOMADS | Created: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    else:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')}\nData Source: NCEP/NOMADS\nCreated: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    
    ax.text(reference_system_textbox_x_position, 
            reference_system_textbox_y_position,
            f"Reference System: {reference_system}",
            fontsize=reference_system_fontsize,
            fontweight='bold',
            bbox=reference_system_box,
            transform=ax.transAxes,
            zorder=reference_system_textbox_zorder)
        
    
        
    temp_vals = _fix_var_array(ds,
                    relative_humidity_var_key,
                    0,
                    decimate)
    
    u_vals = _fix_var_array(ds,
                    u_var_key,
                    0,
                    decimate)
    
    v_vals = _fix_var_array(ds,
                    v_var_key,
                    0,
                    decimate)
    
    ws_vals = _fix_var_array(ds,
                    wind_speed_var_key,
                    0,
                    decimate)

    stn = _mpplots.StationPlot(ax, temp_vals['longitude'], temp_vals['latitude'],
                                transform=datacrs, 
                                fontsize=pixel_query_value_fontsize, 
                                zorder=pixel_query_value_zorder, 
                                clip_on=True)


    stn.plot_parameter('NW', 
                       temp_vals[relative_humidity_var_key], 
                       color=relative_humidity_pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)
    
    stn.plot_parameter('NE', 
                       ws_vals[wind_speed_var_key], 
                       color= wind_speed_pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)

    stn.plot_barb(u_vals[u_var_key], 
                    v_vals[v_var_key],
                    color=barb_color, 
                    length=barb_length, 
                    linewidth=barb_width,
                    zorder=barb_zorder)

    fig.savefig(f"{path}/{region.upper()}/{reference_system.upper()}/{filename}", bbox_inches='tight')
    _plt.close(fig)
    if notifications == 'on':
        print(f"{filename} saved to {path}/{region.upper()}")
        
        
def plot_relative_humidity_and_gust(region='conus',
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=150,
                     start=-30,
                     stop=130,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER relative_humidity [°F] & 10-METER GUST [MPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=12,
                     secondary_title_fontsize=10,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=10,
                     colorbar_aspect=50,
                     colormap='jet',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['magenta',
                             'orchid',
                             'plum',
                             'darkviolet',
                             'darkslateblue',
                             'blue',
                             'cyan',
                             'lawngreen',
                             'greenyellow',
                             'olive',
                             'gold',
                             'goldenrod',
                             'darkorange',
                             'deeppink',
                             'crimson',
                             'darkred',
                             'grey'],
                     ds=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     relative_humidity_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA/relative_humidity',
                     filename='RTMA relative_humidity and Gust.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     relative_humidity_var_key='2m_relative_humidity',
                     wind_gust_var_key='10m_wind_gust',
                     u_var_key='10m_u_wind_component',
                     v_var_key='10m_v_wind_component',
                     wind_direction_var_key='10m_wind_direction',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_to='mph',
                     barb_length=4,
                     barb_width=0.5,
                     barb_color='black',
                     barb_zorder=7):
    
    """
    This function plots the latest Real Time Mesoscale Analysis (RTMA) for relative_humidity + gust.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Entire CONUS region.
            ii) 'jet' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Required Arguments: None
    
    Optional Arguments:
    
    1) region (String) - Default='conus'. The region of the plot. Use the 2-letter state abbreviation or 4-letter GACC abbreviation.
        If the user wants a completely custom region where they define their own lat/lon bounds, set region='custom'. 
        
    2) show_states (Boolean) - Default=True. When set to True, U.S. state borders are shown. 
    
    3) state_border_color (String) - Default='black'. The color of the U.S. state borders.
    
    4) state_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the U.S. state borders.
    
    5) state_border_zorder (Integer) - Default=3. The z-order of the state borders. For state borders to be displayed
        the following condition must be met: state_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
        
    6) show_counties (Boolean) - Default=True. When set to True, U.S. county borders are shown. 
    
    7) county_border_color (String) - Default='black'. The color of the U.S. county borders.
    
    8) county_border_linewidth (Float or Integer) - Default=0.25. The linewidth of the U.S. county borders.
    
    9) county_border_zorder (Integer) - Default=3. The z-order of the county borders. For county borders to be displayed
        the following condition must be met: county_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
    
    10) show_gacc_boundaries (Boolean) - Default=False. When set to True, Geographic Area Coordination Center borders are shown. 
    
    11) gacc_border_color (String) - Default='black'. The color of the Geographic Area Coordination Center borders.
    
    12) gacc_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the Geographic Area Coordination Center borders.
    
    13) gacc_border_zorder (Integer) - Default=3. The z-order of the Geographic Area Coordination Center borders. 
       For Geographic Area Coordination Center borders to be displayed the following condition must be met: gacc_border_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
       
    14) show_predictive_services_areas (Boolean) - Default=False. When set to True, Predictive Services Areas borders are shown. 
    
    15) predictive_services_areas_color (String) - Default='black'. The color of the Predictive Services Areas borders.
    
    16) predictive_services_areas_linewidth (Float or Integer) - Default=0.25. The linewidth of the Predictive Services Areas borders.
    
    17) predictive_services_areas_zorder (Integer) - Default=3. The z-order of the Predictive Services Areas borders. 
       For Predictive Services Areas borders to be displayed the following condition must be met: predictive_services_areas_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    18) show_nws_public_zones (Boolean) - Default=False. When set to True, NWS Public Zone borders are shown. 
    
    19) nws_public_zones_color (String) - Default='black'. The color of the NWS Public Zone borders.
    
    20) nws_public_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Public Zone borders.
    
    21) nws_public_zones_zorder (Integer) - Default=3. The z-order of the NWS Public Zone borders. 
       For NWS Public Zone borders to be displayed the following condition must be met: nws_public_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
    22) show_nws_fire_weather_zones (Boolean) - Default=False. When set to True, NWS Fire Weather Zone borders are shown. 
    
    23) nws_fire_weather_zones_color (String) - Default='black'. The color of the NWS Fire Weather Zone borders.
    
    24) nws_fire_weather_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Fire Weather Zone borders.
    
    25) nws_fire_weather_zones_zorder (Integer) - Default=3. The z-order of the NWS Fire Weather Zone borders. 
       For NWS Fire Weather Zone borders to be displayed the following condition must be met: nws_fire_weather_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    26) show_nws_cwa (Boolean) - Default=False. When set to True, NWS CWA borders are shown.
    
    27) nws_cwa_color (String) - Default='black'. The color of the NWS CWA borders.
    
    28) nws_cwa_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS CWA borders.
    
    29) nws_cwa_zorder (Integer) - Default=3. The z-order of the NWS CWA borders. 
       For NWS CWA borders to be displayed the following condition must be met: nws_cwa_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
    30) show_calfire_boundaries (Boolean) - Default=False. When set to True, CalFire borders are shown.
    
    31) calfire_boundary_color (String) - Default='black'. The color of the CalFire borders.
    
    32) calfire_boundary_linewidth (Float or Integer) - Default=0.25. The linewidth of the CalFire borders.
    
    33) calfire_boundary_zorder (Integer) - Default=3. The z-order of the CalFire borders. 
       For CalFire borders to be displayed the following condition must be met: calfire_boundary_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.

    34) custom_shapefile_url (String or None) - Default=None. If the user wishes to set up an automation importing geometry from a shapefile that
        is not in the base version of FireWxPy, this is how to do that. The user will pass the download URL as a string by setting
        custom_shapefile_url='https"//shapefile_download_url.file_extension'. 
        
    35) custom_shapefile_file_extension (String) - Default='.zip'. This is the file extension of the zipped shapefile folder on the web
        server. 
        
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    36) custom_shapefile_color (String) - Default='black'. The color of the borders in the custom shapefile.
    
    37) custom_shapefile_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders in the custom shapefile.
    
    38) custom_shapefile_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    39) custom_geojson_url (String) - Default=None. If the user wishes to set up an automation with a publicly available
        geojson on the web, pass in the full download URL into this argument.
    
    40) custom_geojson_filename (String) - Default=None. The filename of the custom geojson file. 
    
    41) custom_geojson_folder_name (String) Default='Custom GeoJSON'. The folder where the custom geojson will be saved in.
    
    42) custom_geojson_color (String) - Default='black'. The edge color of the geometries in the custom geojson file.
    
    43) custom_geojson_linewidth (Integer or Float) - Default=0.5. The linewidth of the borders in the custom geojson. 
    
    44) custom_geojson_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    45) custom_shapefile_local_path (String) - Default=None. The path to a shapefile locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    46) custom_shapefile_local_color (String) - Default='black'. The edge color of the geometries in the shapefile.
    
    47) custom_shapefile_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    48) custom_shapefile_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    49) custom_geojson_local_path (String) - Default=None. The path to a geojson locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
    50) custom_geojson_local_color (String) - Default='black'. The edge color of the geometries in the geojson.
    
    51) custom_geojson_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
    52) custom_geojson_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    53) convert_custom_shapefile_crs (Boolean)- Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom shapefile. 
        
    54) convert_local_custom_shapefile_crs (Boolean) - Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom geojson.
        
    55)  refresh_cartographic_files (Boolean) - Default=True. Users that have automated pipelines set up for shapefiles. Having this set to
        True allows the client to delete and re-download the shapefiles with each run of the script. This is useful for shapefiles
        that have frequent geometry updates.
        
    56) reference_system (String) - Default='States & Counties'. The name of the borders overlaid onto the map.
    
    57) show_rivers (Boolean) - Default=False. Set to True to display rivers. 
    
    58) rivers_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    59) rivers_color (String) - Default='lightcyan'. The color of the river. 
    
    60) figure_x_length (Integer) - Default=12. The length of the figure in the x-direction.
    
    61) figure_y_length (Integer) - Default=12. The length of the figure in the y-direction.
    
    62) coastline_linewidth (Float or Integer) - Default=0.75. The linewidth of the coastline.
    
    63) land_color (String) - Default='beige'. The color of the land on a map.
    
    64) ocean_color (String) - Default='lightcyan'. The color of the ocean on a map.
    
    65) lakes_color (String) - Default='lightcyan'. The color of lakes on a map. 

    66) costline_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    67) ocean_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    68) lakes_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
    69) land_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    70) decimate (Integer) - Default=150. This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. When set to 50, every 50 values will be queried. Use
        larger numbers for larger areas and smaller values for smaller areas. The default of 50 represents the setting for
        CONUS. 
        
    71) start (Integer) - Default=-30. The start of the filled contour range.
    
    72) stop (Integer) - Default=130. The end of the filled contour range. 
    
    73) step (Integer) - Default=1. The interval of the filled contours.
    
    74) facecolor (String) - Default='aliceblue'. The background color of the graphic. 
    
    75) primary_title_text (String) - Default='RTMA 2-METER relative_humidity [°F] & 10-METER GUST [MPH]'. The primary title
        of the graphic. 
        
    76) primary_title_textbox_color (String) - Default='wheat'. The color of the textbox of the primary title.
    
    77) primary_title_textbox_style (String) - Default='round'. The style of the textbox of the primary title.
    
    78) primary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    79) secondary_title_textbox_color (Float or Integer) Default='wheat'. The color of the textbox of the secondary title.
        
    80) secondary_title_textbox_style (String) - Default='round'. The style of the textbox of the secondary title.
    
    81) secondary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    82) primary_title_fontsize (Integer) - Default=12. Fontsize of the primary title text.
    
    83) secondary_title_fontsize (Integer) Default=10. Fontsize of the secondary title text.
    
    84) local_time (Boolean) - Default=True. Set to False for UTC time.
    
    85) signature_textbox_color (String) - Default='wheat'. The color of the textbox of the graphic's signature.
    
    86) signature_textbox_style (String) - Default='round'. The style of the textbox of the graphic's signature.
    
    87) signature_textbox_alpha (Float or Integer) - Default=1. A value between 0.5 and 1 representing transparency.

    88) signature_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    89) signature_fontsize (Integer) - Default=8. Fontsize of the graphic's signature text.
    
    90) signature_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the signature text box.
    
    91) signature_textbox_y_position (Float) - Default=-0.175. The y-position with respect to the plot axis of the signature text box.
    
    92) signature_text_new_lines (Boolean) - Default=False. When set to True, each section in the signature is on a new line.
        It is recommended to set this to True on plots that are longer from North to South than West to East. 
        
    93) reference_system_textbox_color (String) - Default='wheat'. The color of the textbox of the reference system.
    
    94) reference_system_textbox_style (String) - Default='round'. The style of the textbox of the reference system.
    
    95) reference_system_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    96) reference_system_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    97) reference_system_fontsize (Integer) - Default=6. Fontsize of the reference system label text.
    
    98) reference_system_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the reference system text box.
    
    99) reference_system_textbox_y_position (Float) - Default=0. The y-position with respect to the plot axis of the reference system text box.

    100) colorbar_shrink (Float or Integer) - Default=1. Fraction by which to multiply the size of the colorbar.
    
    101) colorbar_pad (Float) - Default=0.01. Fraction of original Axes between colorbar and new image Axes.
    
    102) tick_label_fontsize (Integer) - Default=9. The fontsize of the colorbar tick labels.
    
    103) colorbar_location (String) - Default='bottom'. The side of the plot axis where the colorbar will be displayed.
    
    104) colorbar_interval (Integer) - Default=10. The interval of tick marks on the colorbar.
    
    105) colorbar_aspect (Integer) - Default=50. Ratio of long to short dimensions.
    
    106) colormap (String) - Default='jet'. The Matplotlib colormap for filled contours being used OR set to 'custom' to create your own 
        custom colormapping. See the optional colors argument documentation (109) for more information on how to pass
        in a custom array of colors. 
        
    107) contourf_alpha (Float or Integer) - Default=0.5. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
    108) contourf_zorder (Integer) - Default=2. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    109) colors (String List) - Default=colors=['magenta',
                                                'orchid',
                                                'plum',
                                                'darkviolet',
                                                'darkslateblue',
                                                'blue',
                                                'cyan',
                                                'lawngreen',
                                                'greenyellow',
                                                'olive',
                                                'gold',
                                                'goldenrod',
                                                'darkorange',
                                                'deeppink',
                                                'crimson',
                                                'darkred',
                                                'grey']
                                        
            The array of colors being used when colormap='custom'. 
            
    110) ds (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds=ds. 
            
    111) western_bound (Float or Integer) - Default=-125. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    112) eastern_bound (Float or Integer) - Default=-65. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    113) southern_bound (Float or Integer) - Default=20. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    114) northern_bound (Float or Integer) - Default=50. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
    115) pixel_query_value_fontsize (Integer) - Default=4. The fontsize of the pixel query values.
    
    116) pixel_query_value_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
    117) pixel_query_value_foreground (String) - Default='white'. The color of the foreground on the station plot (pixel query value).
    
    118) pixel_query_value_fontcolor (String) - Default='black'. The font color of the pixel query values.
    
    119) pixel_query_stroke_linewidth (Float or Integer) - Default=1. The linewidth of the pixel query values text outline.
    
    120) path (String) - Default='FireWxPy Graphics/RTMA/relative_humidity'. The directory where the graphic will save.
    
    121) filename (String) - Default='RTMA relative_humidity and Gust.png'. The filename of the image.
    
    122) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

    123) clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
        
    124) clear_data (Boolean) - Default=True. When set to True, the data will be cleared with each run of the script.
        Set to False when downloading the data outside of the function and passing the data in. 
        
    125) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB data to a file.
    
    126) notifications (String) - Default='off'. Notifications throughout the process. 

    127) custom_data_directory (String or None) - Default=None. The directory path where the data will be saved to. 

    128) mapcrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the map.
    
    129) datacrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the data.

    130) relative_humidity_var_key (String) - Default='2m_relative_humidity'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    131) wind_gust_var_key (String) - Default='10m_wind_gust'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    132) u_var_key (String) - Default='10m_u_wind_component'. The variable key name of the u-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    133) v_var_key (String) - Default='10m_v_wind_component'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    134) wind_direction_var_key (String) - Default='10m_wind_direction'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    135) time_coord_key (String) - Default='time'. The time coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    136) longitude_key (String) - Default='longitude'. The longitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
    
    137) latitude_key (String) - Default='latitude'. The latitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
    138) convert_wind_speed (Boolean) - Default=True. Convert wind speed from m/s to either mph or kts.
    
    139) convert_to (String) - Default='mph'. Set to 'kts' for knots.
    
    140) pixel_query_type (String) - Default='barbs'. Display either wind barbs or numerical values.
    
    141) barb_length (Float or Integer) - Default=2. Length of wind barb.
    
    142) barb_width (Float or Integer) - Default=0.25. Width of wind barb. 
    
    143) barb_color (String) - Default='black'. Color of wind barb. 
    
    144) barb_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.

    Returns
    -------
    
    An image of the RTMA Relative Humidity + Gust Analysis specified to the user's needs saved to {path}    
    """
    
    _build_directory_branch(f"{path}/{region.upper()}/{reference_system.upper()}")
    
    _mpl.rcParams['xtick.labelsize'] = tick_label_fontsize
    _mpl.rcParams['ytick.labelsize'] = tick_label_fontsize
    
    primary_title_box = dict(boxstyle=primary_title_textbox_style, 
                            facecolor=primary_title_textbox_color, 
                            alpha=primary_title_textbox_alpha)
    
    secondary_title_box = dict(boxstyle=secondary_title_textbox_style, 
                            facecolor=secondary_title_textbox_color, 
                            alpha=secondary_title_textbox_alpha)
    
    signature_box = dict(boxstyle=signature_textbox_style, 
                            facecolor=signature_textbox_color, 
                            alpha=signature_textbox_alpha)
    
    reference_system_box = dict(boxstyle=reference_system_textbox_style, 
                            facecolor=reference_system_textbox_color, 
                            alpha=reference_system_textbox_alpha)
    
    levels = _np.arange(start, (stop + step), step)
    ticks = levels[::colorbar_interval]
    
    western_bound, eastern_bound, southern_bound, northern_bound = _bounding_box(region,
                                                                                 western_bound,
                                                                                 eastern_bound,
                                                                                 southern_bound,
                                                                                 northern_bound)
    
    if ds is None:
        ds = _rtma(proxies=proxies,
                   clear_recycle_bin=clear_recycle_bin,
                   clear_data=clear_data,
                   western_bound=western_bound,
                   eastern_bound=eastern_bound,
                   southern_bound=southern_bound,
                   northern_bound=northern_bound,
                   convert_temperature=True,
                   convert_to='fahrenheit',
                   chunk_size=chunk_size,
                   notifications=notifications,
                   custom_directory=custom_data_directory)
    else:
        ds = ds
        
    if convert_wind_speed == True:
        if convert_to == 'mph':
            ds[wind_gust_var_key] = _calc.mps_to_mph(ds[wind_gust_var_key])
            ds[u_var_key] = _calc.mps_to_mph(ds[u_var_key])
            ds[v_var_key] = _calc.mps_to_mph(ds[v_var_key])
        else:
            ds[wind_gust_var_key] = _calc.mph_to_kts(ds[wind_gust_var_key])
            ds[u_var_key] = _calc.mph_to_kts(ds[u_var_key])
            ds[v_var_key] = _calc.mph_to_kts(ds[v_var_key])
            
    else:
        pass
    
    ds = _calc.u_v_components(ds,
                            u_var_key,
                            v_var_key,
                            wind_direction_var_key,
                            wind_gust_var_key)
        
    if colormap == 'custom':
        cmap = _mcolors.LinearSegmentedColormap.from_list("wind gust", colors)
    else:
        cmap = colormap
    
    valid_time = _pd.to_datetime(ds[time_coord_key].to_pandas())
    valid_time = valid_time.tz_localize('UTC')
    time = valid_time.astimezone(_to_zone)
    time_utc = time.astimezone(_from_zone)
    
    fig = _plt.figure(figsize=(figure_x_length, figure_y_length))
    fig.set_facecolor(facecolor)
    
    ax = fig.add_subplot(1,1,1, projection=mapcrs)
    ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax.add_feature(_cfeature.COASTLINE.with_scale('50m'), linewidth=coastline_linewidth, zorder=costline_zorder)
    ax.add_feature(_cfeature.LAND, color=land_color, zorder=land_zorder)
    ax.add_feature(_cfeature.OCEAN, color=ocean_color, zorder=ocean_zorder)
    ax.add_feature(_cfeature.LAKES, color=lakes_color, zorder=lakes_zorder)
    if show_rivers is True:
        ax.add_feature(_cfeature.RIVERS, color=rivers_color, zorder=rivers_zorder)
    if show_states is True:
        states = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_States_Territories.zip",
                                            f"Cartographic Files/US States",
                                            f"US_States_Territories.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            state_border_color,
                                            datacrs)
        
        ax.add_geometries(states, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=state_border_color, 
                          linewidth=state_border_linewidth, 
                          zorder=state_border_zorder)
    
    if show_counties is True:
        counties = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_Counties.zip",
                                            f"Cartographic Files/US Counties",
                                            f"US_Counties.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            county_border_color,
                                            datacrs)
        
        ax.add_geometries(counties, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=county_border_color, 
                          linewidth=county_border_linewidth, 
                          zorder=county_border_zorder)
        
    if show_gacc_boundaries is True:
        gacc = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/GACC_Boundaries_2026.zip",
                                            f"Cartographic Files/GACC Boundaries",
                                            f"GACC_Boundaries_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            gacc_border_color,
                                            datacrs)
        
        ax.add_geometries(gacc, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=gacc_border_color, 
                          linewidth=gacc_border_linewidth, 
                          zorder=gacc_border_zorder)
    
    if show_predictive_services_areas is True:
        psa = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/PSA_Boundaries.zip",
                                            f"Cartographic Files/PSA Boundaries",
                                            f"PSA_Boundaries.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            predictive_services_areas_color,
                                            datacrs)
        
        ax.add_geometries(psa, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=predictive_services_areas_color, 
                          linewidth=predictive_services_areas_linewidth, 
                          zorder=predictive_services_areas_zorder)
        
    if show_nws_public_zones is True:
        pz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Public_Zones_2026.zip",
                                            f"Cartographic Files/NWS Public Zones",
                                            f"NWS_Public_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_public_zones_color,
                                            datacrs)
        
        ax.add_geometries(pz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_public_zones_color, 
                          linewidth=nws_public_zones_linewidth, 
                          zorder=nws_public_zones_zorder)
        
    if show_nws_fire_weather_zones is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Fire_Weather_Zones_2026.zip",
                                            f"Cartographic Files/NWS Fire Weather Zones",
                                            f"NWS_Fire_Weather_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_fire_weather_zones_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_fire_weather_zones_color, 
                          linewidth=nws_fire_weather_zones_linewidth, 
                          zorder=nws_fire_weather_zones_zorder)
        
    if show_nws_cwa is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_CWA_2026.zip",
                                            f"Cartographic Files/NWS CWAs",
                                            f"NWS_CWA_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_cwa_color,
                                            datacrs)
        
        ax.add_geometries(fwz, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=nws_cwa_color, 
                          linewidth=nws_cwa_linewidth, 
                          zorder=nws_cwa_zorder)
        
    if show_calfire_boundaries is True:
        calfire = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/CALFIRE/CalFire_Administrative_Units.zip",
                                            f"Cartographic Files/CalFire",
                                            f"CalFire_Administrative_Units.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            calfire_boundary_color,
                                            datacrs,
                                            convert_crs=True,
                                            convert_to='EPSG:4326')
        
        ax.add_geometries(calfire, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=calfire_boundary_color, 
                          linewidth=calfire_boundary_linewidth, 
                          zorder=calfire_boundary_zorder)
        
    if custom_shapefile_url is not None:
        
        fname = _get_filename_from_url(custom_shapefile_url)
        
        custom_shape = _import_shapefile_from_web(custom_shapefile_url,
                                            f"Cartographic Files/{custom_shapefile_folder_name}",
                                            fname,
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            custom_shapefile_file_extension,
                                            custom_shapefile_color,
                                            convert_crs=convert_custom_shapefile_crs)
        
        ax.add_geometries(custom_shape, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_color, 
                          linewidth=custom_shapefile_linewidth, 
                          zorder=custom_shapefile_zorder)
        
    if custom_geojson_url is not None:
        
        custom_json = _import_geojson_from_web(custom_geojson_url,
                                                f"Cartographic Files/{custom_geojson_folder_name}", 
                                                custom_geojson_filename, 
                                                proxies, 
                                                chunk_size,
                                                notifications, 
                                                refresh_cartographic_files)
        
        ax.add_geometries(custom_json, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_color, 
                          linewidth=custom_geojson_linewidth, 
                          zorder=custom_geojson_zorder)
        
    if custom_shapefile_local_path is not None:
        custom_local_shapefile = _import_shapefile_local(custom_shapefile_local_path,
                                                            custom_shapefile_local_color,
                                                            convert_crs=convert_local_custom_shapefile_crs)
        
        ax.add_geometries(custom_local_shapefile, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_shapefile_local_color, 
                          linewidth=custom_shapefile_local_linewidth, 
                          zorder=custom_shapefile_local_zorder)
        
    if custom_geojson_local_path is not None:
        custom_local_geojson = _import_geojson_local(custom_geojson_local_path)
        
        ax.add_geometries(custom_local_geojson, 
                          crs=datacrs, 
                          facecolor='none', 
                          edgecolor=custom_geojson_local_color, 
                          linewidth=custom_geojson_local_linewidth, 
                          zorder=custom_geojson_local_zorder)
    
    cs = ax.contourf(ds[longitude_key],
                ds[latitude_key],
                ds[relative_humidity_var_key],
                cmap=cmap,
                levels=levels,
                transform=datacrs,
                alpha=contourf_alpha,
                zorder=contourf_zorder,
                extend='both')
    
    fig.colorbar(cs, 
                shrink=colorbar_shrink, 
                pad=colorbar_pad, 
                location=colorbar_location,
                ticks=ticks,
                aspect=colorbar_aspect)
    
    _plt.title(f"{primary_title_text}", 
               fontsize=primary_title_fontsize, 
               fontweight='bold',
               bbox=primary_title_box,
               loc='left')
    
    if local_time is True:
        _plt.title(f"Valid: {time.strftime('%m/%d/%Y %H:00')} {_timezone}", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
    else:
        _plt.title(f"Valid: {time_utc.strftime('%m/%d/%Y %H:00')} UTC", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
        
    if signature_text_new_lines is False:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')} | Data Source: NCEP/NOMADS | Created: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    else:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')}\nData Source: NCEP/NOMADS\nCreated: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    
    ax.text(reference_system_textbox_x_position, 
            reference_system_textbox_y_position,
            f"Reference System: {reference_system}",
            fontsize=reference_system_fontsize,
            fontweight='bold',
            bbox=reference_system_box,
            transform=ax.transAxes,
            zorder=reference_system_textbox_zorder)
        
    
        
    rh_vals = _fix_var_array(ds,
                    relative_humidity_var_key,
                    0,
                    decimate)
    
    u_vals = _fix_var_array(ds,
                    u_var_key,
                    0,
                    decimate)
    
    v_vals = _fix_var_array(ds,
                    v_var_key,
                    0,
                    decimate)
    
    wg_vals = _fix_var_array(ds,
                    wind_gust_var_key,
                    0,
                    decimate)

    stn = _mpplots.StationPlot(ax, rh_vals['longitude'], rh_vals['latitude'],
                                transform=datacrs, 
                                fontsize=pixel_query_value_fontsize, 
                                zorder=pixel_query_value_zorder, 
                                clip_on=True)


    stn.plot_parameter('NW', 
                       rh_vals[relative_humidity_var_key], 
                       color=relative_humidity_pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)
    
    stn.plot_parameter('NE', 
                       wg_vals[wind_gust_var_key], 
                       color= wind_speed_pixel_query_value_fontcolor, 
                       path_effects=[_withStroke(linewidth=pixel_query_stroke_linewidth, 
                                                 foreground=pixel_query_value_foreground)], 
                       zorder=pixel_query_value_zorder)

    stn.plot_barb(u_vals[u_var_key], 
                    v_vals[v_var_key],
                    color=barb_color, 
                    length=barb_length, 
                    linewidth=barb_width,
                    zorder=barb_zorder)

    fig.savefig(f"{path}/{region.upper()}/{reference_system.upper()}/{filename}", bbox_inches='tight')
    _plt.close(fig)
    if notifications == 'on':
        print(f"{filename} saved to {path}/{region.upper()}")
        
        