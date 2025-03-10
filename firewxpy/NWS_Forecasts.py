
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
import firewxpy.geometry as geometry
import firewxpy.colormaps as colormaps
import firewxpy.settings as settings
import firewxpy.standard as standard
import firewxpy.dims as dims
import os
import pandas as pd
import xarray as xr
import warnings
warnings.filterwarnings('ignore')

from metpy.plots import USCOUNTIES
from matplotlib.patheffects import withStroke
from firewxpy.calc import scaling, unit_conversion
from firewxpy.utilities import file_functions
from firewxpy.data_access import NDFD_GRIDS
from firewxpy.parsers import NDFD
from metpy.units import units
from dateutil import tz
from datetime import datetime, timedelta


mpl.rcParams['font.weight'] = 'bold'
props = dict(boxstyle='round', facecolor='wheat', alpha=1)

mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9

provinces = cfeature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale='50m', facecolor='none', edgecolor='k')

mapcrs = ccrs.PlateCarree()
datacrs = ccrs.PlateCarree()

local_time, utc_time = standard.plot_creation_time()
timezone = standard.get_timezone_abbreviation()
tzone = standard.get_timezone()

def get_cwa_coords(cwa):

    if cwa == None:
        wb, eb, sb, nb = [-170, -128, 50, 75]
    if cwa == 'AER' or cwa == 'aer':
        wb, eb, sb, nb = [-155, -140.75, 55.5, 64.5]
    if cwa == 'ALU' or cwa == 'alu':
        wb, eb, sb, nb = [-170, -151, 52, 62.9]
    if cwa == 'AJK' or cwa == 'ajk':
        wb, eb, sb, nb = [-145, -129.5, 54, 60.75]
    if cwa == 'AFG' or cwa == 'afg':
        wb, eb, sb, nb = [-170, -140.75, 59, 72]

    return wb, eb, sb, nb


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

    def plot_poor_overnight_recovery_relative_humidity_forecast(poor_overnight_recovery_rh_threshold=30, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function plots the latest available NOAA/NWS Poor Overnight Recovery RH Forecast. 

        Required Arguments: None

        Optional Arguments: 
        
        1) poor_overnight_recovery_rh_threshold (Integer) -  Default = 30%. The relative humidity threshold for 
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
        
        6) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        7) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        8) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        9) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        10) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        11) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        12) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        13) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        14) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        15) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        16) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        17) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        18) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        19) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        20) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        21) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        22) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        23) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        24) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        27) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        28) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        29) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        30) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        31) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        32) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        33) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        34) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        35) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        36) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        37) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        38) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        39) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks        

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        Return: Saves individual images to f:Weather Data/NWS Forecasts/POOR OVERNIGHT RH RECOVERY/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/POOR OVERNIGHT RH RECOVERY/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        thresh = poor_overnight_recovery_rh_threshold + 1

        levels = np.arange(0, thresh, 1)
        if thresh > 31:
            labels = levels[::4]
        else:
            labels = levels[::2]

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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, 'Poor Overnight RH Recovery', reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.maxrh.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop + 1

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'maxrh')
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'maxrh')

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        init_hr = 6
        hour = short_start_times_utc[0].hour
        dt = False
        if hour == init_hr:
            start = 0
            skip = False
        else:
            if local_time.hour >= 18 or local_time.hour <= 2:
                start = 0
                skip = False
                dt = True
                hours = hour - init_hr
            else:
                start = 1
                skip = True

        if skip == True:
            extended_start = extended_start - 1
        else:
            extended_start = extended_start

        for i in range(start, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"
            if skip == False:
                index = 1 + i
            else:
                index = i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = short_vals[i]
            start = short_start_times[i]
            end = short_end_times[i]             

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['maxrh'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['maxrh'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Night {index}]\nPoor Overnight RH Recovery [Max RH <= {str(poor_overnight_recovery_rh_threshold)}%]", fontsize=8, fontweight='bold', loc='left')
            if dt == False:
                plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
            else:
                start_hour = short_start_times[0].hour - hours
                end_hour = short_end_times[0].hour - hours
                plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(0, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = extended_vals[i]
            start = extended_start_times[i]
            end = extended_end_times[i]

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['maxrh'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['maxrh'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Night {index}]\nPoor Overnight RH Recovery [Max RH <= {str(poor_overnight_recovery_rh_threshold)}%]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)   

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


    def plot_excellent_overnight_recovery_relative_humidity_forecast(excellent_overnight_recovery_rh_threshold=80, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function plots the latest available NOAA/NWS Excellent Overnight Recovery RH Forecast. 

        Required Arguments: None

        Optional Arguments: 
        
        1) excellent_overnight_recovery_rh_threshold (Integer) -  Default = 80%. The relative humidity threshold for 
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
        
        6) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        7) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        8) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        9) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        10) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        11) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        12) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        13) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        14) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        15) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        16) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        17) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        18) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        19) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        20) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        21) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        22) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        23) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        24) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        27) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        28) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        29) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        30) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        31) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        32) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        33) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        34) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        35) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        36) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        37) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        38) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        39) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks      

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        Return: Saves individual images to f:Weather Data/NWS Forecasts/EXCELLENT OVERNIGHT RH RECOVERY/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/EXCELLENT OVERNIGHT RH RECOVERY/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        levels = np.arange(excellent_overnight_recovery_rh_threshold, 102, 1)
        labels = levels[::2]
        cmap = colormaps.excellent_recovery_colormap()

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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, 'Excellent Overnight RH Recovery', reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.maxrh.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop + 1

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'maxrh')
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'maxrh')

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        init_hr = 6
        hour = short_start_times_utc[0].hour
        dt = False
        if hour == init_hr:
            start = 0
            skip = False
        else:
            if local_time.hour >= 18 or local_time.hour <= 2:
                start = 0
                skip = False
                dt = True
                hours = hour - init_hr
            else:
                start = 1
                skip = True

        if skip == True:
            extended_start = extended_start - 1
        else:
            extended_start = extended_start

        for i in range(start, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"
            if skip == False:
                index = 1 + i
            else:
                index = i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = short_vals[i]
            start = short_start_times[i]
            end = short_end_times[i]             

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['maxrh'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['maxrh'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Night {index}]\nExcellent Overnight RH Recovery [Max RH >= {str(excellent_overnight_recovery_rh_threshold)}%]", fontsize=8, fontweight='bold', loc='left')
            if dt == False:
                plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
            else:
                start_hour = short_start_times[0].hour - hours
                end_hour = short_end_times[0].hour - hours
                plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(0, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = extended_vals[i]
            start = extended_start_times[i]
            end = extended_end_times[i]

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['maxrh'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['maxrh'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Night {index}]\nExcellent Overnight RH Recovery [Max RH >= {str(excellent_overnight_recovery_rh_threshold)}%]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)   

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


    def plot_low_minimum_relative_humidity_forecast(low_rh_threshold=15, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function plots the latest available NOAA/NWS Low Minimum RH Forecast. 

        Required Arguments: None

        Optional Arguments: 
        
        1) low_rh_threshold (Integer) -  Default = 15%. The relative humidity threshold for 
           low minimum relative humidity. This is the upper bound of values shaded. 
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
        
        6) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        7) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        8) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        9) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        10) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        11) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        12) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        13) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        14) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        15) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        16) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        17) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        18) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        19) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        20) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        21) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        22) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        23) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        24) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        27) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        28) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        29) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        30) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        31) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        32) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        33) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        34) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        35) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        36) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        37) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        38) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        39) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks 

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        Return: Saves individual images to f:Weather Data/NWS Forecasts/LOW MINIMUM RH/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/LOW MINIMUM RH/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        thresh = low_rh_threshold + 1

        levels = np.arange(0, thresh, 1)
        if thresh > 26:
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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, 'Low Minimum RH', reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.minrh.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop + 1

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'unknown')
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'unknown')

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        init_hr = 18
        hour = short_start_times_utc[0].hour
        dt = False
        if hour == init_hr:
            start = 0
            skip = False
        else:
            if local_time.hour <= 14:
                start = 0
                skip = False
                dt = True
                hours = hour - init_hr
            else:
                start = 1
                skip = True

        if skip == True:
            extended_start = extended_start - 1
        else:
            extended_start = extended_start

        for i in range(start, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"
            if skip == False:
                index = 1 + i
            else:
                index = i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = short_vals[i]
            start = short_start_times[i]
            end = short_end_times[i]             

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['unknown'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['unknown'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Day {index}]\nLow Minimum RH [Min RH <= {str(low_rh_threshold)}%]", fontsize=8, fontweight='bold', loc='left')
            if dt == False:
                plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
            else:
                start_hour = short_start_times[0].hour - hours
                end_hour = short_end_times[0].hour - hours
                plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(0, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = extended_vals[i]
            start = extended_start_times[i]
            end = extended_end_times[i]

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['unknown'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['unknown'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Day {index}]\nLow Minimum RH [Min RH <= {str(low_rh_threshold)}%]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)   

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


    def plot_minimum_relative_humidity_forecast(low_rh_threshold=15, high_rh_threshold=60, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, x=0.01, y=0.97):


        r'''
        This function plots the latest available NOAA/NWS Low Minimum RH Forecast. 

        Required Arguments: None

        Optional Arguments: 
        
        1) low_rh_threshold (Integer) -  Default = 15%. The relative humidity threshold for 
           low minimum relative humidity. This is the value at which the red contour line
           plots on the map. 

        2) high_rh_threshold (Integer) - Default = 60%. The relative humidity threshold for 
           high minimum relative humidity. This is the value at which the blue contour line 
           plots on the map. 

        3) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        4) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        5) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere. 

        6) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere.
        
        7) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        9) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        17) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        18) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        19) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        20) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        21) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        22) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        23) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        24) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        27) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        28) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        29) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        30) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        31) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        32) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        33) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        34) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        35) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        36) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        37) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        38) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        39) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        40) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks   

        45) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        46) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        47) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        48) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.         

        Return: Saves individual images to f:Weather Data/NWS Forecasts/Minimum RH Low Contour {low_rh_threshold}% High Contour {high_rh_threshold}%/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Minimum RH Low Contour {low_rh_threshold}% High Contour {high_rh_threshold}%/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        thresh = low_rh_threshold + 1

        levels = np.arange(0, 102, 1)
        labels = levels[::5]

        cmap = colormaps.relative_humidity_colormap()

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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            sp, x, y = settings.get_sp_dims_and_textbox_coords(state)

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            sp, x, y = settings.get_sp_dims_and_textbox_coords(gacc_region)

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, f"Minimum RH Low Contour {low_rh_threshold}% High Contour {high_rh_threshold}%", reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.minrh.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop + 1

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'unknown')
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'unknown')

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        init_hr = 18
        hour = short_start_times_utc[0].hour
        dt = False
        if hour == init_hr:
            start = 0
            skip = False
        else:
            if local_time.hour < 14:
                start = 0
                skip = False
                dt = True
                hours = hour - init_hr
            else:
                start = 1
                skip = True

        if skip == True:
            extended_start = extended_start - 1
        else:
            extended_start = extended_start

        for i in range(start, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"
            if skip == False:
                index = 1 + i
            else:
                index = i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = short_vals[i]
            start = short_start_times[i]
            end = short_end_times[i]             

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['unknown'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['unknown'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            c_low = ax.contour(ds_short['longitude'][:, :], ds_short['latitude'][:, :], mpcalc.smooth_gaussian(ds_short['unknown'][i, :, :] * units('percent'), n=8), levels=[low_rh_threshold], colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_low, levels=[low_rh_threshold], inline=True, fontsize=8, rightside_up=True)  

            c_high = ax.contour(ds_short['longitude'][:, :], ds_short['latitude'][:, :], mpcalc.smooth_gaussian(ds_short['unknown'][i, :, :] * units('percent'), n=8), levels=[high_rh_threshold], colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_high, levels=[high_rh_threshold], inline=True, fontsize=8, rightside_up=True)    

            plt.title(f"National Weather Service Forecast [Day {index}]\nMinimum Relative Humidity", fontsize=8, fontweight='bold', loc='left')
            if dt == False:
                plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
            else:
                start_hour = short_start_times[0].hour - hours
                end_hour = short_end_times[0].hour - hours
                plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            ax.text(x, y, f"Red Contour Line: RH = {low_rh_threshold}% | Blue Contour Line: RH = {high_rh_threshold}%", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(0, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = extended_vals[i]
            start = extended_start_times[i]
            end = extended_end_times[i]

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['unknown'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['unknown'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            c_low = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian(ds_extended['unknown'][i, :, :] * units('percent'), n=8), levels=[low_rh_threshold], colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_low, levels=[low_rh_threshold], inline=True, fontsize=8, rightside_up=True)  

            c_high = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian(ds_extended['unknown'][i, :, :] * units('percent'), n=8), levels=[high_rh_threshold], colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_high, levels=[high_rh_threshold], inline=True, fontsize=8, rightside_up=True)    

            plt.title(f"National Weather Service Forecast [Day {index}]\nMinimum Relative Humidity", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            ax.text(x, y, f"Red Contour Line: RH = {low_rh_threshold}% | Blue Contour Line: RH = {high_rh_threshold}%", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


    def plot_maximum_relative_humidity_forecast(low_rh_threshold=30, high_rh_threshold=80, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, x=0.01, y=0.97):


        r'''
        This function plots the latest available NOAA/NWS Low Minimum RH Forecast. 

        Required Arguments: None

        Optional Arguments: 
        
        1) low_rh_threshold (Integer) -  Default = 30%. The relative humidity threshold for 
           low maximum relative humidity. This is the value at which the red contour line
           plots on the map. 

        2) high_rh_threshold (Integer) - Default = 80%. The relative humidity threshold for 
           high maximum relative humidity. This is the value at which the blue contour line 
           plots on the map. 

        3) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        4) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        5) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere. 

        6) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere.
        
        7) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        9) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        17) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        18) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        19) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        20) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        21) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        22) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        23) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        24) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        27) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        28) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        29) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        30) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        31) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        32) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        33) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        34) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        35) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        36) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        37) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        38) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        39) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        40) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks   

        45) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        46) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        47) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        48) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.         

        Return: Saves individual images to f:Weather Data/NWS Forecasts/Maximum RH Low Contour {low_rh_threshold}% High Contour {high_rh_threshold}%/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Maximum RH Low Contour {low_rh_threshold}% High Contour {high_rh_threshold}%/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        thresh = low_rh_threshold + 1

        levels = np.arange(0, 102, 1)
        labels = levels[::5]

        cmap = colormaps.relative_humidity_colormap()

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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            sp, x, y = settings.get_sp_dims_and_textbox_coords(state)

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            sp, x, y = settings.get_sp_dims_and_textbox_coords(gacc_region)

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, f"Maximum RH Low Contour {low_rh_threshold}% High Contour {high_rh_threshold}%", reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.maxrh.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop + 1

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'maxrh')
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'maxrh')

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        init_hr = 6
        hour = short_start_times_utc[0].hour
        dt = False
        if hour == init_hr:
            start = 0
            skip = False
        else:
            if local_time.hour >= 18 or local_time.hour <= 2:
                start = 0
                skip = False
                dt = True
                hours = hour - init_hr
            else:
                start = 1
                skip = True

        if skip == True:
            extended_start = extended_start - 1
        else:
            extended_start = extended_start

        for i in range(start, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"
            if skip == False:
                index = 1 + i
            else:
                index = i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = short_vals[i]
            start = short_start_times[i]
            end = short_end_times[i]             

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['maxrh'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['maxrh'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            c_low = ax.contour(ds_short['longitude'][:, :], ds_short['latitude'][:, :], mpcalc.smooth_gaussian(ds_short['maxrh'][i, :, :], n=8), levels=[low_rh_threshold], colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_low, levels=[low_rh_threshold], inline=True, fontsize=8, rightside_up=True)  

            c_high = ax.contour(ds_short['longitude'][:, :], ds_short['latitude'][:, :], mpcalc.smooth_gaussian(ds_short['maxrh'][i, :, :], n=8), levels=[high_rh_threshold], colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_high, levels=[high_rh_threshold], inline=True, fontsize=8, rightside_up=True)    

            plt.title(f"National Weather Service Forecast [Night {index}]\nMaximum Relative Humidity", fontsize=8, fontweight='bold', loc='left')
            if dt == False:
                plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
            else:
                start_hour = short_start_times[0].hour - hours
                end_hour = short_end_times[0].hour - hours
                plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            ax.text(x, y, f"Red Contour Line: RH = {low_rh_threshold}% | Blue Contour Line: RH = {high_rh_threshold}%", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(0, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = extended_vals[i]
            start = extended_start_times[i]
            end = extended_end_times[i]

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['maxrh'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['maxrh'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            c_low = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian(ds_extended['maxrh'][i, :, :], n=8), levels=[low_rh_threshold], colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_low, levels=[low_rh_threshold], inline=True, fontsize=8, rightside_up=True)  

            c_high = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian(ds_extended['maxrh'][i, :, :], n=8), levels=[high_rh_threshold], colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_high, levels=[high_rh_threshold], inline=True, fontsize=8, rightside_up=True)    

            plt.title(f"National Weather Service Forecast [Night {index}]\nMaximum Relative Humidity", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            ax.text(x, y, f"Red Contour Line: RH = {low_rh_threshold}% | Blue Contour Line: RH = {high_rh_threshold}%", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


    def plot_maximum_relative_humidity_forecast_trend(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, x=0.01, y=0.97):


        r'''
        This function plots the latest available NOAA/NWS Maximum RH Forecast Trend. 

        Required Arguments: None

        Optional Arguments: 

        1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
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
        
        5) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        6) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        7) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        15) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        16) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        17) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        18) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        19) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        20) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        21) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        22) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        23) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        24) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        27) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        28) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        29) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        30) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        31) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks   

        39) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        40) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        41) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        42) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.         

        Return: Saves individual images to f:Weather Data/NWS Forecasts/Maximum RH Trend/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Maximum RH Trend/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        levels = np.arange(-60, 61, 1)
        labels = levels[::5]

        lower = [-50, -30, -15]
        higher = [15, 30, 50]

        cmap = colormaps.relative_humidity_change_colormap()

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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            sp, x, y = settings.get_sp_dims_and_textbox_coords(state)

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            sp, x, y = settings.get_sp_dims_and_textbox_coords(gacc_region)

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, f"Maximum RH Trend", reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.maxrh.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop
        total_count = short_stop + extended_stop

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'maxrh', diff=True)
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'maxrh', diff=True)

        short_vals_init = NDFD.ndfd_to_dataframe(ds_short, 'maxrh')
        extended_vals_init = NDFD.ndfd_to_dataframe(ds_extended, 'maxrh')

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        vs = short_vals_init[short_stop - 1]
        ve = extended_vals_init[0]
        s = short_start_times[short_stop - 1]
        s1 = extended_start_times[0]

        for i in range(1, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"

            index = i + 1

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

                try:
                    val = short_vals[i-1]
                    start = short_start_times[i-1]
                    start_1 = short_start_times[i]
                except Exception as e:
                    pass
    
                stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
        
                stn.plot_parameter('C', val['maxrh'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

                try:
                    cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], (ds_short['maxrh'][i, :, :] - ds_short['maxrh'][i-1, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)
        
                    c_low = ax.contour(ds_short['longitude'][:, :], ds_short['latitude'][:, :], mpcalc.smooth_gaussian((ds_short['maxrh'][i, :, :] - ds_short['maxrh'][i-1, :, :]), n=8), levels=lower, colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_low, levels=lower, inline=True, fontsize=8, rightside_up=True)  
        
                    c_high = ax.contour(ds_short['longitude'][:, :], ds_short['latitude'][:, :], mpcalc.smooth_gaussian((ds_short['maxrh'][i, :, :] - ds_short['maxrh'][i-1, :, :]), n=8), levels=higher, colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_high, levels=higher, inline=True, fontsize=8, rightside_up=True)   
                except Exception as e:
                    pass

            plt.title(f"National Weather Service Forecast\nMaximum Relative Humidity Trend [Δ%]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Night {index}: {start_1.strftime('%a %m/%d')} - Night {index-1}: {start.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')
            
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            ax.text(x, y, f"Red Contour Line: Decreasing RH | Blue Contour Line: Increasing RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(1, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"
            fname_7 = f"B_Extended_Term_{i+1}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            try:
                val = extended_vals[i-2]
                start = extended_start_times[i-2]
                start_1 = extended_start_times[i-1]
            except Exception as e:
                pass

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            if i == 1:
                try:

                    diff = ve['maxrh'] - vs['maxrh']
    
                    stn.plot_parameter('C', diff[::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

                    cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], (ds_extended['maxrh'][0, :, :] - ds_short['maxrh'][short_stop - 1, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)
        
                    c_low = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['maxrh'][0, :, :] - ds_short['maxrh'][short_stop - 1, :, :]), n=8), levels=lower, colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_low, levels=lower, inline=True, fontsize=8, rightside_up=True)  
        
                    c_high = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['maxrh'][0, :, :] - ds_short['maxrh'][short_stop - 1, :, :]), n=8), levels=higher, colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_high, levels=higher, inline=True, fontsize=8, rightside_up=True) 
                except Exception as e:
                    pass

                plt.title(f"Night {index}: {s1.strftime('%a %m/%d')} - Night {index-1}: {s.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')

            else:

                stn.plot_parameter('C', val['maxrh'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

                try:
                    cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], (ds_extended['maxrh'][i-1, :, :] - ds_extended['maxrh'][i-2, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)
        
                    c_low = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['maxrh'][i-1, :, :] - ds_extended['maxrh'][i-2, :, :]), n=8), levels=lower, colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_low, levels=lower, inline=True, fontsize=8, rightside_up=True)  
        
                    c_high = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['maxrh'][i-1, :, :] - ds_extended['maxrh'][i-2, :, :]), n=8), levels=higher, colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_high, levels=higher, inline=True, fontsize=8, rightside_up=True)    
                except Exception as e:
                    pass
                    
                plt.title(f"Night {index}: {start_1.strftime('%a %m/%d')} - Night {index-1}: {start.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')

            plt.title(f"National Weather Service Forecast\nMaximum Relative Humidity Trend [Δ%]", fontsize=8, fontweight='bold', loc='left')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            ax.text(x, y, f"Red Contour Line: Decreasing RH | Blue Contour Line: Increasing RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        fig = plt.figure(figsize=(12,12))
        fig.set_facecolor('aliceblue')
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=1, zorder=1)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass  

        try:
            val = extended_vals[-1]
            start = extended_start_times[-2]
            start_1 = extended_start_times[-1]
        except Exception as e:
            pass

        stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                         transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
        
        stn.plot_parameter('C', val['maxrh'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

        try:
            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], (ds_extended['maxrh'][-1, :, :] - ds_extended['maxrh'][-2, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            c_low = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['maxrh'][-1, :, :] - ds_extended['maxrh'][-2, :, :]), n=8), levels=lower, colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_low, levels=lower, inline=True, fontsize=8, rightside_up=True)  

            c_high = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['maxrh'][-1, :, :] - ds_extended['maxrh'][-2, :, :]), n=8), levels=higher, colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_high, levels=higher, inline=True, fontsize=8, rightside_up=True)    
        except Exception as e:
            pass
            
            
        plt.title(f"Night {index + 1}: {start_1.strftime('%a %m/%d')} - Night {index}: {start.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')

        plt.title(f"National Weather Service Forecast\nMaximum Relative Humidity Trend [Δ%]", fontsize=8, fontweight='bold', loc='left')

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

        ax.text(x, y, f"Red Contour Line: Decreasing RH | Blue Contour Line: Increasing RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)

        fig.savefig(f"{path}/{fname_7}", bbox_inches='tight')
        print(f"Saved {fname_7} to {path_print}")


    def plot_minimum_relative_humidity_forecast_trend(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, x=0.01, y=0.97):


        r'''
        This function plots the latest available NOAA/NWS Minimum RH Forecast Trend. 

        Required Arguments: None

        Optional Arguments: 

        1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
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
        
        5) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        6) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        7) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        15) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        16) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        17) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        18) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        19) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        20) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        21) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        22) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        23) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        24) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        27) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        28) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        29) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        30) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        31) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks   

        39) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        40) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        41) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        42) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.         

        Return: Saves individual images to f:Weather Data/NWS Forecasts/Minimum RH Trend/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Minimum RH Trend/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        levels = np.arange(-60, 61, 1)
        labels = levels[::5]

        lower = [-50, -30, -15]
        higher = [15, 30, 50]

        cmap = colormaps.relative_humidity_change_colormap()

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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            sp, x, y = settings.get_sp_dims_and_textbox_coords(state)

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            sp, x, y = settings.get_sp_dims_and_textbox_coords(gacc_region)

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, f"Minimum RH Trend", reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.minrh.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop
        total_count = short_stop + extended_stop

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'unknown', diff=True)
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'unknown', diff=True)

        short_vals_init = NDFD.ndfd_to_dataframe(ds_short, 'unknown')
        extended_vals_init = NDFD.ndfd_to_dataframe(ds_extended, 'unknown')

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        vs = short_vals_init[short_stop - 1]
        ve = extended_vals_init[0]
        s = short_start_times[short_stop - 1]
        s1 = extended_start_times[0]

        for i in range(1, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"

            index = i + 1

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

                try:
                    val = short_vals[i-1]
                    start = short_start_times[i-1]
                    start_1 = short_start_times[i]
                except Exception as e:
                    pass
    
                stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
        
                stn.plot_parameter('C', val['unknown'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

                try:
                    cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], (ds_short['unknown'][i, :, :] - ds_short['unknown'][i-1, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)
        
                    c_low = ax.contour(ds_short['longitude'][:, :], ds_short['latitude'][:, :], mpcalc.smooth_gaussian((ds_short['unknown'][i, :, :] - ds_short['unknown'][i-1, :, :]) * units('percent'), n=8), levels=lower, colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_low, levels=lower, inline=True, fontsize=8, rightside_up=True)  
        
                    c_high = ax.contour(ds_short['longitude'][:, :], ds_short['latitude'][:, :], mpcalc.smooth_gaussian((ds_short['unknown'][i, :, :] - ds_short['unknown'][i-1, :, :]) * units('percent'), n=8), levels=higher, colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_high, levels=higher, inline=True, fontsize=8, rightside_up=True)   
                except Exception as e:
                    pass

            plt.title(f"National Weather Service Forecast\nMinimum Relative Humidity Trend [Δ%]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Day {index}: {start_1.strftime('%a %m/%d')} - Day {index-1}: {start.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')
            
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            ax.text(x, y, f"Red Contour Line: Decreasing RH | Blue Contour Line: Increasing RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(1, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"
            fname_7 = f"B_Extended_Term_{i+1}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            try:
                val = extended_vals[i-2]
                start = extended_start_times[i-2]
                start_1 = extended_start_times[i-1]
            except Exception as e:
                pass

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            if i == 1:
                try:

                    diff = ve['unknown'] - vs['unknown']
    
                    stn.plot_parameter('C', diff[::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

                    cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], (ds_extended['unknown'][0, :, :] - ds_short['unknown'][short_stop - 1, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)
        
                    c_low = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['unknown'][0, :, :] - ds_short['unknown'][short_stop - 1, :, :]) * units('percent'), n=8), levels=lower, colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_low, levels=lower, inline=True, fontsize=8, rightside_up=True)  
        
                    c_high = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['unknown'][0, :, :] - ds_short['unknown'][short_stop - 1, :, :]) * units('percent'), n=8), levels=higher, colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_high, levels=higher, inline=True, fontsize=8, rightside_up=True) 
                except Exception as e:
                    pass

                plt.title(f"Day {index}: {s1.strftime('%a %m/%d')} - Day {index-1}: {s.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')

            else:

                stn.plot_parameter('C', val['unknown'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

                try:
                    cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], (ds_extended['unknown'][i-1, :, :] - ds_extended['unknown'][i-2, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)
        
                    c_low = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['unknown'][i-1, :, :] - ds_extended['unknown'][i-2, :, :]) * units('percent'), n=8), levels=lower, colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_low, levels=lower, inline=True, fontsize=8, rightside_up=True)  
        
                    c_high = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['unknown'][i-1, :, :] - ds_extended['unknown'][i-2, :, :]) * units('percent'), n=8), levels=higher, colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_high, levels=higher, inline=True, fontsize=8, rightside_up=True)    
                except Exception as e:
                    pass
                    
                    
                plt.title(f"Day {index}: {start_1.strftime('%a %m/%d')} - Day {index-1}: {start.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')

            plt.title(f"National Weather Service Forecast\nMinimum Relative Humidity Trend [Δ%]", fontsize=8, fontweight='bold', loc='left')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            ax.text(x, y, f"Red Contour Line: Decreasing RH | Blue Contour Line: Increasing RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")

        fig = plt.figure(figsize=(12,12))
        fig.set_facecolor('aliceblue')
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=1, zorder=1)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass  

        try:
            val = extended_vals[-1]
            start = extended_start_times[-2]
            start_1 = extended_start_times[-1]
        except Exception as e:
            pass

        stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                         transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
        
        stn.plot_parameter('C', val['unknown'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

        try:
            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], (ds_extended['unknown'][-1, :, :] - ds_extended['unknown'][-2, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            c_low = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['unknown'][-1, :, :] - ds_extended['unknown'][-2, :, :]) * units('percent'), n=8), levels=lower, colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_low, levels=lower, inline=True, fontsize=8, rightside_up=True)  

            c_high = ax.contour(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], mpcalc.smooth_gaussian((ds_extended['unknown'][-1, :, :] - ds_extended['unknown'][-2, :, :]) * units('percent'), n=8), levels=higher, colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
            ax.clabel(c_high, levels=higher, inline=True, fontsize=8, rightside_up=True)    
        except Exception as e:
            pass
            
            
        plt.title(f"Day {index + 1}: {start_1.strftime('%a %m/%d')} - Day {index}: {start.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')

        plt.title(f"National Weather Service Forecast\nMinimum Relative Humidity Trend [Δ%]", fontsize=8, fontweight='bold', loc='left')

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

        ax.text(x, y, f"Red Contour Line: Decreasing RH | Blue Contour Line: Increasing RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)

        fig.savefig(f"{path}/{fname_7}", bbox_inches='tight')
        print(f"Saved {fname_7} to {path_print}")


class temperature:

    r'''
    This class holds all the plotting functions for the National Weather Service Temperature Forecasts:

    '''

    def plot_frost_freeze_forecast(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function plots the latest available NOAA/NWS Frost/Freeze Forecast. 

        Required Arguments: None

        Optional Arguments: 

        1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
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
        
        5) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        6) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        7) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        15) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        16) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        17) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        18) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        19) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        20) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        21) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        22) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        23) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        24) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        27) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        28) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        29) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        30) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        31) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks        

        39) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        40) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        Return: Saves individual images to f:Weather Data/NWS Forecasts/Frost Freeze Forecast/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Frost Freeze Forecast/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        levels = np.arange(-10, 33, 1)
        labels = levels [::2]

        cmap = colormaps.cool_temperatures_colormap()

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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, 'Frost Freeze Forecast', reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.mint.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop + 1

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'tmin', temperature_to_F=True)
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'tmin', temperature_to_F=True)

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        init_hr = 0
        hour = short_start_times_utc[0].hour
        dt = False
        if hour == init_hr:
            start = 0
            skip = False
        else:
            if local_time.hour >= 18 or local_time.hour <= 2:
                start = 0
                skip = False
                dt = True
                hours = hour - init_hr
            else:
                start = 1
                skip = True

        if skip == True:
            extended_start = extended_start - 1
        else:
            extended_start = extended_start

        for i in range(start, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"
            if skip == False:
                index = 1 + i
            else:
                index = i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = short_vals[i]
            start = short_start_times[i]
            end = short_end_times[i]             

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['tmin'][::decimate], color='orange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=10)

            cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['tmin'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='min')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Night {index}]\nFrost Freeze Areas [Minimum Temperature <= 32°F]", fontsize=8, fontweight='bold', loc='left')
            if dt == False:
                plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
            else:
                start_hour = short_start_times[0].hour - hours
                end_hour = short_end_times[0].hour - hours
                plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(0, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = extended_vals[i]
            start = extended_start_times[i]
            end = extended_end_times[i]

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['tmin'][::decimate], color='orange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=10)

            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['tmin'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='min')

            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Night {index}]\nFrost Freeze Areas [Minimum Temperature <= 32°F]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)   

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


    def plot_extremely_warm_low_temperature_forecast(warm_low_threshold=80, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function plots the latest available NOAA/NWS Extremely Warm Low Temperature Forecast. 

        Required Arguments: None

        Optional Arguments: 

        1) warm_low_threshold (Integer) - Default = 80F. The threshold that defines an "extremely warm
           low temperature." This is the lower bound of the colorscale. All values greater than or equal to
           this threshold will be shaded. 

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
        
        6) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        7) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        8) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        9) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        10) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        11) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        12) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        13) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        14) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        15) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        16) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        17) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        18) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        19) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        20) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        21) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        22) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        23) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        24) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        27) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        28) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        29) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        30) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        31) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        32) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        33) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        34) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        35) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        36) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        37) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        38) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        39) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks        

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        Return: Saves individual images to f:Weather Data/NWS Forecasts/Extremely Warm Low Temperatures/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Extremely Warm Low Temperatures/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        end = warm_low_threshold + 21

        levels = np.arange(warm_low_threshold, end, 1)
        labels = levels [::2]

        cmap = colormaps.warm_temperatures_colormap()

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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, 'Extremely Warm Low Temperatures', reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.mint.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop + 1

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'tmin', temperature_to_F=True)
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'tmin', temperature_to_F=True)

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        init_hr = 0
        hour = short_start_times_utc[0].hour
        dt = False
        if hour == init_hr:
            start = 0
            skip = False
        else:
            if local_time.hour >= 18 or local_time.hour <= 2:
                start = 0
                skip = False
                dt = True
                hours = hour - init_hr
            else:
                start = 1
                skip = True
        if skip == True:
            extended_start = extended_start - 1
        else:
            extended_start = extended_start

        for i in range(start, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"
            if skip == False:
                index = 1 + i
            else:
                index = i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = short_vals[i]
            start = short_start_times[i]
            end = short_end_times[i]             

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['tmin'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['tmin'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Night {index}]\nExtremely Warm Low Temperatures [Minimum Temperature >= {str(warm_low_threshold)}°F]", fontsize=8, fontweight='bold', loc='left')
            if dt == False:
                plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
            else:
                start_hour = short_start_times[0].hour - hours
                end_hour = short_end_times[0].hour - hours
                plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(0, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = extended_vals[i]
            start = extended_start_times[i]
            end = extended_end_times[i]

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['tmin'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['tmin'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='max')

            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Night {index}]\nExtremely Warm Low Temperatures [Minimum Temperature >= {str(warm_low_threshold)}°F]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)   

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


    def plot_extreme_heat_forecast(extreme_heat_threshold=110, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function plots the latest available NOAA/NWS Extreme Heat Forecast. 

        Required Arguments: None

        Optional Arguments: 

        1) extreme_heat_threshold (Integer) - Default = 110F. The threshold that defines "extreme heat" with respect to 
           maximum temperature. This is the lower bound of the colorscale. All values greater than or equal to
           this threshold will be shaded. 

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
        
        6) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        7) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        8) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        9) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        10) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        11) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        12) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        13) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        14) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        15) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        16) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        17) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        18) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        19) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        20) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        21) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        22) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        23) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        24) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        27) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        28) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        29) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        30) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        31) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        32) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        33) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        34) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        35) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        36) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        37) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        38) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        39) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks        

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        Return: Saves individual images to f:Weather Data/NWS Forecasts/Extreme Heat Forecast/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Extreme Heat Forecast/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        end = extreme_heat_threshold + 21

        levels = np.arange(extreme_heat_threshold, end, 1)
        labels = levels [::2]

        cmap = colormaps.warm_temperatures_colormap()

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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, 'Extreme Heat Forecast', reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.maxt.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop + 1

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'tmax', temperature_to_F=True)
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'tmax', temperature_to_F=True)

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        init_hr = 12
        hour = short_start_times_utc[0].hour
        dt = False
        if hour == init_hr:
            start = 0
            skip = False
        else:
            if local_time.hour <= 14:
                start = 0
                skip = False
                dt = True
                hours = hour - init_hr
            else:
                start = 1
                skip = True

        if skip == True:
            extended_start = extended_start - 1
        else:
            extended_start = extended_start

        for i in range(start, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"
            if skip == False:
                index = 1 + i
            else:
                index = i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = short_vals[i]
            start = short_start_times[i]
            end = short_end_times[i]             

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['tmax'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['tmax'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Day {index}]\nExtreme Heat Forecast [Maximum Temperature >= {str(extreme_heat_threshold)}°F]", fontsize=8, fontweight='bold', loc='left')
            if dt == False:
                plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
            else:
                start_hour = short_start_times[0].hour - hours
                end_hour = short_end_times[0].hour - hours
                plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(0, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = extended_vals[i]
            start = extended_start_times[i]
            end = extended_end_times[i]

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['tmax'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['tmax'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='max')

            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Day {index}]\nExtreme Heat Forecast [Maximum Temperature >= {str(extreme_heat_threshold)}°F]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)   

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


    def plot_maximum_temperature_forecast(start_of_warm_season_month=4, end_of_warm_season_month=10, temp_scale_warm_start=40, temp_scale_warm_stop=110, temp_scale_cool_start=20, temp_scale_cool_stop=90, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function plots the latest available NOAA/NWS Maximum Temperature Forecast. 

        Required Arguments: None

        Optional Arguments: 

        1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

        2) end_of_warm_season_month (Integer) - Default = 10 (October). The numeric value for the month the warm season ends. 

        3) temp_scale_warm_start (Integer) - Default = 40. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

        4) temp_scale_warm_stop (Integer) - Default = 110. The top bound temperature value in Fahrenheit of the warm season temperature range.

        5) temp_scale_cool_start (Integer) - Default = 20. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

        6) temp_scale_cool_stop (Integer) - Default = 90. The top bound temperature value in Fahrenheit of the cool season temperature range.         

        7) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        8) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        9) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere. 

        10) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere.
        
        11) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        12) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        13) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        14) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        15) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        16) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        17) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        18) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        19) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        20) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        21) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        22) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        23) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        24) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        32) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        33) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        34) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        35) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        37) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        38) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        39) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        40) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        41) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        42) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        43) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        44) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks        

        45) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        46) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        Return: Saves individual images to f:Weather Data/NWS Forecasts/Max T Forecast/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Max T Forecast/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            levels = np.arange(temp_scale_warm_start, (temp_scale_warm_stop + 1), 1)
            labels = levels[::5]
        else:
            levels = np.arange(temp_scale_cool_start, (temp_scale_cool_stop + 1), 1)
            labels = levels[::5]            

        cmap = colormaps.temperature_colormap()

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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, 'Max T Forecast', reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.maxt.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop + 1

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'tmax', temperature_to_F=True)
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'tmax', temperature_to_F=True)

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        init_hr = 12
        hour = short_start_times_utc[0].hour
        dt = False
        if hour == init_hr:
            start = 0
            skip = False
        else:
            if local_time.hour < 14:
                start = 0
                skip = False
                dt = True
                hours = hour - init_hr
            else:
                start = 1
                skip = True

        if skip == True:
            extended_start = extended_start - 1
        else:
            extended_start = extended_start

        for i in range(start, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"
            if skip == False:
                index = 1 + i
            else:
                index = i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = short_vals[i]
            start = short_start_times[i]
            end = short_end_times[i]             

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['tmax'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['tmax'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Day {index}]\nMaximum Temperature Forecast [°F]", fontsize=8, fontweight='bold', loc='left')
            if dt == False:
                plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
            else:
                start_hour = short_start_times[0].hour - hours
                end_hour = short_end_times[0].hour - hours
                plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(0, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = extended_vals[i]
            start = extended_start_times[i]
            end = extended_end_times[i]

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['tmax'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['tmax'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')

            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Day {index}]\nMaximum Temperature Forecast [°F]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)   

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


    def plot_minimum_temperature_forecast(start_of_warm_season_month=4, end_of_warm_season_month=10, temp_scale_warm_start=30, temp_scale_warm_stop=90, temp_scale_cool_start=0, temp_scale_cool_stop=70, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function plots the latest available NOAA/NWS Minimum Temperature Forecast. 

        Required Arguments: None

        Optional Arguments: 

        1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

        2) end_of_warm_season_month (Integer) - Default = 10 (October). The numeric value for the month the warm season ends. 

        3) temp_scale_warm_start (Integer) - Default = 30. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

        4) temp_scale_warm_stop (Integer) - Default = 90. The top bound temperature value in Fahrenheit of the warm season temperature range.

        5) temp_scale_cool_start (Integer) - Default = 0. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

        6) temp_scale_cool_stop (Integer) - Default = 70. The top bound temperature value in Fahrenheit of the cool season temperature range.         

        7) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        8) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        9) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere. 

        10) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere.
        
        11) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        12) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        13) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        14) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        15) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        16) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        17) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        18) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        19) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        20) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        21) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        22) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        23) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        24) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        32) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        33) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        34) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        35) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        37) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        38) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        39) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        40) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        41) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        42) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        43) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        44) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks        

        45) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        46) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        Return: Saves individual images to f:Weather Data/NWS Forecasts/Min T Forecast/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Min T Forecast/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = None
        else:
            state = state

        if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
            levels = np.arange(temp_scale_warm_start, (temp_scale_warm_stop + 1), 1)
            labels = levels[::5]
        else:
            levels = np.arange(temp_scale_cool_start, (temp_scale_cool_stop + 1), 1)
            labels = levels[::5]            

        cmap = colormaps.temperature_colormap()

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

        if state != None and gacc_region == None:
            directory_name = settings.get_state_directory(state)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_state(state)
            else:
                decimate = decimate

            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'AK' or state == 'ak':
               western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
    
        if state == None and gacc_region != None:
            directory_name = settings.get_gacc_region_directory(gacc_region)
    
            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_gacc_region(gacc_region)
            else:
                decimate = decimate

            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', gacc_region)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

            if decimate == 'default':
                decimate = scaling.get_NDFD_decimation_by_region(western_bound, eastern_bound, southern_bound, northern_bound, 'conus')
            else:
                decimate = decimate

            directory_name = settings.check_NDFD_directory_name('conus')
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, 'Min T Forecast', reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.mint.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop + 1

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'tmin', temperature_to_F=True)
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'tmin', temperature_to_F=True)

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        init_hr = 0
        hour = short_start_times_utc[0].hour
        dt = False
        if hour == init_hr:
            start = 0
            skip = False
        else:
            if local_time.hour >= 18 and local_time.hour <= 2:
                start = 0
                skip = False
                dt = True
                hours = hour - init_hr
            else:
                start = 1
                skip = True

        if skip == True:
            extended_start = extended_start - 1
        else:
            extended_start = extended_start

        for i in range(start, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"
            if skip == False:
                index = 1 + i
            else:
                index = i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = short_vals[i]
            start = short_start_times[i]
            end = short_end_times[i]             

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['tmin'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['tmin'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Night {index}]\nMinimum Temperature Forecast [°F]", fontsize=8, fontweight='bold', loc='left')
            if dt == False:
                plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
            else:
                start_hour = short_start_times[0].hour - hours
                end_hour = short_end_times[0].hour - hours
                plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(0, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            val = extended_vals[i]
            start = extended_start_times[i]
            end = extended_end_times[i]

            stn = mpplots.StationPlot(ax, val['longitude'][::decimate], val['latitude'][::decimate],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['tmin'][::decimate], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['tmin'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')

            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

            plt.title(f"National Weather Service Forecast [Night {index}]\nMinimum Temperature Forecast [°F]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)   

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


    def plot_minimum_temperature_forecast_trend(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa='STATE', signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function plots the latest available NOAA/NWS Minimum Temperature Forecast Trend. 

        Required Arguments: None

        Optional Arguments: 

        1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
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
        
        5) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        6) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        7) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        15) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        16) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        17) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        18) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        19) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        20) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        21) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        22) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        23) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        24) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        27) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        28) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        29) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        30) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        31) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks   

        39) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        40) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot.      

        Return: Saves individual images to f:Weather Data/NWS Forecasts/Minimum Temperature Trend/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Minimum Temperature Trend/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = gacc_region
        else:
            state = state

        levels = np.arange(-30, 31, 1)
        labels = levels[::5]

        lower = [-20, -10]
        higher = [10, 20]

        cmap = colormaps.temperature_change_colormap()

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

        western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
        if state == 'AK' or state == 'ak':
           western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
           directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'
        if state != 'AK' and state != 'ak' or gacc_region != None:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'

        sp, x, y = settings.get_sp_dims_and_textbox_coords(state)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3

    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, f"Minimum Temperature Trend", reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.mint.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        short_stop = len(ds_short['step'])
        extended_stop = len(ds_extended['step'])
        extended_start = short_stop
        total_count = short_stop + extended_stop

        short_times = ds_short['valid_time']
        extended_times = ds_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        decimate = scaling.get_ndfd_decimation(western_bound, eastern_bound, southern_bound, northern_bound)
        try:
            if cwa == 'AER' or cwa == 'aer' or cwa == 'ALU' or cwa == 'alu' or cwa == 'AJK' or cwa == 'ajk':
                decimate = 30
            if cwa == 'AFG' or cwa == 'afg':
                decimate = 50
        except Exception as e:
            pass

        if state == 'SWCC' or state == 'swcc':
            decimate = 30

        short_vals = NDFD.ndfd_to_dataframe(ds_short, 'tmin', diff=True, temperature_to_F=True, decimate=decimate)
        extended_vals = NDFD.ndfd_to_dataframe(ds_extended, 'tmin', diff=True, temperature_to_F=True, decimate=decimate)

        short_vals_init = NDFD.ndfd_to_dataframe(ds_short, 'tmin', temperature_to_F=True, decimate=decimate)
        extended_vals_init = NDFD.ndfd_to_dataframe(ds_extended, 'tmin', temperature_to_F=True, decimate=decimate)

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 12)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 12)

        vs = short_vals_init[short_stop - 1]
        ve = extended_vals_init[0]
        s = short_start_times[short_stop - 1]
        s1 = extended_start_times[0]

        for i in range(1, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"

            index = i + 1

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

                try:
                    val = short_vals[i-1]
                    start = short_start_times[i-1]
                    start_1 = short_start_times[i]
                except Exception as e:
                    pass
    
                stn = mpplots.StationPlot(ax, val['longitude'], val['latitude'],
                                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
        
                stn.plot_parameter('C', val['tmin'], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

                try:
                    cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], (ds_short['tmin'][i, :, :] - ds_short['tmin'][i-1, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)
                except Exception as e:
                    pass

            plt.title(f"National Weather Service Forecast\nMinimum Temperature Trend [Δ°F]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Night {index}: {start_1.strftime('%a %m/%d')} - Night {index-1}: {start.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')
            
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


        for i in range(1, extended_stop, 1):

            fname = f"B_Extended_Term_{i}.png"
            fname_7 = f"B_Extended_Term_{i+1}.png"

            index = extended_start + i

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            try:
                val = extended_vals[i-2]
                start = extended_start_times[i-2]
                start_1 = extended_start_times[i-1]
            except Exception as e:
                pass

            stn = mpplots.StationPlot(ax, val['longitude'], val['latitude'],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            if i == 1:
                try:

                    diff = ve['tmin'] - vs['tmin']
    
                    stn.plot_parameter('C', diff, color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

                    cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], (ds_extended['tmin'][0, :, :] - ds_short['tmin'][short_stop, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)
                except Exception as e:
                    pass

                plt.title(f"Night {index}: {s1.strftime('%a %m/%d')} - Night {index-1}: {s.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')

            else:

                stn.plot_parameter('C', val['tmin'], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

                try:
                    cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], (ds_extended['tmin'][i-1, :, :] - ds_extended['tmin'][i-2, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)
                except Exception as e:
                    pass
                    
                    
                plt.title(f"Night {index}: {start_1.strftime('%a %m/%d')} - Night {index-1}: {start.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')

            plt.title(f"National Weather Service Forecast\nMinimum Temperature Trend [Δ°F]", fontsize=8, fontweight='bold', loc='left')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")

        fig = plt.figure(figsize=(12,12))
        fig.set_facecolor('aliceblue')
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=1, zorder=1)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass  

        try:
            val = extended_vals[-1]
            start = extended_start_times[-2]
            start_1 = extended_start_times[-1]
        except Exception as e:
            pass

        stn = mpplots.StationPlot(ax, val['longitude'], val['latitude'],
                                         transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
        
        stn.plot_parameter('C', val['tmin'], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

        try:
            cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], (ds_extended['tmin'][-1, :, :] - ds_extended['tmin'][-2, :, :]), levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)

        except Exception as e:
            pass
            
            
        plt.title(f"Night {index + 1}: {start_1.strftime('%a %m/%d')} - Night {index}: {start.strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')

        plt.title(f"National Weather Service Forecast\nMinimum Temperature Trend [Δ°F]", fontsize=8, fontweight='bold', loc='left')

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

        fig.savefig(f"{path}/{fname_7}", bbox_inches='tight')
        print(f"Saved {fname_7} to {path_print}")


    def plot_maximum_temperature_forecast_trend(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function plots the latest available NOAA/NWS Maximum Temperature Forecast Trend. 

        Required Arguments: None

        Optional Arguments: 

        1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
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
        
        5) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        6) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        7) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        15) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        16) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        17) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        18) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        19) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        20) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        21) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        22) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        23) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        24) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 

        27) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        28) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
            This setting is only to be changed if the user wants to limit the amount of downloads from the 
            NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
            if the user wishes to download the data outside of this function. 

        29) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
            sample points to appear in good order. Example: A value of 300 plots the sample point for one row
            of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
            Lower values equal more sample points which are less spaced apart. The default value is None. If
            the default value is selected, the decimation is scaled automatically, however if the user wishes 
            to change the spacing of the sample points, then the user must edit this value. 

        30) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        31) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks   

        39) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        40) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot.      

        Return: Saves individual images to f:Weather Data/NWS Forecasts/Maximum Temperature Trend/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Maximum Temperature Trend/{reference_system}/{cwa}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state

        if gacc_region != None:
            state = gacc_region
        else:
            state = state

        levels = np.arange(-30, 31, 1)
        labels = levels[::5]

        lower = [-20, -10]
        higher = [10, 20]

        cmap = colormaps.temperature_change_colormap()

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

        western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
        if state == 'AK' or state == 'ak':
           western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
           directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'
        if state != 'AK' and state != 'ak' or gacc_region != None:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'

        sp, x, y = settings.get_sp_dims_and_textbox_coords(state)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3
    
        else:
            pass

        path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, f"Maximum Temperature Trend", reference_system, cwa)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.maxt.bin', state)

        else:
            ds_short = ds_short
            ds_extended = ds_extended

        ds = ds_short.combine_first(ds_extended)

        stop = len(ds['step'])

        times = ds_short['valid_time'].combine_first(ds_extended['valid_time'])
        times = times.to_pandas()
        times = pd.to_datetime(times)

        starts = []
        for t in times:
            time = t - timedelta(hours=12)
            starts.append(time)

        decimate = scaling.get_ndfd_decimation(western_bound, eastern_bound, southern_bound, northern_bound)
        try:
            if cwa == 'AER' or cwa == 'aer' or cwa == 'ALU' or cwa == 'alu' or cwa == 'AJK' or cwa == 'ajk':
                decimate = 30
            if cwa == 'AFG' or cwa == 'afg':
                decimate = 50
        except Exception as e:
            pass

        if state == 'SWCC' or state == 'swcc':
            decimate = 30

        vals = NDFD.ndfd_to_dataframe(ds, 'tmax', diff=True, temperature_to_F=True, decimate=decimate)

        diffs = []
        for i in range(1, stop, 1):
            p = i-1
            diff = ds['tmax'][i, :, :] - ds['tmax'][p, :, :]
            diffs.append(diff)

        for i in range(0, len(diffs), 1):

            fname = f"Image_{i}.png"
            index = i + 1

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            try:
                val = vals[i]
            except Exception as e:
                pass

            stn = mpplots.StationPlot(ax, val['longitude'], val['latitude'],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
            stn.plot_parameter('C', val['tmax'], color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=10)

            try:
                cs = ax.contourf(ds['longitude'][:, :], ds['latitude'][:, :], diffs[i], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=labels)
            except Exception as e:
                pass

            plt.title(f"National Weather Service Forecast\nMaximum Temperature Trend [Δ°F]", fontsize=8, fontweight='bold', loc='left')
            plt.title(f"Day {index +1}: {starts[index].strftime('%a %m/%d')} - Day {index}: {starts[i].strftime('%a %m/%d')}", fontsize=7, fontweight='bold', loc='right')
            
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")


class critical_firewx:

    r'''
    This class hosts the function for the NWS Critical Fire Weather Forecast
    
    '''

    def plot_critical_firewx_forecast(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa='STATE', signature_fontsize=6, stamp_fontsize=5, x=0.01, y=0.97, use_wind_gust=False, add_temperature_parameter=False, data=False, rh_short=None, ws_short=None, wdir_short=None, wgust_short=None, temp_short=None, rh_extended=None, ws_extended=None, wdir_extended=None, wgust_extended=None, temp_extended=None, low_rh_threshold=15, wind_threshold=25, temperature_threshold=75):


        r'''
        This function plots the latest available NOAA/NWS Critical Fire Weather Forecast. 

        Required Arguments: None

        Optional Arguments: 

        1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
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
        
        5) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
           This is a feature of matplotlib, as per their definition, the shrink is:
           "Fraction by which to multiply the size of the colorbar." 
           This should only be changed if the user wishes to change the size of the colorbar. 
           Preset values are called from the settings module for each state and/or gacc_region.

        6) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        7) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
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
                               

        8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        15) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

        16) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

        17) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

        18) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

        19) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        20) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        21) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        22) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        23) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        24) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
            Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 

        27) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

        28) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        29) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        30) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        31) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        32) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        33) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        34) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa='STATE'. 

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks   

        35) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        36) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        37) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        38) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.   

        39) use_wind_gust (Boolean) - Default = False. If set to True, the critical fire weather forecast will use wind gust rather than sustained wind speed. If set to False, sustained
            wind speed will be used. 

        40) add_temperature_parameter (Boolean) - Default = False. If set to True, temperature will also be a factor in determining the criteria for critical fire weather risk. 

        41) data (Boolean) - Default = False. If set to True, the user will need to pass in the datasets from outside of the function. If set to False, the function will download the datasets inside of 
            the function. 

        42) rh_short (xarray.data array) - Default=None. The short-term NDFD RH grids as an xarray.data array. This is to be used for users who want to create a lot of different types of plots with the same dataset to limit
            the amount of data requests on the server. 

        43) ws_short (xarray.data array) - Default=None. The short-term NDFD sustained wind speed grids as an xarray.data array. This is to be used for users who want to create a lot of different types of plots with the same dataset to limit the amount of data requests on the server. 

        44) wdir_short (xarray.data array) - Default=None. The short-term NDFD sustained wind direction grids as an xarray.data array. This is to be used for users who want to create a lot of different types of plots with the same dataset to limit the amount of data requests on the server. 

        45) wgust_short (xarray.data array) - Default=None. The short-term NDFD wind gust grids as an xarray.data array. This is to be used for users who want to create a lot of different types of plots with the same dataset to limit the amount of data requests on the server. 

        46) temp_short (xarray.data array) - Default=None. The short-term NDFD temperature grids as an xarray.data array. This is to be used for users who want to create a lot of different types of plots with the same dataset to limit the amount of data requests on the server. 

        47) rh_extended (xarray.data array) - Default=None. The extended NDFD RH grids as an xarray.data array. This is to be used for users who want to create a lot of different types of plots with the same dataset to limit
            the amount of data requests on the server. 

        48) ws_extended (xarray.data array) - Default=None. The extended NDFD sustained wind speed grids as an xarray.data array. This is to be used for users who want to create a lot of different types of plots with the same dataset to limit the amount of data requests on the server. 

        49) wdir_extended (xarray.data array) - Default=None. The extended NDFD sustained wind direction grids as an xarray.data array. This is to be used for users who want to create a lot of different types of plots with the same dataset to limit the amount of data requests on the server. 

        50) wgust_extended (xarray.data array) - Default=None. The extended NDFD wind gust grids as an xarray.data array. This is to be used for users who want to create a lot of different types of plots with the same dataset to limit the amount of data requests on the server. 

        51) temp_extended (xarray.data array) - Default=None. The extended NDFD temperature grids as an xarray.data array. This is to be used for users who want to create a lot of different types of plots with the same dataset to limit the amount of data requests on the server. 

        52) low_rh_threshold (Integer) - Default = 15%. The threshold for what defines low relative humidity. 

        53) wind_threshold (Integer) - Default = 25 MPH. The threshold for what defines high sustained winds and/or gusts. 

        54) temperature_threshold (Integer) - Default = 75°F. The threshold for what defines the "hot" in "hot, dry and windy."

        Return: Saves individual images to f:Weather Data/NWS Forecasts/Critical Fire Weather Forecast/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Critical Fire Weather Forecast/{reference_system}/{cwa}
        '''


        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        state = state
        cwa = cwa

        if gacc_region != None:
            state = gacc_region
        else:
            state = state

        cmap = colormaps.red_flag_warning_criteria_colormap()

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

        western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
        if state == 'AK' or state == 'ak':
           western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
           directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'
        if state != 'AK' and state != 'ak' or gacc_region != None:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'

        sp, x, y = settings.get_sp_dims_and_textbox_coords(state)

        if state =='Custom' or state == 'custom':
    
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            state = 'Custom'
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3
    
        else:
            pass

        if add_temperature_parameter == True:            
            if use_wind_gust == False:
                path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, f"Critical Fire Weather Forecast T {temperature_threshold} & RH {low_rh_threshold} & Wind Speed {wind_threshold}", reference_system, cwa)
            else:
                path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, f"Critical Fire Weather Forecast T {temperature_threshold} & RH {low_rh_threshold} & Wind Gust {wind_threshold}", reference_system, cwa)
        else:
            if use_wind_gust == False:
                path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, f"Critical Fire Weather Forecast RH {low_rh_threshold} & Wind Speed {wind_threshold}", reference_system, cwa)
            else:
                path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, f"Critical Fire Weather Forecast RH {low_rh_threshold} & Wind Gust {wind_threshold}", reference_system, cwa)            

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
            
        if data == False:

            rh_short, rh_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.rhm.bin', state)
            wdir_short, wdir_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.wdir.bin', state)
            if use_wind_gust == False:
                ws_short, ws_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.wspd.bin', state)
            else:
                wgust_short, wgust_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.wgust.bin', state)
            if add_temperature_parameter == True:
                temp_short, temp_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.temp.bin', state)
            else:
                pass
                

        else:
            rh_short=rh_short
            wdir_short=wdir_short
            if use_wind_gust == False:
                ws_short=ws_short
            else:
                wgust_short=wgust_short
            if add_temperature_parameter == True:
                temp_short=temp_short
            else:
                pass
            rh_extended=rh_extended
            wdir_extended=wdir_extended 
            if use_wind_gust == False:
                ws_extended=ws_extended
            else:
                wgust_extended=wgust_extended 
            if add_temperature_parameter == True:
                temp_extended=temp_extended
            else:
                pass

        if use_wind_gust == False:
            ws_short['si10'] = ws_short['si10'] * 2.23694
            ws_extended['si10'] = ws_extended['si10'] * 2.23694
            ws_short['u'], ws_short['v'] = mpcalc.wind_components(ws_short['si10'] * units('mph'), wdir_short['wdir10'] * units('degrees'))
            ws_extended['u'], ws_extended['v'] = mpcalc.wind_components(ws_extended['si10'] * units('mph'), wdir_extended['wdir10'] * units('degrees'))

        else:
            wgust_short['i10fg'] = wgust_short['i10fg'] * 2.23694
            try:
                wgust_extended['i10fg'] = wgust_extended['i10fg'] * 2.23694
            except Exception as e:
                pass
            wgust_short['u'], wgust_short['v'] = mpcalc.wind_components(wgust_short['i10fg'] * units('mph'), wdir_short['wdir10'] * units('degrees'))
            try:
                wgust_extended['u'], wgust_extended['v'] = mpcalc.wind_components(wgust_extended['i10fg'] * units('mph'), wdir_extended['wdir10'] * units('degrees'))
            except Exception as e:
                pass

        short_stop = len(rh_short['step'])
        extended_stop = len(rh_extended['step'])
        extended_start = short_stop
        total_count = short_stop + extended_stop

        short_times = rh_short['valid_time']
        extended_times = rh_extended['valid_time']
        short_times = short_times.to_pandas()
        extended_times = extended_times.to_pandas()

        decimate = scaling.get_ndfd_decimation(western_bound, eastern_bound, southern_bound, northern_bound)
        try:
            if cwa == 'AER' or cwa == 'aer' or cwa == 'ALU' or cwa == 'alu' or cwa == 'AJK' or cwa == 'ajk':
                decimate = 30
            if cwa == 'AFG' or cwa == 'afg':
                decimate = 50
        except Exception as e:
            pass

        if state == 'SWCC' or state == 'swcc':
            decimate = 30

        short_vals_rh = NDFD.ndfd_to_dataframe(rh_short, 'r2', decimate=decimate)
        extended_vals_rh = NDFD.ndfd_to_dataframe(rh_extended, 'r2', decimate=decimate)      
        
        if use_wind_gust == False:
            short_vals_u = NDFD.ndfd_to_dataframe(ws_short, 'u', decimate=decimate)
            extended_vals_u = NDFD.ndfd_to_dataframe(ws_extended, 'u', decimate=decimate)
            short_vals_v = NDFD.ndfd_to_dataframe(ws_short, 'v', decimate=decimate)
            extended_vals_v = NDFD.ndfd_to_dataframe(ws_extended, 'v', decimate=decimate)
            short_vals_ws = NDFD.ndfd_to_dataframe(ws_short, 'si10', decimate=decimate)
            extended_vals_ws = NDFD.ndfd_to_dataframe(ws_extended, 'si10', decimate=decimate) 
            parameter = 'si10'
        else:
            short_vals_u = NDFD.ndfd_to_dataframe(wgust_short, 'u', decimate=decimate)
            try:
                extended_vals_u = NDFD.ndfd_to_dataframe(wgust_extended, 'u', decimate=decimate) 
            except Exception as e:
                pass
            short_vals_v = NDFD.ndfd_to_dataframe(wgust_short, 'v', decimate=decimate)
            try:
                extended_vals_v = NDFD.ndfd_to_dataframe(wgust_extended, 'v', decimate=decimate)
            except Exception as e:
                pass
            short_vals_ws = NDFD.ndfd_to_dataframe(wgust_short, 'i10fg', decimate=decimate)
            try:
                extended_vals_ws = NDFD.ndfd_to_dataframe(wgust_extended, 'i10fg', decimate=decimate)
            except Exception as e:
                pass
            parameter = 'i10fg'

        if add_temperature_parameter == True:
            short_vals_temp = NDFD.ndfd_to_dataframe(temp_short, 't2m', temperature_to_F=True, decimate=decimate)
            extended_vals_temp = NDFD.ndfd_to_dataframe(temp_extended, 't2m', temperature_to_F=True, decimate=decimate) 
        else:
            pass

        short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(rh_short, 3)
        extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(rh_extended, 3)

        if add_temperature_parameter == True:
            if use_wind_gust == False:
                mask_short = (rh_short['r2'] <= low_rh_threshold) & (ws_short['si10'] >= wind_threshold) & (temp_short['t2m'] >= temperature_threshold)
                mask_extended = (rh_extended['r2'] <= low_rh_threshold) & (ws_extended['si10'] >= wind_threshold) & (temp_extended['t2m'] >= temperature_threshold)
            else:
                mask_short = (rh_short['r2'] <= low_rh_threshold) & (wgust_short['i10fg'] >= wind_threshold) & (temp_short['t2m'] >= temperature_threshold)
                try:
                    mask_extended = (rh_extended['r2'] <= low_rh_threshold) & (wgust_extended['i10fg'] >= wind_threshold) & (temp_extended['t2m'] >= temperature_threshold)
                except Exception as e:
                    pass
        else:
            if use_wind_gust == False:
                mask_short = (rh_short['r2'] <= low_rh_threshold) & (ws_short['si10'] >= wind_threshold)
                mask_extended = (rh_extended['r2'] <= low_rh_threshold) & (ws_extended['si10'] >= wind_threshold)
            else:
                mask_short = (rh_short['r2'] <= low_rh_threshold) & (wgust_short['i10fg'] >= wind_threshold)
                try:
                    mask_extended = (rh_extended['r2'] <= low_rh_threshold) & (wgust_extended['i10fg'] >= wind_threshold) 
                except Exception as e:
                    pass

        for i in range(0, short_stop, 1):

            fname = f"A_Short_Term_{i}.png"

            fig = plt.figure(figsize=(12,12))
            fig.set_facecolor('aliceblue')
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=1, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass  

            rh = short_vals_rh[i]
            u = short_vals_u[i]
            v = short_vals_v[i]
            ws = short_vals_ws[i]
            if add_temperature_parameter == True:
                temp = short_vals_temp[i]
            else:
                pass
            
            valid_time = short_end_times[i]             

            stn = mpplots.StationPlot(ax, u['longitude'], u['latitude'],
                                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)

            stn.plot_barb(u['u'], v['v'], color='black', alpha=1, zorder=10, linewidth=0.5)
            
            stn.plot_parameter('NW', ws[parameter], color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=10)
            stn.plot_parameter('SW', rh['r2'], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=10)
            if add_temperature_parameter == True:
                stn.plot_parameter('NE', temp['t2m'], color='red', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=10)

            try:
                ax.pcolormesh(mask_short['longitude'], mask_short['latitude'], mask_short[i, :, :], cmap=cmap, alpha=0.5, transform=datacrs, zorder=2)
            except Exception as e:
                pass


            if add_temperature_parameter == True:
                if use_wind_gust == False:
                    plt.title(f"National Weather Service Forecast\nCritical Fire Weather Forecast\n(T >= {temperature_threshold}[°F] & RH <= {low_rh_threshold}[%] & Sustained Wind Speed >= {wind_threshold}[MPH])", fontsize=8, fontweight='bold', loc='left')
                else:
                    plt.title(f"National Weather Service Forecast\nCritical Fire Weather Forecast\n(T >= {temperature_threshold}[°F] & RH <= {low_rh_threshold}[%] & Wind Gust >= {wind_threshold}[MPH])", fontsize=8, fontweight='bold', loc='left')
            else:
                if use_wind_gust == False:
                    plt.title(f"National Weather Service Forecast\nCritical Fire Weather Forecast\n(RH <= {low_rh_threshold}[%] & Sustained Wind Speed >= {wind_threshold}[MPH])", fontsize=8, fontweight='bold', loc='left')
                else:
                    plt.title(f"National Weather Service Forecast\nCritical Fire Weather Forecast\n(RH <= {low_rh_threshold}[%] & Wind Gust >= {wind_threshold}[MPH])", fontsize=8, fontweight='bold', loc='left')
                    
                    
            plt.title(f"Valid: {valid_time.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

            if add_temperature_parameter == True:
                if use_wind_gust == False:
                    ax.text(x, y, f"Key: Cyan = Wind Speed | Green = RH | Red = Temperature", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                else:
                    ax.text(x, y, f"Key: Cyan = Wind Gust | Green = RH | Red = Temperature", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
            else:
                if use_wind_gust == False:
                    ax.text(x, y, f"Key: Cyan = Wind Speed | Green = RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                else:
                    ax.text(x, y, f"Key: Cyan = Wind Gust | Green = RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)                

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            print(f"Saved {fname} to {path_print}")

        try:

            for i in range(0, extended_stop, 1):
    
                fname = f"B_Extended_Term_{i}.png"
    
                index = extended_start + i
    
                fig = plt.figure(figsize=(12,12))
                fig.set_facecolor('aliceblue')
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                ax.add_feature(provinces, linewidth=1, zorder=1)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                else:
                    pass
            
                if show_gacc_borders == True:
                    ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass  
    
                rh = extended_vals_rh[i]
                u = extended_vals_u[i]
                v = extended_vals_v[i]
                ws = extended_vals_ws[i]
                if add_temperature_parameter == True:
                    temp = extended_vals_temp[i]
                else:
                    pass
                
                valid_time = extended_end_times[i]             
    
                stn = mpplots.StationPlot(ax, u['longitude'], u['latitude'],
                                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
                stn.plot_barb(u['u'], v['v'], color='black', alpha=1, zorder=10, linewidth=0.5)
                
                stn.plot_parameter('NW', ws[parameter], color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=10)
                stn.plot_parameter('SW', rh['r2'], color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=10)
                if add_temperature_parameter == True:
                    stn.plot_parameter('NE', temp['t2m'], color='red', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=10)
    
                try:
                    ax.pcolormesh(mask_extended['longitude'], mask_extended['latitude'], mask_extended[i, :, :], cmap=cmap, alpha=0.5, transform=datacrs, zorder=2)
                except Exception as e:
                    pass
    
    
                if add_temperature_parameter == True:
                    if use_wind_gust == False:
                        plt.title(f"National Weather Service Forecast\nCritical Fire Weather Forecast\n(T >= {temperature_threshold}[°F] & RH <= {low_rh_threshold}[%] & Sustained Wind Speed >= {wind_threshold}[MPH])", fontsize=8, fontweight='bold', loc='left')
                    else:
                        plt.title(f"National Weather Service Forecast\nCritical Fire Weather Forecast\n(T >= {temperature_threshold}[°F] & RH <= {low_rh_threshold}[%] & Wind Gust >= {wind_threshold}[MPH])", fontsize=8, fontweight='bold', loc='left')
                else:
                    if use_wind_gust == False:
                        plt.title(f"National Weather Service Forecast\nCritical Fire Weather Forecast\n(RH <= {low_rh_threshold}[%] & Sustained Wind Speed >= {wind_threshold}[MPH])", fontsize=8, fontweight='bold', loc='left')
                    else:
                        plt.title(f"National Weather Service Forecast\nCritical Fire Weather Forecast\n(RH <= {low_rh_threshold}[%] & Wind Gust >= {wind_threshold}[MPH])", fontsize=8, fontweight='bold', loc='left')
                        
                        
                plt.title(f"Valid: {valid_time.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
    
                ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NWS/NDFD", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  
    
                if add_temperature_parameter == True:
                    if use_wind_gust == False:
                        ax.text(x, y, f"Key: Cyan = Wind Speed | Green = RH | Red = Temperature", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                    else:
                        ax.text(x, y, f"Key: Cyan = Wind Gust | Green = RH | Red = Temperature", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                else:
                    if use_wind_gust == False:
                        ax.text(x, y, f"Key: Cyan = Wind Speed | Green = RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                    else:
                        ax.text(x, y, f"Key: Cyan = Wind Gust | Green = RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)                
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                print(f"Saved {fname} to {path_print}")
        except Exception as e:
            pass



















    
