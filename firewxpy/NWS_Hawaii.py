
'''
This file hosts all the plotting functions for the National Weather Service Forecast Graphics.

Each class hosts a variety of plotting functions to analyze a particular weather element. 

Classes in this file:
    1) Relative Humidity 
    2) Temperature

 This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS

'''

#### IMPORTS ####

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import metpy.calc as mpcalc
import numpy as np
import pandas as pd
import firewxpy.parsers as parsers
import firewxpy.geometry as geometry
import firewxpy.colormaps as colormaps
import firewxpy.settings as settings
import firewxpy.standard as standard
import os
import imageio
import firewxpy.dims as dims
import warnings
warnings.filterwarnings('ignore')

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from dateutil import tz
from matplotlib.patheffects import withStroke
from firewxpy.calc import scaling, unit_conversion, contouring
from firewxpy.utilities import file_functions
from firewxpy.data_access import NDFD_CONUS
from metpy.units import units

mpl.rcParams['font.weight'] = 'bold'

class relative_humidity:

    '''
    This class holds all the plotting functions for the National Weather Service Relative Humidity Forecasts:

    1) Poor Overnight Recovery Forecast 

    2) Excellent Overnight Recovery Forecast

    3) Maximum Relative Humidity Forecast

    4) Maximum Relative Humidity Trend Forecast

    5) Low Minimum Relative Humidity Forecast

    6) Minimum Relative Humidity Forecast

    7) Minimum Relative Humidity Trend Forecast


    '''

    def plot_poor_overnight_recovery_relative_humidity_forecast(poor_overnight_recovery_rh_threshold=60, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, aspect=30, tick=9, island=None):
    
        r'''
        This function plots the latest available NOAA/NWS Poor Overnight Recovery RH Forecast. 

        Required Arguments: None

        Optional Arguments: 1) poor_overnight_recovery_rh_threshold (Integer) -  Default = 30%. The relative humidity threshold for 
                               a poor overnight relative humidity recovery. This is the upper bound of values shaded. 
                               (i.e. a value of 30 means all values less than 30% get shaded).

                            2) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            3) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            4) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            5) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            6) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            7) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            8) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            9) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            10) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            11) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            12) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            13) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            14) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            15) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            16) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            17) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            18) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            19) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            20) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            21) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            22) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            23) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            24) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            25) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            26) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            27) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            28) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            29) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            30) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            31) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            32) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            35) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            36) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            37) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            38) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            39) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            40) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            41) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            42) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            43) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            44) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            45) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            46) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            47) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            48) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            49) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            50) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            51) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            52) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
        poor_overnight_recovery_rh_threshold = poor_overnight_recovery_rh_threshold
        file_path = file_path
        count_short = count_short
        count_extended = count_extended
        state = 'hi'
        island = island

        thresh = poor_overnight_recovery_rh_threshold + 1
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

        levels = np.arange(0, thresh, 1)
        if thresh > 31:
            labels = levels[::2]
        else:
            labels = levels

        cmap = colormaps.low_relative_humidity_colormap()

        reference_system = reference_system

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
    
        if file_path == None:
    
            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.maxrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)

    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False       
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
        
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        else:
            pass    
    
        try:

            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'maxrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            mask1 = (df1['maxrh'] <= poor_overnight_recovery_rh_threshold)
        
            df2 = vals[1]
            mask2 = (df2['maxrh'] <= poor_overnight_recovery_rh_threshold)    
        
            df3 = vals[2]
            mask3 = (df3['maxrh'] <= poor_overnight_recovery_rh_threshold)
            
            df4 = vals[3]
            mask4 = (df4['maxrh'] <= poor_overnight_recovery_rh_threshold)
            
            df5 = vals[4]
            mask5 = (df5['maxrh'] <= poor_overnight_recovery_rh_threshold)
            
            df6 = vals[5]
            mask6 = (df6['maxrh'] <= poor_overnight_recovery_rh_threshold)
        
            if test_7 == True:
                df7 = vals[6]
                mask7 = (df7['maxrh'] <= poor_overnight_recovery_rh_threshold)
            else:
                pass
    
            no_vals = False
        except Exception as e:
            no_vals = True
            
        files = count

        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()

        local_time, utc_time = standard.plot_creation_time()
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        ax1.set_title('National Weather Service Forecast [Night 1]\nPoor Overnight RH Recovery\n(Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')

        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=levels, cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)

        plot_lon, plot_lat = np.meshgrid(ds['longitude'][::decimate], ds['latitude'][::decimate])

    
        if show_sample_points == True and no_vals == False:

    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)

            
            stn1.plot_parameter('C', df1['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)

    
        else:
            pass  

        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        ax2.set_title('National Weather Service Forecast [Night 2]\nPoor Overnight RH Recovery\n(Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
     
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=levels, cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass   
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        ax3.set_title('National Weather Service Forecast [Night 3]\nPoor Overnight RH Recovery\n(Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')

        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=levels, cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass   
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        ax4.set_title('National Weather Service Forecast [Night 4]\nPoor Overnight RH Recovery\n(Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')

        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=levels, cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass   
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass


        ax5.set_title('National Weather Service Forecast [Night 5]\nPoor Overnight RH Recovery\n(Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')

        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=levels, cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass   
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax6.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax6.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax6.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass


        ax6.set_title('National Weather Service Forecast [Night 6]\nPoor Overnight RH Recovery\n(Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')

        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=levels, cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass   
    
        cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass

                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=levels, cmap=cmap, transform=datacrs, alpha=alpha, zorder=2)
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   

            ax7.set_title('National Weather Service Forecast [Night 7]\nPoor Overnight RH Recovery\n(Max RH <= ' +str(poor_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')

            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Poor Overnight Recovery', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Poor Overnight Recovery')
    
    
    def plot_excellent_overnight_recovery_relative_humidity_forecast(excellent_overnight_recovery_rh_threshold=80, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9):
    
        r'''
        This function plots the latest available NOAA/NWS Excellent Overnight Recovery RH Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) excellent_overnight_recovery_rh_threshold (Integer) -  Default = 80%. The relative humidity threshold for 
                               an excellent overnight relative humidity recovery. This is the lower bound of values shaded. 
                               (i.e. a value of 80 means all values greater than 80% get shaded).

                            2) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            3) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            4) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            5) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            6) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            7) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            8) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            9) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            10) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            11) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            12) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            13) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            14) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            15) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            16) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            17) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            18) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            19) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            20) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            21) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            22) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            23) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            24) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            25) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            26) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            27) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            28) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            29) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            30) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            31) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            32) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            35) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            36) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            37) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            38) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            39) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            40) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            41) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            42) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            43) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            44) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            45) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            46) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            47) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            48) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            49) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            50) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            51) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            52) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
    
        state_border_linewidth = state_border_linewidth
        excellent_overnight_recovery_rh_threshold = excellent_overnight_recovery_rh_threshold
        file_path = file_path
        count_short = count_short
        count_extended = count_extended
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
        cmap = colormaps.excellent_recovery_colormap()
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        props = dict(boxstyle='round', facecolor='wheat', alpha=1)
        state = 'hi'

        levels = np.arange(excellent_overnight_recovery_rh_threshold, 101, 1)
        if excellent_overnight_recovery_rh_threshold < 80:
            labels = levels[::2]
        else:
            labels = levels

        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        

        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
    
        if file_path == None:
    
            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.maxrh.bin')
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)     
    
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False       
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
        else:
            pass
    
        
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'maxrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
        
            df2 = vals[1] 
        
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]
        
        
            if test_7 == True:
                df7 = vals[6]
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
    
        files = count

        local_time, utc_time = standard.plot_creation_time()
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass


        ax1.set_title('National Weather Service Forecast [Night 1]\nExcellent Overnight RH Recovery\n(Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')

        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='max')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df1['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass     
    
        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass


        ax2.set_title('National Weather Service Forecast [Night 2]\nExcellent Overnight RH Recovery\n(Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='max')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass  
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass


        ax3.set_title('National Weather Service Forecast [Night 3]\nExcellent Overnight RH Recovery\n(Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='max')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass  
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass


        ax4.set_title('National Weather Service Forecast [Night 4]\nExcellent Overnight RH Recovery\n(Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='max')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass  
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass


        ax5.set_title('National Weather Service Forecast [Night 5]\nExcellent Overnight RH Recovery\n(Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='center')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='max')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass  
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax6.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax6.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax6.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass


        ax6.set_title('National Weather Service Forecast [Night 6]\nExcellent Overnight RH Recovery\n(Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='max')
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass  
    
        cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
            
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass


            ax7.set_title('National Weather Service Forecast [Night 7]\nExcellent Overnight RH Recovery\n(Max RH >= ' +str(excellent_overnight_recovery_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='max')
    
            if show_sample_points == True and no_vals == False:
        
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
        
                stn7.plot_parameter('C', df7['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
        
            else:
                pass  
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Excellent Overnight Recovery', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Excellent Overnight Recovery')
    
    
    def plot_maximum_relative_humidity_forecast(color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9):
    
        r'''
        This function plots the latest available NOAA/NWS Maximum RH Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            2) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            3) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            4) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            5) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            6) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            7) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            8) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            9) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            10) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            11) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            12) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            13) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            14) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            15) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            16) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            17) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            18) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            19) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            20) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            21) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            22) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            23) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            24) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            25) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            26) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            27) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            28) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            29) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            30) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            31) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            32) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            35) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            36) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            37) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            38) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            39) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            40) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            41) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            42) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            43) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            44) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            45) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            46) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            47) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            48) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            49) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            50) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            51) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
    
        file_path = file_path
        count_short = count_short
        count_extended = count_extended
        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
        cmap = colormaps.relative_humidity_colormap()

        state = 'hi'
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

        levels = np.arange(0, 102, 1)
        labels = levels[::4]

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
    
        if file_path == None:
    
            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.maxrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)
            
        if file_path != None:
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)    
    
        
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False       
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
    
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        
        else:
            pass    
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'maxrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
        
            df2 = vals[1] 
        
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]
        
            if test_7 == True:
                df7 = vals[6]
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
            
        files = count

        local_time, utc_time = standard.plot_creation_time()
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass


        ax1.set_title('National Weather Service Forecast [Night 1]\nMaximum Relative Humidity [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df1['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass     
    
        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, pad=0.02, shrink=color_table_shrink)
        cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

            
        ax2.set_title('National Weather Service Forecast [Night 2]\nMaximum Relative Humidity [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass     
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, pad=0.02, shrink=color_table_shrink)
        cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

            
        ax3.set_title('National Weather Service Forecast [Night 3]\nMaximum Relative Humidity [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass     
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, pad=0.02, shrink=color_table_shrink)
        cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

            
        ax4.set_title('National Weather Service Forecast [Night 4]\nMaximum Relative Humidity [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass     
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, pad=0.02, shrink=color_table_shrink)
        cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        
        ax5.set_title('National Weather Service Forecast [Night 5]\nMaximum Relative Humidity [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass     
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, pad=0.02, shrink=color_table_shrink)
        cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax6.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax6.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax6.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass


        ax6.set_title('National Weather Service Forecast [Night 6]\nMaximum Relative Humidity [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass     
    
        cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, pad=0.02, shrink=color_table_shrink)
        cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass

            if show_cwa_borders == True:
                ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass

            
            ax7.set_title('National Weather Service Forecast [Night 7]\nMaximum Relative Humidity [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
        
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
        
                stn7.plot_parameter('C', df7['maxrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
        
            else:
                pass     
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, pad=0.02, shrink=color_table_shrink)
            cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Maximum RH', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Maximum RH')
    
    
    
    def plot_maximum_relative_humidity_trend_forecast(color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9):
    
        r'''
        This function plots the latest available NOAA/NWS Maximum RH Trend Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            2) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            3) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            4) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            5) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            6) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            7) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            8) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            9) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            10) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            11) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            12) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            13) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            14) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            15) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            16) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            17) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            18) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            19) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            20) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            21) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            22) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            23) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            24) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            25) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            26) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            27) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            28) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            29) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            30) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            31) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            32) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            35) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            36) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            37) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            38) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            39) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            40) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            41) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            42) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            43) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            44) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            45) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            46) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            47) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            48) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            49) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            50) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            51) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
        file_path = file_path
        count_short = count_short
        count_extended = count_extended
        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
        cmap = colormaps.relative_humidity_change_colormap()
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

        state = 'hi'

        levels = np.arange(-50, 51, 1)
        labels = levels[::4]

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        

        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)

    
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
    
        if file_path == None:
    
            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.maxrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
            
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxrh.bin', 12, False, count_short, count_extended, directory_name)        
    
    
        diff1 = grb_2_vals - grb_1_vals
        diff2 = grb_3_vals - grb_2_vals
        diff3 = grb_4_vals - grb_3_vals
        diff4 = grb_5_vals - grb_4_vals
        diff5 = grb_6_vals - grb_5_vals
    
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False       
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
            diff6 = grb_7_vals - grb_6_vals
        else:
            pass
    
        try:    
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'maxrh', count, True, count_short, count_extended, discard)
        
            df1 = vals[0]
        
            df2 = vals[1] 
        
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]
        
            df2['diff'] = df2['maxrh'] - df1['maxrh']
            df3['diff'] = df3['maxrh'] - df2['maxrh']
            df4['diff'] = df4['maxrh'] - df3['maxrh']
            df5['diff'] = df5['maxrh'] - df4['maxrh']
            df6['diff'] = df6['maxrh'] - df5['maxrh']
        
            
            if test_7 == True:
                df7 = vals[6]
                df7['diff'] = df7['maxrh'] - df6['maxrh']
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
            
        files = count

        local_time, utc_time = standard.plot_creation_time()
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
    
        ax1.set_title('National Weather Service Forecast [Night 2]\nMaximum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=levels, cmap=cmap, transform=datacrs, zorder=2, extend='both', alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df2['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass     
    
        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar1.set_label(label="Maximum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
    
        ax2.set_title('National Weather Service Forecast [Night 3]\nMaximum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=levels, cmap=cmap, transform=datacrs, zorder=2, extend='both', alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df3['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass 
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar2.set_label(label="Maximum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
    
        ax3.set_title('National Weather Service Forecast [Night 4]\nMaximum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=levels, cmap=cmap, transform=datacrs, zorder=2, extend='both', alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df4['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass 
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar3.set_label(label="Maximum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
    
        ax4.set_title('National Weather Service Forecast [Night 5]\nMaximum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=levels, cmap=cmap, transform=datacrs, zorder=2, extend='both', alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df5['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass 
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar4.set_label(label="Maximum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
    
        ax5.set_title('National Weather Service Forecast [Night 6]\nMaximum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=levels, cmap=cmap, transform=datacrs, zorder=2, extend='both', alpha=alpha)
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df6['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass 
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar5.set_label(label="Maximum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax7.set_title('National Weather Service Forecast [Night 7]\nMaximum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=levels, cmap=cmap, transform=datacrs, zorder=2, extend='both', alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
        
                stn7 = mpplots.StationPlot(ax7, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
        
                stn7.plot_parameter('C', df7['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
        
            else:
                pass 
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar7.set_label(label="Maximum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)

        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Maximum RH Trend', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Maximum RH Trend')
    
        
    
    def plot_low_minimum_relative_humidity_forecast(low_minimum_rh_threshold=75, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9):
    
        r'''
        This function plots the latest available NOAA/NWS Low Minimum RH Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) low_minimum_rh_threshold (Integer) -  Default = 15%. The relative humidity threshold for 
                               a low minimum relative humidity. This is the upper bound of values shaded. 
                               (i.e. a value of 15 means all values less than 15% get shaded).

                            2) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            3) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            4) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            5) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            6) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            7) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            8) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            9) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            10) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            11) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            12) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            13) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            14) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            15) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            16) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            17) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            18) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            19) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            20) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            21) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            22) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            23) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            24) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            25) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            26) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            27) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            28) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            29) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            30) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            31) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            32) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            35) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            36) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            37) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            38) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            39) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            40) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            41) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            42) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            43) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            44) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            45) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            46) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            47) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            48) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            49) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            50) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            51) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            52) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
        low_minimum_rh_threshold = low_minimum_rh_threshold
        file_path = file_path  
        count_short = count_short
        count_extended = count_extended
        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

        thresh = low_minimum_rh_threshold + 1

        levels = np.arange(0, thresh, 1)
        labels = levels

        state = 'hi'
    
        cmap = colormaps.low_relative_humidity_colormap()
        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25

            
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)
    
    
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
        
        if file_path == None:
    
            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.minrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.minrh.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False       
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
    
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
            
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        else:
            pass
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'minrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
    
            df2 = vals[1] 
    
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]
    
            if test_7 == True:
                df7 = vals[6]
            else:
                pass
    
    
            no_vals = False
    
        except Exception as ee:
            try:
                vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'unknown', count, True, count_short, count_extended, discard)
                df1 = vals[0]
        
                df2 = vals[1]
        
                df3 = vals[2]
                
                df4 = vals[3]
        
                df5 = vals[4]
                
                df6 = vals[5]
        
        
                if test_7 == True:
                    df7 = vals[6]
                else:
                    pass
    
    
                no_vals = False
            except Exception as g:
                no_vals = True
            
        files = count

        local_time, utc_time = standard.plot_creation_time()    
        
        figs = [] 

        print("Creating Images - Please Wait...")
    
        try:
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass

    
            ax1.set_title('National Weather Service Forecast [Day 1]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn1.plot_parameter('C', df1['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass     
    
            cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax2.set_title('National Weather Service Forecast [Day 2]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn2.plot_parameter('C', df2['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
            
            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax3.set_title('National Weather Service Forecast [Day 3]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn3.plot_parameter('C', df3['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax4.set_title('National Weather Service Forecast [Day 4]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn4.plot_parameter('C', df4['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
            
            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax5.set_title('National Weather Service Forecast [Day 5]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn5.plot_parameter('C', df5['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax6.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax6.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax6.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax6.set_title('National Weather Service Forecast [Day 6]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn6.plot_parameter('C', df6['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
                
                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_gacc_borders == True:
                    ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass
    
                ax7.set_title('National Weather Service Forecast [Day 7]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
                
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
                if show_sample_points == True and no_vals == False:
        
                    stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
        
                    stn7.plot_parameter('C', df7['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
        
                else:
                    pass   
    
                cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
                cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
        except Exception as ff:
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax1.set_title('National Weather Service Forecast [Day 1]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn1.plot_parameter('C', df1['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass     
    
            cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
            
            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax2.set_title('National Weather Service Forecast [Day 2]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn2.plot_parameter('C', df2['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax3.set_title('National Weather Service Forecast [Day 3]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn3.plot_parameter('C', df3['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax4.set_title('National Weather Service Forecast [Day 4]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn4.plot_parameter('C', df4['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax5.set_title('National Weather Service Forecast [Day 5]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn5.plot_parameter('C', df5['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax6.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax6.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax6.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            ax6.set_title('National Weather Service Forecast [Day 6]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn6.plot_parameter('C', df6['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_gacc_borders == True:
                    ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass
    
                ax7.set_title('National Weather Service Forecast [Day 7]\nExceptionally Low Minimum RH\n(Min RH <= ' +str(low_minimum_rh_threshold) + '%)', fontsize=title_fontsize, fontweight='bold', loc='left')
                
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
                if show_sample_points == True and no_vals == False:
        
                    stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
        
                    stn7.plot_parameter('C', df7['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
        
                else:
                    pass   
    
                cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
                cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Low Minimum RH', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Low Minimum RH')
    
    
    def plot_minimum_relative_humidity_forecast(color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9):
    
        r'''
        This function plots the latest available NOAA/NWS Minimum RH Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            2) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            3) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            4) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            5) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            6) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            7) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            8) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            9) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            10) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            11) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            12) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            13) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            14) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            15) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            16) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            17) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            18) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            19) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            20) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            21) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            22) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            23) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            24) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            25) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            26) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            27) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            28) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            29) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            30) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            31) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            32) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            35) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            36) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            37) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            38) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            39) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            40) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            41) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            42) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            43) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            44) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            45) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            46) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            47) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            48) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            49) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            50) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            51) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
        file_path = file_path
        cmap = colormaps.relative_humidity_colormap()
        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

        state = 'hi'

        levels = np.arange(0, 102, 1)
        labels = levels[::4]
    
        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)
    
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
            
        if file_path == None:

            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.minrh.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.minrh.bin', 12, False, count_short, count_extended, directory_name)
    
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
        try:
            if grb_7_vals.all() != None:
                test_7 = True
        
        except Exception as e:
            test_7 = False    
        
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        else:
            pass
    
        try:

            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'minrh', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
    
            df2 = vals[1] 
    
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]   
    
            if test_7 == True:
    
                df7 = vals[6]
    
            else:
                pass
    
            no_vals = False
        except Exception as ee:
            try:
                vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'unknown', count, True, count_short, count_extended, discard)
                
                df1 = vals[0]
        
                df2 = vals[1]
        
                df3 = vals[2]
                
                df4 = vals[3]
        
                df5 = vals[4]
                
                df6 = vals[5]
           
        
                if test_7 == True:
        
                    df7 = vals[6]
        
                else:
                    pass
    
                no_vals = False
            except Exception as g:    
                no_vals = True
        
            
        files = count
        
        local_time, utc_time = standard.plot_creation_time()
    
        figs = [] 

        print("Creating Images - Please Wait...")
        
        try:
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass

            ax1.set_title('National Weather Service Forecast [Day 1]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn1.plot_parameter('C', df1['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass     
    
            cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
            
            ax2.set_title('National Weather Service Forecast [Day 2]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn2.plot_parameter('C', df2['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
                
            ax3.set_title('National Weather Service Forecast [Day 3]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn3.plot_parameter('C', df3['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
                
            ax4.set_title('National Weather Service Forecast [Day 4]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn4.plot_parameter('C', df4['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
                
            ax5.set_title('National Weather Service Forecast [Day 5]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn5.plot_parameter('C', df5['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax6.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax6.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax6.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
                
            ax6.set_title('National Weather Service Forecast [Day 6]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn6.plot_parameter('C', df6['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_gacc_borders == True:
                    ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass
                
                ax7.set_title('National Weather Service Forecast [Day 7]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
                
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
                if show_sample_points == True and no_vals == False:
        
                    stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
        
                    stn7.plot_parameter('C', df7['minrh'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
        
                else:
                    pass   
    
                cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
                cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
        except Exception as ff:
    
            fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig1.set_facecolor('aliceblue')
            fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
                
            ax1.set_title('National Weather Service Forecast [Day 1]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn1.plot_parameter('C', df1['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass     
    
            cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar1.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig2.set_facecolor('aliceblue')
            fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
                
            ax2.set_title('National Weather Service Forecast [Day 2]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn2.plot_parameter('C', df2['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar2.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig3.set_facecolor('aliceblue')
            fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
                
            ax3.set_title('National Weather Service Forecast [Day 3]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn3.plot_parameter('C', df3['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar3.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
            fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig4.set_facecolor('aliceblue')
            fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
                
            ax4.set_title('National Weather Service Forecast [Day 4]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn4.plot_parameter('C', df4['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar4.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig5.set_facecolor('aliceblue')
            fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
                
            ax5.set_title('National Weather Service Forecast [Day 5]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn5.plot_parameter('C', df5['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar5.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig6.set_facecolor('aliceblue')
            fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax6.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax6.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax6.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
                
            ax6.set_title('National Weather Service Forecast [Day 6]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
            if show_sample_points == True and no_vals == False:
    
                stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn6.plot_parameter('C', df6['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass   
    
            cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar6.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
    
            if files == 7:
    
                fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
                fig7.set_facecolor('aliceblue')
                fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

                ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
                ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
                ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
                if show_rivers == True:
                    ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
                if show_gacc_borders == True:
                    ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass
                
                ax7.set_title('National Weather Service Forecast [Day 7]\nMinimum Relative Humidity Forecast [%]', fontsize=title_fontsize, fontweight='bold', loc='left')
                
                ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                    
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha)
    
                if show_sample_points == True and no_vals == False:
        
                    stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
        
                    stn7.plot_parameter('C', df7['unknown'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
        
                else:
                    pass   
    
                cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
                cbar7.set_label(label="Relative Humidity (%)", fontsize=colorbar_fontsize, fontweight='bold')
            
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
                figs.append(fig7)
    
            else:
                figs.append(fig1)
                figs.append(fig2)
                figs.append(fig3)
                figs.append(fig4)
                figs.append(fig5)
                figs.append(fig6)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Minimum RH', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Minimum RH')
    
    
    
    def plot_minimum_relative_humidity_trend_forecast(color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9):
    
        r'''
        This function plots the latest available NOAA/NWS Minimum RH Trend Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            2) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            3) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            4) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            5) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            6) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            7) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            8) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            9) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            10) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            11) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            12) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            13) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            14) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            15) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            16) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            17) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            18) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            19) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            20) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            21) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            22) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            23) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            24) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            25) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            26) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            27) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            28) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            29) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            30) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            31) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            32) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            35) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            36) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            37) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            38) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            39) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            40) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            41) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            42) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            43) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            44) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            45) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            46) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            47) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            48) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            49) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            50) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            51) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
        
        file_path = file_path

        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()

        cmap = colormaps.relative_humidity_change_colormap()

        state = 'hi'
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

        levels = np.arange(-50, 51, 1)
        labels = levels[::4]

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        

        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)

    
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
            
        if file_path == None:

            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.minrh.bin')

            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.minrh.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False      
        
        diff1 = grb_2_vals - grb_1_vals
        diff2 = grb_3_vals - grb_2_vals
        diff3 = grb_4_vals - grb_3_vals
        diff4 = grb_5_vals - grb_4_vals
        diff5 = grb_6_vals - grb_5_vals
    
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
    
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)  
            
            diff6 = grb_7_vals - grb_6_vals
        else:
            pass
    
        
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'minrh', count, True, count_short, count_extended, discard)
            df1 = vals[0]
    
            df2 = vals[1] 
    
            df3 = vals[2]
            
            df4 = vals[3]
            
            df5 = vals[4]
            
            df6 = vals[5]
    
            df2['diff'] = df2['minrh'] - df1['minrh']
            df3['diff'] = df3['minrh'] - df2['minrh']
            df4['diff'] = df4['minrh'] - df3['minrh']
            df5['diff'] = df5['minrh'] - df4['minrh']
            df6['diff'] = df6['minrh'] - df5['minrh']
    
            if test_7 == True:
                df7 = vals[6]
                df7['diff'] = df7['minrh'] - df6['minrh']
            else:
                pass
        
            no_vals = False
        except Exception as ee:
            try:
                vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'unknown', count, True, count_short, count_extended, discard)
                df1 = vals[0]
        
                df2 = vals[1]
        
                df3 = vals[2]
                
                df4 = vals[3]
        
                df5 = vals[4]
                
                df6 = vals[5]
        
                diff1 = grb_2_vals - grb_1_vals
                diff2 = grb_3_vals - grb_2_vals
                diff3 = grb_4_vals - grb_3_vals
                diff4 = grb_5_vals - grb_4_vals
                diff5 = grb_6_vals - grb_5_vals
        
                df2['diff'] = df2['unknown'] - df1['unknown']
                df3['diff'] = df3['unknown'] - df2['unknown']
                df4['diff'] = df4['unknown'] - df3['unknown']
                df5['diff'] = df5['unknown'] - df4['unknown']
                df6['diff'] = df6['unknown'] - df5['unknown']
        
                if test_7 == True:
                    df7 = vals[6]
                    df7['diff'] = df7['unknown'] - df6['unknown']
                else:
                    pass
    
                no_vals = False
            except Exception as g:
                no_vals = True
            
        files = count

        local_time, utc_time = standard.plot_creation_time()
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        ax1.set_title('National Weather Service Forecast [Day 2]\nMinimum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df2['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass   
    
        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar1.set_label(label="Minimum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        ax2.set_title('National Weather Service Forecast [Day 3]\nMinimum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df3['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass   
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar2.set_label(label="Minimum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        ax3.set_title('National Weather Service Forecast [Day 4]\nMinimum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df4['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass   
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar3.set_label(label="Minimum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        ax4.set_title('National Weather Service Forecast [Day 5]\nMinimum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df5['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass   
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar4.set_label(label="Minimum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        ax5.set_title('National Weather Service Forecast [Day 6]\nMinimum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df6['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass   
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar5.set_label(label="Minimum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
            ax7.set_title('National Weather Service Forecast [Day 7]\nMinimum Relative Humidity Trend [Δ%]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=levels, cmap=cmap, transform=datacrs, zorder=2, alpha=alpha, extend='both')
    
            if show_sample_points == True and no_vals == False:
        
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
        
                stn7.plot_parameter('C', df7['diff'][::decimate], color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
        
            else:
                pass   
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar7.set_label(label="Minimum Relative Humidity Trend (Δ%)", fontsize=colorbar_fontsize, fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Minimum RH Trend', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Minimum RH Trend')

class temperature: 

    r'''
    This class holds all the plotting functions for the National Weather Service Temperature Forecasts:

    1) Extreme Heat Forecast

    2) Extremely Warm Low Temperature Forecast

    3) Frost/Freeze Forecast 

    4) Maximum Temperature Forecast

    5) Minimum Temperature Forecast

    6) Maximum Temperature Trend Forecast

    7) Minimum Temperature Trend Forecast

    '''


    def plot_extreme_heat_forecast(start_of_warm_season_month=4, end_of_warm_season_month=10, start_of_cool_season_month=11, end_of_cool_season_month=3, temp_scale_warm_start=100, temp_scale_warm_stop=120, temp_scale_cool_start=90, temp_scale_cool_stop=110, temp_scale_step=1, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9): 
    
        r'''
        This function plots the latest available NOAA/NWS Extreme Heat Forecast. 

        Required Arguments: None

        Optional Arguments: 1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

                            2) end_of_warm_season_month (Integer) - Default = 10 (October). The numeric value for the month the warm season ends. 

                            3) start_of_cool_season_month (Integer) - Default = 11 (November). The numeric value for the month the cool season begins. 

                            4) end_of_cool_season_month (Integer) - Default = 3 (March). The numeric value for the month the cool season ends.

                            5) temp_scale_warm_start (Integer) - Default = 100. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

                            6) temp_scale_warm_stop (Integer) - Default = 120. The top bound temperature value in Fahrenheit of the warm season temperature range.

                            7) temp_scale_cool_start (Integer) - Default = 90. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

                            8) temp_scale_cool_stop (Integer) - Default = 110. The top bound temperature value in Fahrenheit of the cool season temperature range. 

                            9) temp_scale_step (Integer) - Default = 1. The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                                                           (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

                            10) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            11) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            12) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            13) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            14) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            15) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            16) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            17) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            18) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            19) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            20) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            21) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            22) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            23) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            24) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            25) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            26) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            27) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            28) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            29) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            30) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            31) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            32) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            33) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            34) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            35) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            36) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            37) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            38) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            39) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            40) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            41) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            42) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            43) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            44) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            45) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            46) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            47) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            48) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            49) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            50) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            51) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            52) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            53) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            54) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            55) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            56) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            57) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            58) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            59) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            60) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
        file_path = file_path
        start_of_warm_season_month = start_of_warm_season_month
        end_of_warm_season_month = end_of_warm_season_month
        start_of_cool_season_month = start_of_cool_season_month
        end_of_cool_season_month = end_of_cool_season_month
        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        color_table_shrink = color_table_shrink
        title_fontsize = title_fontsize
        subplot_title_fontsize = subplot_title_fontsize 
        colorbar_fontsize = colorbar_fontsize
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position 
        signature_fontsize = signature_fontsize
        temp_scale_warm_start = temp_scale_warm_start
        temp_scale_warm_stop = temp_scale_warm_stop
        temp_scale_step = temp_scale_step
        temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
        temp_scale_cool_start = temp_scale_cool_start
        temp_scale_cool_stop = temp_scale_cool_stop
        temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
    
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

        state = 'hi'
    
        temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
        temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        

        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)
    
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
    
        if file_path == None:

            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.maxt.bin')

            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
        grb_1_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_1_vals)
        grb_2_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_2_vals)
        grb_3_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_3_vals)
        grb_4_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_4_vals)
        grb_5_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_5_vals)
        grb_6_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_6_vals)
        
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False       
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
            grb_7_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_7_vals)
        else:
            pass
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmax', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmax'])
        
            df2 = vals[1]
            df2['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmax'])         
        
            df3 = vals[2]
            df3['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmax'])
            
            df4 = vals[3]
            df4['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmax'])
        
            df5 = vals[4]
            df5['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmax'])
            
            df6 = vals[5]
            df6['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmax'])
    
            if test_7 == True:
                df7 = vals[6]
                df7['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmax'])
            else:
                pass
    
            no_vals = False
    
        except Exception as g:
            no_vals = True
            
        files = count

        local_time, utc_time = standard.plot_creation_time()

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            labels = temp_scale_warm
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            labels = temp_scale_cool
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax1.set_title("National Weather Service Forecast [Day 1]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax1.set_title("National Weather Service Forecast [Day 1]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df1['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
    
        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar1.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
            
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax2.set_title("National Weather Service Forecast [Day 2]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax2.set_title("National Weather Service Forecast [Day 2]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar2.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax3.set_title("National Weather Service Forecast [Day 3]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax3.set_title("National Weather Service Forecast [Day 3]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar3.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax4.set_title("National Weather Service Forecast [Day 4]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax4.set_title("National Weather Service Forecast [Day 4]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar4.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax5.set_title("National Weather Service Forecast [Day 5]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax5.set_title("National Weather Service Forecast [Day 5]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar5.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax6.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax6.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax6.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax6.set_title("National Weather Service Forecast [Day 6]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax6.set_title("National Weather Service Forecast [Day 6]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar6.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                ax7.set_title("National Weather Service Forecast [Day 7]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                ax7.set_title("National Weather Service Forecast [Day 7]\nExtreme Heat\n(Maximum Temperature >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tmaxf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar7.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Extreme Heat', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Extreme Heat')

    def plot_extremely_warm_low_temperature_forecast(start_of_warm_season_month=4, end_of_warm_season_month=10, start_of_cool_season_month=11, end_of_cool_season_month=3, temp_scale_warm_start=80, temp_scale_warm_stop=100, temp_scale_cool_start=80, temp_scale_cool_stop=100, temp_scale_step=1, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9): 
    
        r'''
        This function plots the latest available NOAA/NWS Extremely Warm Low Temperature Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

                            2) end_of_warm_season_month (Integer) - Default = 10 (October). The numeric value for the month the warm season ends. 

                            3) start_of_cool_season_month (Integer) - Default = 11 (November). The numeric value for the month the cool season begins. 

                            4) end_of_cool_season_month (Integer) - Default = 3 (March). The numeric value for the month the cool season ends.

                            5) temp_scale_warm_start (Integer) - Default = 70. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

                            6) temp_scale_warm_stop (Integer) - Default = 90. The top bound temperature value in Fahrenheit of the warm season temperature range.

                            7) temp_scale_cool_start (Integer) - Default = 60. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

                            8) temp_scale_cool_stop (Integer) - Default = 80. The top bound temperature value in Fahrenheit of the cool season temperature range. 

                            9) temp_scale_step (Integer) - Default = 1. The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                                                           (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

                            10) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            11) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            12) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            13) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            14) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            15) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            16) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            17) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            18) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            19) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            20) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            21) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            22) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            23) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            24) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            25) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            26) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            27) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            28) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            29) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            30) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            31) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            32) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            33) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            34) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            35) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            36) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            37) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            38) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            39) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            40) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            41) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            42) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            43) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            44) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            45) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            46) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            47) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            48) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            49) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            50) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            51) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            52) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            53) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            54) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            55) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            56) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            57) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            58) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            59) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            60) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
    
        start_of_warm_season_month = start_of_warm_season_month
        end_of_warm_season_month = end_of_warm_season_month
        start_of_cool_season_month = start_of_cool_season_month
        end_of_cool_season_month = end_of_cool_season_month
        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        color_table_shrink = color_table_shrink
        title_fontsize = title_fontsize
        subplot_title_fontsize = subplot_title_fontsize 
        colorbar_fontsize = colorbar_fontsize
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position 
        signature_fontsize = signature_fontsize
        temp_scale_warm_start = temp_scale_warm_start
        temp_scale_warm_stop = temp_scale_warm_stop
        temp_scale_step = temp_scale_step
        temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
        temp_scale_cool_start = temp_scale_cool_start
        temp_scale_cool_stop = temp_scale_cool_stop
        temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
    
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
        state = 'hi'
        ds = data_array

        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    
        temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
        temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        

        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)
    
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
    
        if file_path == None:

            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.mint.bin')

            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
        grb_1_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_1_vals)
        grb_2_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_2_vals)
        grb_3_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_3_vals)
        grb_4_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_4_vals)
        grb_5_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_5_vals)
        grb_6_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_6_vals)
        
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False       
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
            grb_7_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_7_vals)
        else:
            pass
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmin', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmin'])
        
            df2 = vals[1]
            df2['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmin'])         
        
            df3 = vals[2]
            df3['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmin'])
            
            df4 = vals[3]
            df4['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmin'])
        
            df5 = vals[4]
            df5['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmin'])
            
            df6 = vals[5]
            df6['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmin'])
    
            if test_7 == True:
                df7 = vals[6]
                df7['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmin'])
            else:
                pass
    
            no_vals = False
    
        except Exception as g:
            no_vals = True
            
        files = count

        local_time, utc_time = standard.plot_creation_time()

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            labels = temp_scale_warm
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            labels = temp_scale_cool
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax1.set_title("National Weather Service Forecast [Night 1]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax1.set_title("National Weather Service Forecast [Night 1]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df1['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
    
        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax2.set_title("National Weather Service Forecast [Night 2]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax2.set_title("National Weather Service Forecast [Night 2]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax3.set_title("National Weather Service Forecast [Night 3]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax3.set_title("National Weather Service Forecast [Night 3]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax4.set_title("National Weather Service Forecast [Night 4]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax4.set_title("National Weather Service Forecast [Night 4]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax5.set_title("National Weather Service Forecast [Night 5]\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax5.set_title("National Weather Service Forecast [Night 5]\nExtremely Warm Low Temperatures (Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax6.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax6.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax6.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax6.set_title("National Weather Service Forecast [Night 6]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax6.set_title("National Weather Service Forecast [Night 6]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
        cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=2)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=2)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=2)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                ax7.set_title("National Weather Service Forecast [Night 7]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_warm_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                ax7.set_title("National Weather Service Forecast [Night 7]\nExtremely Warm Low Temperatures\n(Min T >= " +str(temp_scale_cool_start)+ " (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tminf'][::decimate], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap='hot', alpha=alpha, zorder=2, transform=datacrs, extend='max')
    
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar7.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Warm Min T', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Warm Min T')
    
    def plot_frost_freeze_forecast(temperature_bottom_bound=-10, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9): 
    
        r'''
        This function plots the latest available NOAA/NWS Frost/Freeze Forecast. 

        Required Arguments: None

        Optional Arguments: 1) temperature_bottom_bound (Integer) - Default = -10. The temperature value in Fahrenheit for the bottom bound of the temperature scale. 
                                                                    This value must be less than 32.  
        
                            2) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            3) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            4) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            5) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            6) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            7) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            8) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            9) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            10) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            11) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            12) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            13) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            14) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            15) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            16) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            17) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            18) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            19) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            20) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            21) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            22) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            23) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            24) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            25) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            26) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            27) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            28) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            29) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            30) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            31) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            32) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            35) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            36) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            37) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            38) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            39) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            40) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            41) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            42) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            43) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            44) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            45) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            46) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            47) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            48) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            49) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            50) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            51) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            51) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
        
        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        color_table_shrink = color_table_shrink
        title_fontsize = title_fontsize
        subplot_title_fontsize = subplot_title_fontsize 
        colorbar_fontsize = colorbar_fontsize
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position 
        signature_fontsize = signature_fontsize
        temperature_bottom_bound = temperature_bottom_bound
        
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha
        state = 'hi'

        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    
        cmap = colormaps.cool_temperatures_colormap()
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        levels = np.arange(temperature_bottom_bound, 33, 1)
        labels = levels[::2]
    
        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        

        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)
    
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
    
        if file_path == None:

            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.mint.bin')

            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
        grb_1_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_1_vals)
        grb_2_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_2_vals)
        grb_3_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_3_vals)
        grb_4_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_4_vals)
        grb_5_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_5_vals)
        grb_6_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_6_vals)
    
    
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False       
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)    
    
            grb_7_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_7_vals)
        else:
            pass
            
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmin', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmin'])
        
            df2 = vals[1]
            df2['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmin'])
        
            df3 = vals[2]
            df3['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmin'])
            
            df4 = vals[3]
            df4['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmin'])
            
            df5 = vals[4]
            df5['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmin'])
            
            df6 = vals[5]
            df6['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmin'])
    
    
            if test_7 == True:
                df7 = vals[6]
                df7['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmin'])
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
            
        files = count

        local_time, utc_time = standard.plot_creation_time()
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax1.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax1.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax1.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        ax1.set_title("National Weather Service Forecast [Night 1]\nFreeze Areas\n(Minimum Temperature <= 32 (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=levels, cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df1['tminf'][::decimate], color='orange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        ax2.set_title("National Weather Service Forecast [Night 2]\nFreeze Areas\n(Minimum Temperature <= 32 (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=levels, cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['tminf'][::decimate], color='orange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax3.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax3.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax3.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        ax3.set_title("National Weather Service Forecast [Night 3]\nFreeze Areas\n(Minimum Temperature <= 32 (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=levels, cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['tminf'][::decimate], color='orange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax4.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax4.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax4.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        ax4.set_title("National Weather Service Forecast [Night 4]\nFreeze Areas\n(Minimum Temperature <= 32 (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=levels, cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['tminf'][::decimate], color='orange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        ax5.set_title("National Weather Service Forecast [Night 5]\nFreeze Areas\n(Minimum Temperature <= 32 (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=levels, cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['tminf'][::decimate], color='orange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax6.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax6.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax6.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        ax6.set_title("National Weather Service Forecast [Night 6]\nFreeze Areas\n(Minimum Temperature <= 32 (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=levels, cmap=cmap , transform=datacrs, extend='min')
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['tminf'][::decimate], color='orange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax7.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax7.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax7.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass

            ax7.set_title("National Weather Service Forecast [Night 7]\nFreeze Areas\n(Minimum Temperature <= 32 (\N{DEGREE SIGN}F))", fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
            cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=levels, cmap=cmap , transform=datacrs, extend='min')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tminf'][::decimate], color='orange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar7.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Frost Freeze', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Frost Freeze')
    
    
    def plot_maximum_temperature_forecast(start_of_warm_season_month=4, end_of_warm_season_month=10, start_of_cool_season_month=11, end_of_cool_season_month=3, temp_scale_warm_start=50, temp_scale_warm_stop=90, temp_scale_cool_start=50, temp_scale_cool_stop=90, temp_scale_step=1, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9): 
    
        r'''
        This function plots the latest available NOAA/NWS Maximum Temperature Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

                            2) end_of_warm_season_month (Integer) - Default = 10 (October). The numeric value for the month the warm season ends. 

                            3) start_of_cool_season_month (Integer) - Default = 11 (November). The numeric value for the month the cool season begins. 

                            4) end_of_cool_season_month (Integer) - Default = 3 (March). The numeric value for the month the cool season ends.

                            5) temp_scale_warm_start (Integer) - Default = 50. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

                            6) temp_scale_warm_stop (Integer) - Default = 110. The top bound temperature value in Fahrenheit of the warm season temperature range.

                            7) temp_scale_cool_start (Integer) - Default = 10. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

                            8) temp_scale_cool_stop (Integer) - Default = 80. The top bound temperature value in Fahrenheit of the cool season temperature range. 

                            9) temp_scale_step (Integer) - Default = 1. The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                                                           (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

                            10) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            11) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            12) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            13) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            14) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            15) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            16) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            17) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            18) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            19) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            20) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            21) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            22) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            23) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            24) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            25) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            26) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            27) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            28) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            29) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            30) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            31) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            32) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            33) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            34) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            35) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            36) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            37) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            38) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            39) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            40) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            41) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            42) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            43) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            44) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            45) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            46) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            47) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            48) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            49) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            50) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            51) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            52) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            53) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            54) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            55) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            56) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            57) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            58) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            59) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            60) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
        
        start_of_warm_season_month = start_of_warm_season_month
        end_of_warm_season_month = end_of_warm_season_month
        start_of_cool_season_month = start_of_cool_season_month
        end_of_cool_season_month = end_of_cool_season_month
        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        color_table_shrink = color_table_shrink
        title_fontsize = title_fontsize
        subplot_title_fontsize = subplot_title_fontsize 
        colorbar_fontsize = colorbar_fontsize
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position 
        signature_fontsize = signature_fontsize
        temp_scale_warm_start = temp_scale_warm_start
        temp_scale_warm_stop = temp_scale_warm_stop
        temp_scale_step = temp_scale_step
        temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
        temp_scale_cool_start = temp_scale_cool_start
        temp_scale_cool_stop = temp_scale_cool_stop
        temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
    
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha

        props = dict(boxstyle='round', facecolor='wheat', alpha=1)
    
        cmap = colormaps.temperature_colormap()
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        state = 'hi'
    
        temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
        temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
    
        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        

        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)
    
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
    
        if file_path == None:

            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.maxt.bin')

            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
        grb_1_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_1_vals)
        grb_2_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_2_vals)
        grb_3_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_3_vals)
        grb_4_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_4_vals)
        grb_5_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_5_vals)
        grb_6_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_6_vals)
        
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False       
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
            grb_7_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_7_vals)
        else:
            pass
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmax', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmax'])
        
            df2 = vals[1]
            df2['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmax'])         
        
            df3 = vals[2]
            df3['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmax'])
            
            df4 = vals[3]
            df4['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmax'])
        
            df5 = vals[4]
            df5['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmax'])
            
            df6 = vals[5]
            df6['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmax'])
    
            if test_7 == True:
                df7 = vals[6]
                df7['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmax'])
            else:
                pass
            
            no_vals = False
    
        except Exception as g:
            no_vals = True
            
        files = count

        local_time, utc_time = standard.plot_creation_time()

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            labels = temp_scale_warm[::5]
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            labels = temp_scale_cool[::5]
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax1.set_title("National Weather Service Forecast [Day 1]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax1.set_title("National Weather Service Forecast [Day 1]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
            
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
        
            stn1.plot_parameter('C', df1['tmaxf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar1.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax2.set_title("National Weather Service Forecast [Day 2]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax2.set_title("National Weather Service Forecast [Day 2]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
            
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['tmaxf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar2.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax3.set_title("National Weather Service Forecast [Day 3]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax3.set_title("National Weather Service Forecast [Day 3]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
            
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['tmaxf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar3.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax4.set_title("National Weather Service Forecast [Day 4]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax4.set_title("National Weather Service Forecast [Day 4]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
            
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['tmaxf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar4.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax5.set_title("National Weather Service Forecast [Day 5]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax5.set_title("National Weather Service Forecast [Day 5]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
            
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['tmaxf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar5.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax6.set_title("National Weather Service Forecast [Day 6]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax6.set_title("National Weather Service Forecast [Day 6]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
            
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['tmaxf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar6.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass

            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                ax7.set_title("National Weather Service Forecast [Day 7]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
        
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                ax7.set_title("National Weather Service Forecast [Day 7]\nMaximum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
                
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tmaxf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar7.set_label(label="Maximum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Max T', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Max T')
    
    def plot_minimum_temperature_forecast(start_of_warm_season_month=4, end_of_warm_season_month=10, start_of_cool_season_month=11, end_of_cool_season_month=3, temp_scale_warm_start=40, temp_scale_warm_stop=70, temp_scale_cool_start=40, temp_scale_cool_stop=70, temp_scale_step=1, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9): 
    
        r'''
        This function plots the latest available NOAA/NWS Minimum Temperature Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

                            2) end_of_warm_season_month (Integer) - Default = 10 (October). The numeric value for the month the warm season ends. 

                            3) start_of_cool_season_month (Integer) - Default = 11 (November). The numeric value for the month the cool season begins. 

                            4) end_of_cool_season_month (Integer) - Default = 3 (March). The numeric value for the month the cool season ends.

                            5) temp_scale_warm_start (Integer) - Default = 30. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

                            6) temp_scale_warm_stop (Integer) - Default = 90. The top bound temperature value in Fahrenheit of the warm season temperature range.

                            7) temp_scale_cool_start (Integer) - Default = -10. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

                            8) temp_scale_cool_stop (Integer) - Default = 60. The top bound temperature value in Fahrenheit of the cool season temperature range. 

                            9) temp_scale_step (Integer) - Default = 1. The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                                                           (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

                            10) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            11) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            12) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            13) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            14) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            15) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            16) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            17) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            18) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            19) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            20) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            21) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            22) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            23) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            24) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            25) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            26) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            27) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            28) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            29) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            30) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            31) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            32) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            33) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            34) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            35) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            36) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            37) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            38) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            39) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            40) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            41) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            42) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            43) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            44) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            45) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            46) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            47) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            48) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            49) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            50) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            51) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            52) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            53) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            54) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            55) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            56) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            57) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            58) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            59) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            60) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
        
        start_of_warm_season_month = start_of_warm_season_month
        end_of_warm_season_month = end_of_warm_season_month
        start_of_cool_season_month = start_of_cool_season_month
        end_of_cool_season_month = end_of_cool_season_month
        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        color_table_shrink = color_table_shrink
        title_fontsize = title_fontsize
        subplot_title_fontsize = subplot_title_fontsize 
        colorbar_fontsize = colorbar_fontsize
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position 
        signature_fontsize = signature_fontsize
        temp_scale_warm_start = temp_scale_warm_start
        temp_scale_warm_stop = temp_scale_warm_stop
        temp_scale_step = temp_scale_step
        temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
        temp_scale_cool_start = temp_scale_cool_start
        temp_scale_cool_stop = temp_scale_cool_stop
        temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
    
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha

        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

        state = 'hi'
    
        cmap = colormaps.temperature_colormap()
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
        temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
    
    
        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        

        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)
    
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
    
        if file_path == None:

            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.mint.bin')

            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
    
        grb_1_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_1_vals)
        grb_2_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_2_vals)
        grb_3_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_3_vals)
        grb_4_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_4_vals)
        grb_5_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_5_vals)
        grb_6_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_6_vals)
        
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False       
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
    
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
    
            grb_7_vals = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(grb_7_vals)
        else:
            pass
    
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmin', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmin'])
        
            df2 = vals[1]
            df2['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmin'])         
        
            df3 = vals[2]
            df3['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmin'])
            
            df4 = vals[3]
            df4['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmin'])
        
            df5 = vals[4]
            df5['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmin'])
            
            df6 = vals[5]
            df6['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmin'])
    
            if test_7 == True:
                df7 = vals[6]
                df7['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmin'])
            else:
                pass
    
            no_vals = False
    
        except Exception as g:
            no_vals = True
            
        files = count

        local_time, utc_time = standard.plot_creation_time()

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            labels = temp_scale_warm[::5]
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            labels = temp_scale_cool[::5]
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax1.set_title("National Weather Service Forecast [Night 1]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax1.set_title("National Weather Service Forecast [Night 1]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df1['longitude'][::decimate], df1['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df1['tminf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar1.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax2.set_title("National Weather Service Forecast [Night 2]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax2.set_title("National Weather Service Forecast [Night 2]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df2['tminf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar2.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax3= fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax3.set_title("National Weather Service Forecast [Night 3]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax3.set_title("National Weather Service Forecast [Night 3]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df3['tminf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar3.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax4.set_title("National Weather Service Forecast [Night 4]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax4.set_title("National Weather Service Forecast [Night 4]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df4['tminf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar4.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax5.set_title("National Weather Service Forecast [Night 5]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax5.set_title("National Weather Service Forecast [Night 5]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df5['tminf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar5.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig6.set_facecolor('aliceblue')
        fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            ax6.set_title("National Weather Service Forecast [Night 6]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            ax6.set_title("National Weather Service Forecast [Night 6]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
            cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn6 = mpplots.StationPlot(ax6, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn6.plot_parameter('C', df6['tminf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar6 = fig6.colorbar(cs6, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar6.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=3)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                ax7.set_title("National Weather Service Forecast [Night 7]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
        
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                ax7.set_title("National Weather Service Forecast [Night 7]\nMinimum Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
    
            if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_warm, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
            if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=temp_scale_cool, cmap=cmap, alpha=alpha, transform=datacrs, extend='both')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tminf'][::decimate], color='green', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar7.set_label(label="Minimum Temperature (\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig6)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Min T', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Min T')
    
    
    def plot_minimum_temperature_trend_forecast(color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9):
    
        r'''
        This function plots the latest available NOAA/NWS Minimum Temperature Trend Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            2) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            3) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            4) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            5) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            6) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            7) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            8) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            9) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            10) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            11) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            12) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            13) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            14) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            15) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            16) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            17) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            18) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            19) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            20) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            21) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            22) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            23) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            24) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            25) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            26) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            27) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            28) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            29) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            30) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            31) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            32) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            35) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            36) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            37) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            38) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            39) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            40) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            41) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            42) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            43) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            44) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            45) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            46) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            47) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            48) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            49) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            50) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            51) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
    
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha

        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

        state = 'hi'

        levels = np.arange(-10, 11, 1)
        labels = levels[::2]
    
        cmap = colormaps.temperature_change_colormap()
        
        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        

        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)
    
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
    
        if file_path == None:

            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.mint.bin')
                    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.mint.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)
    
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False      
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)    
    
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
            
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        else:
            pass
    
    
        diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
        diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
        diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
        diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
        diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
        if test_7 == True:
            diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
        else:
            pass
    
        
        try:
            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmin', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmin'])
            
            df2 = vals[1]
            df2['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmin'])
            df2['tdiff'] = df2['tminf'] - df1['tminf']
            
            df3 = vals[2]
            df3['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmin'])
            df3['tdiff'] = df3['tminf'] - df2['tminf']        
            
            df4 = vals[3]
            df4['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmin'])
            df4['tdiff'] = df4['tminf'] - df3['tminf']
            
            df5 = vals[4]
            df5['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmin'])
            df5['tdiff'] = df5['tminf'] - df4['tminf']
            
            df6 = vals[5]
            df6['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmin'])
            df6['tdiff'] = df6['tminf'] - df5['tminf']
    
            if test_7 == True:
                df7 = vals[6]
                df7['tminf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmin'])
                df7['tdiff'] = df7['tminf'] - df6['tminf']
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
    
        files = count

        local_time, utc_time = standard.plot_creation_time()
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
    
        ax1.set_title('National Weather Service Forecast [Night 2]\nMinimum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df2['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar1.set_label(label="Minimum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
    
        ax2.set_title('National Weather Service Forecast [Night 3]\nMinimum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df3['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar2.set_label(label="Minimum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
    
        ax3.set_title('National Weather Service Forecast [Night 4]\nMinimum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df4['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar3.set_label(label="Minimum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
    
        ax4.set_title('National Weather Service Forecast [Night 5]\nMinimum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df5['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar4.set_label(label="Minimum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
        
        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
    
        ax5.set_title('National Weather Service Forecast [Night 6]\nMinimum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df6['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar5.set_label(label="Minimum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
    
            ax7.set_title('National Weather Service Forecast [Night 7]\nMinimum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar7.set_label(label="Minimum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Min T Trend', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Min T Trend')
    
    
    def plot_maximum_temperature_trend_forecast(color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=10, alpha=0.5, file_path=None, data_array=None, count_short=None, count_extended=None, island=None, aspect=30, tick=9):
    
        r'''
        This function plots the latest available NOAA/NWS Maximum Temperature Trend Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            2) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 

                            3) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 

                            4) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.

                            5) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            6) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            7) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            8) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            9) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            10) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            11) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            12) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            13) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            14) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            15) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
                                wishes to use a reference system not on this list, please see items 17-23. 
                                Reference Systems: 1) 'States & Counties'
                                                   2) 'States Only'
                                                   3) 'GACC Only'
                                                   4) 'GACC & PSA'
                                                   5) 'CWA Only'
                                                   6) 'NWS CWAs & NWS Public Zones'
                                                   7) 'NWS CWAs & NWS Fire Weather Zones'
                                                   8) 'NWS CWAs & Counties'
                                                   9) 'GACC & PSA & NWS Fire Weather Zones'
                                                   10) 'GACC & PSA & NWS Public Zones'
                                                   11) 'GACC & PSA & NWS CWA'
                                                   12) 'GACC & PSA & Counties'
                                                   13) 'GACC & Counties'
                                                   
    
                            16) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            17) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            18) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            19) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            20) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            21) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            22) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            23) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            24) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            25) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            26) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            27) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            28) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            29) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            30) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            31) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            32) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            35) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            36) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            37) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            38) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            39) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            40) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            41) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            42) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
                                This setting is to be edited if the user wishes to make a plot with custom boundaries. For the generic 
                                state and/or gacc boundary plots, the correct directory name is automatically returned from the settings 
                                module. Default setting is CONUS. 
                                
                                Here is the list of abbreviations for other directory names if the user wishes to change this setting: 

                                CONUS: 'CONUS' or 'US' or 'USA' or 'conus' or 'us' or 'usa'
                                Central Great Lakes: 'Central Great Lakes' or 'CGL' or 'central great lakes' or 'cgl'
                                Central Mississippi Valley: 'Central Mississippi Valley'  'central mississippi valley'  'CMV'  'cmv'
                                Central Plains: 'Central Plains'  'central plains'  'CP'  'cp'
                                Central Rockies: 'Central Rockies'  'central rockies'  'CR'  'cr'
                                Eastern Great Lakes: 'Eastern Great Lakes'  'eastern great lakes'  'EGL'  'egl'
                                Mid Atlantic: 'Mid Atlantic'  'Mid-Atlantic'  'mid atlantic'  'mid-atlantic'  'ma'  'Mid Atl'  'mid atl'  'Mid-Atl'  'mid-atl'
                                Northeast: 'Northeast'  'northeast'  'neast'  'NE'  'ne'  'NEAST'  'Neast'
                                Alaska: 'Alaska'  'AK'  'ak'  'alaska'
                                Guam: 'GUAM'  'Guam'  'guam'  'GM'  'gm'
                                Hawaii: 'Hawaii'  'HAWAII'  'HI'  'hi'
                                Northern Hemisphere: 'Northern Hemisphere'  'NHemisphere'  'northern hemisphere'  'nhemisphere'  'NH'  'nh'
                                North Pacific Ocean: 'North Pacific Ocean'  'NORTH PACIFIC OCEAN'  'north pacific ocean'  'npo'  'NPO'
                                Northern Plains: 'Northern Plains'  'NORTHERN PLAINS'  'northern plains'  'NP'  'np'  'NPLAINS'  'nplains'
                                Northern Rockies: 'Northern Rockies'  'northern rockies'  'NR'  'nr'
                                Oceanic: 'Oceanic'  'OCEANIC'  'oceanic'  'o'  'O'
                                Pacific Northwest: 'Pacific Northwest'  'PACIFIC NORTHWEST'  'pacific northwest'  'PNW'  'pnw'  'PACNW'  'pacnw'
                                Pacific Southwest: 'Pacific Southwest'  'PACIFIC SOUTHWEST'  'pacific southwest'  'PSW'  'psw'  'PACSW'  'pacsw'
                                Puerto Rico: 'Puerto Rico'  'PUERTO RICO'  'puerto rico'  'PR'  'pr'
                                Southeast: 'Southeast'  'SOUTHEAST'  'southeast'  'SEAST'  'seast'  'SE'  'se'
                                Southern Mississippi Valley: 'Southern Mississippi Valley'  'southern mississippi valley'  'SMV'  'smv'
                                Southern Plains: 'Southern Plains'  'SOUTHERN PLAINS'  'southern plains'  'SPLAINS'  'splains'  'SP'  'sp'
                                Southern Rockies: 'Southern Rockies'  'southern rockies'  'SR'  'sr'
                                Upper Mississippi Valley: 'Upper Mississippi Valley'  'upper mississippi valley'  'UMV'  'umv'

                            43) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            44) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
                                This setting is only to be changed if the user wants to limit the amount of downloads from the 
                                NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
                                if the user wishes to download the data outside of this function. 

                            45) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            46) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            47) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
                                sample points to appear in good order. Example: A value of 300 plots the sample point for one row
                                of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
                                Lower values equal more sample points which are less spaced apart. The default value is None. If
                                the default value is selected, the decimation is scaled automatically, however if the user wishes 
                                to change the spacing of the sample points, then the user must edit this value. 

                            48) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            49) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
                                If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
                                None and the gacc_region variable must be set to one of the acceptable abbreviations. 

                                Here is a list of acceptable gacc_region abbreviations:

                                South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
                                North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
                                Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
                                Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
                                Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
                                Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
                                Southern: 'SACC' or 'sacc' or 'SE' or 'se'
                                Eastern: 'EACC' or 'eacc' or 'E' or 'e'
                                Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
                                Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

                            50) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            51) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
        '''
        
        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        psa_border_linewidth = psa_border_linewidth
        state_border_linestyle = state_border_linestyle
        county_border_linestyle = county_border_linestyle
        gacc_border_linestyle = gacc_border_linestyle
        psa_border_linestyle = psa_border_linestyle
        show_sample_points = show_sample_points
        sample_point_fontsize = sample_point_fontsize
        alpha = alpha

        props = dict(boxstyle='round', facecolor='wheat', alpha=1)

        levels = np.arange(-10, 11, 1)
        labels = levels[::2]

        state = 'hi'
    
        cmap = colormaps.temperature_change_colormap()
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
    
        reference_system = reference_system
        mapcrs = ccrs.PlateCarree()
        datacrs = ccrs.PlateCarree()

        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones

        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                nws_firewx_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                nws_public_zones_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                cwa_border_linewidth=0.25
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    psa_border_linewidth=0.5
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                county_border_linewidth=0.25
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                    county_border_linewidth=0.25
        
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'nws', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        western_bound, eastern_bound, southern_bound, northern_bound, decimate = dims.hawaiian_islands_coords(island)
    
    
        PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
        
        GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

        CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

        FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

        PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

        directory_name = settings.check_NDFD_directory_name(directory_name)
        ds = data_array
    
        if file_path == None:

            grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.maxt.bin')

            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.maxt.bin', 12, False, count_short, count_extended, directory_name)
    
        if file_path != None:
    
            grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 12, False, count_short, count_extended, directory_name)

    
        try:
            if grb_7_vals.all() != None:
                test_7 = True
    
        except Exception as e:
            test_7 = False      
    
        grb_1_start = grb_1_start.replace(tzinfo=from_zone)
        grb_1_start = grb_1_start.astimezone(to_zone)
        grb_2_start = grb_2_start.replace(tzinfo=from_zone)
        grb_2_start = grb_2_start.astimezone(to_zone)
        grb_3_start = grb_3_start.replace(tzinfo=from_zone)
        grb_3_start = grb_3_start.astimezone(to_zone)
        grb_4_start = grb_4_start.replace(tzinfo=from_zone)
        grb_4_start = grb_4_start.astimezone(to_zone)
        grb_5_start = grb_5_start.replace(tzinfo=from_zone)
        grb_5_start = grb_5_start.astimezone(to_zone)
        grb_6_start = grb_6_start.replace(tzinfo=from_zone)
        grb_6_start = grb_6_start.astimezone(to_zone)
    
        grb_1_end = grb_1_end.replace(tzinfo=from_zone)
        grb_1_end = grb_1_end.astimezone(to_zone)
        grb_2_end = grb_2_end.replace(tzinfo=from_zone)
        grb_2_end = grb_2_end.astimezone(to_zone)
        grb_3_end = grb_3_end.replace(tzinfo=from_zone)
        grb_3_end = grb_3_end.astimezone(to_zone)
        grb_4_end = grb_4_end.replace(tzinfo=from_zone)
        grb_4_end = grb_4_end.astimezone(to_zone)
        grb_5_end = grb_5_end.replace(tzinfo=from_zone)
        grb_5_end = grb_5_end.astimezone(to_zone)
        grb_6_end = grb_6_end.replace(tzinfo=from_zone)
        grb_6_end = grb_6_end.astimezone(to_zone)    
    
        if test_7 == True:
            grb_7_start = grb_7_start.replace(tzinfo=from_zone)
            grb_7_start = grb_7_start.astimezone(to_zone)
            
            grb_7_end = grb_7_end.replace(tzinfo=from_zone)
            grb_7_end = grb_7_end.astimezone(to_zone)
        else:
            pass
    
    
        diff1 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_2_vals - grb_1_vals)
        diff2 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_3_vals - grb_2_vals)
        diff3 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_4_vals - grb_3_vals)
        diff4 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_5_vals - grb_4_vals)
        diff5 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_6_vals - grb_5_vals)
        if test_7 == True:
            diff6 = unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(grb_7_vals - grb_6_vals)
        else:
            pass
    
        
        try:

            vals = parsers.checks.parse_NWS_GRIB_data_array(ds, 'tmax', count, True, count_short, count_extended, discard)
            
            df1 = vals[0]
            df1['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df1['tmax'])
            
            df2 = vals[1]
            df2['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df2['tmax'])
            df2['tdiff'] = df2['tmaxf'] - df1['tmaxf']
            
            df3 = vals[2]
            df3['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df3['tmax'])
            df3['tdiff'] = df3['tmaxf'] - df2['tmaxf']        
            
            df4 = vals[3]
            df4['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df4['tmax'])
            df4['tdiff'] = df4['tmaxf'] - df3['tmaxf']
            
            df5 = vals[4]
            df5['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df5['tmax'])
            df5['tdiff'] = df5['tmaxf'] - df4['tmaxf']
            
            df6 = vals[5]
            df6['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df6['tmax'])
            df6['tdiff'] = df6['tmaxf'] - df5['tmaxf']
    
            if test_7 == True:
                df7 = vals[6]
                df7['tmaxf'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(df7['tmax'])
                df7['tdiff'] = df7['tmaxf'] - df6['tmaxf']
            else:
                pass
    
            no_vals = False
        except Exception as g:
            no_vals = True
    
        files = count

        local_time, utc_time = standard.plot_creation_time()
    
        figs = [] 

        print("Creating Images - Please Wait...")
    
        fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig1.set_facecolor('aliceblue')
        fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
        ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
        ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax1.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax1.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax1.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax1.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax1.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
            
        ax1.set_title('National Weather Service Forecast [Day 2]\nMaximum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax1.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs1 = ax1.contourf(lons_1, lats_1, diff1, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn1 = mpplots.StationPlot(ax1, df2['longitude'][::decimate], df2['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn1.plot_parameter('C', df2['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar1 = fig1.colorbar(cs1, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar1.set_label(label="Maximum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig2.set_facecolor('aliceblue')
        fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
        ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        ax2.set_title('National Weather Service Forecast [Day 3]\nMaximum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax2.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs2 = ax2.contourf(lons_2, lats_2, diff2, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn2 = mpplots.StationPlot(ax2, df3['longitude'][::decimate], df3['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn2.plot_parameter('C', df3['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar2 = fig2.colorbar(cs2, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar2.set_label(label="Maximum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig3.set_facecolor('aliceblue')
        fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
        ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax3.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax3.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax3.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax3.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax3.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        ax3.set_title('National Weather Service Forecast [Day 4]\nMaximum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax3.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs3 = ax3.contourf(lons_3, lats_3, diff3, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn3 = mpplots.StationPlot(ax3, df4['longitude'][::decimate], df4['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn3.plot_parameter('C', df4['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar3 = fig3.colorbar(cs3, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar3.set_label(label="Maximum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
        fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig4.set_facecolor('aliceblue')
        fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
        ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax4.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax4.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax4.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax4.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax4.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax4.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        ax4.set_title('National Weather Service Forecast [Day 5]\nMaximum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax4.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs4 = ax4.contourf(lons_4, lats_4, diff4, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn4 = mpplots.StationPlot(ax4, df5['longitude'][::decimate], df5['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn4.plot_parameter('C', df5['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar4 = fig4.colorbar(cs4, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar4.set_label(label="Maximum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig5.set_facecolor('aliceblue')
        fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        ax5.set_title('National Weather Service Forecast [Day 6]\nMaximum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax5.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs5 = ax5.contourf(lons_5, lats_5, diff5, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
        if show_sample_points == True and no_vals == False:
    
            stn5 = mpplots.StationPlot(ax5, df6['longitude'][::decimate], df6['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
            stn5.plot_parameter('C', df6['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
        else:
            pass
    
        cbar5 = fig5.colorbar(cs5, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
        cbar5.set_label(label="Maximum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
    
        if files == 7:
    
            fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
            fig7.set_facecolor('aliceblue')
            fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/NDFD\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

            ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
            ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=4)
            ax7.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
            if show_rivers == True:
                ax7.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            if show_gacc_borders == True:
                ax7.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax7.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax7.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax7.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            ax7.set_title('National Weather Service Forecast [Day 7]\nMaximum Temperature Trend [Δ\N{DEGREE SIGN}F]', fontsize=title_fontsize, fontweight='bold', loc='left')
            
            ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
                
            cs7 = ax7.contourf(lons_7, lats_7, diff6, levels=levels, cmap=cmap, alpha=alpha, transform=datacrs, zorder=2, extend='both')
    
            if show_sample_points == True and no_vals == False:
    
                stn7 = mpplots.StationPlot(ax7, df7['longitude'][::decimate], df7['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=3, clip_on=True)
    
                stn7.plot_parameter('C', df7['tdiff'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=3)
    
            else:
                pass
    
            cbar7 = fig7.colorbar(cs7, location='bottom', ticks=labels, aspect=aspect, shrink=color_table_shrink, pad=0.02)
            cbar7.set_label(label="Maximum Temperature Trend (Δ\N{DEGREE SIGN}F)", fontsize=colorbar_fontsize, fontweight='bold')
        
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
            figs.append(fig7)
    
        else:
            figs.append(fig1)
            figs.append(fig2)
            figs.append(fig3)
            figs.append(fig4)
            figs.append(fig5)
    
        path, gif_path = file_functions.check_file_paths_hawaii(state, island, 'NWS Max T Trend', reference_system)
        file_functions.update_images(figs, path, gif_path, 'NWS Max T Trend')    



            
