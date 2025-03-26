
r'''
This file hosts the current and past observation graphics without the 2.5km x 2.5km Real Time Mesoscale Analysis Data. 
The functions in this file only make graphics from the METAR data. 

This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS

'''

import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import numpy as np
import firewxpy.parsers as parsers
import firewxpy.colormaps as colormaps
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib.dates as md
import firewxpy.standard as standard
import firewxpy.settings as settings
import metpy.calc as mpcalc
import warnings
warnings.filterwarnings('ignore')

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from dateutil import tz
from pysolar import solar, radiation
from firewxpy.utilities import file_functions
from firewxpy.data_access import obs
from firewxpy.geometry import get_shapes
from matplotlib.patheffects import withStroke
from firewxpy.calc import Thermodynamics, unit_conversion
from metpy.interpolate import interpolate_to_grid, remove_nan_observations
from metpy.units import units

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
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

def get_cwa_coords(cwa):

    r'''
    This function returns the coordinate bounds for the Alaska NWS CWAs

    Required Arguments:

    1) cwa (String) **For Alaska Only as of the moment** The NWS CWA abbreviation. 

    Returns: Coordinate boundaries in decimal degrees

    '''

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

class gridded_observations:

    r'''
    This class hosts all the functions that use interpolation methods to make gridded data from observations. 

    '''

    def plot_relative_humidity_observations(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, df=None, mask=300000, time=None, state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, interpolation_type='cressman', shrink=0.7):
    
        r'''
        This function makes a plot of the latest Gridded Relative Humidity Observations. 
    
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
    
        26) data (Boolean) - Default = False. When set to False, the data is downloaded inside of the function.
            When making a lot of plots with the same dataset, download the data outside of the function and set
            date=True to pass the dataset into the function. 
    
        27) df (Pandas DataFrame) - Default = None. The Pandas DataFrame of the METAR data. Set df=df when 
            downloading the data outside of the function and passing it in. 
    
        28) mask (Integer or Float) - Default = 300000. This determines how many METARs show up on the graphic. 
            Lower values equal more METAR observations. Default reflects that of CONUS so when looking at a
            smaller area, you most likely would want to set this to a lower value. The value must be a positive
            non-zero number. 
    
        29) time (datetime) - Default = None. This is the time of the METAR dataset. 
            When downloading the data outside of the function and passing in the data
            into the function, set time=time. 
    
        30) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
            or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
        41) interpolation_type (String) - Default='cressman'. This determines the type of interpolation method used. 
    
            Here are the various interpolation methods:
    
            1) cressman
            2) barnes
            3) linear
            4) nearest
            5) cubic
            6) rbf
            7) natural neighbor
    
        42) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
            This is a feature of matplotlib, as per their definition, the shrink is:
            "Fraction by which to multiply the size of the colorbar." 
            This should only be changed if the user wishes to change the size of the colorbar. 
            Preset values are called from the settings module for each state and/or gacc_region.
        
        Return: Saves individual images to f:Weather Data/Observations/GRIDDED RELATIVE HUMIDITY/{state}/{reference_system}/{interpolation_type}. 
        If the user selects a cwa the path will look like this: f:Weather Data/Observations/GRIDDED RELATIVE HUMIDITY/{state}/{reference_system}/{cwa}/{interpolation_type}.
    
        '''
    
        PSAs = get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        state = state
    
        if gacc_region != None:
            state = gacc_region
        else:
            state = state
    
        reference_system = reference_system
    
        levels = np.arange(0, 102, 1)
        ticks = levels[::5]
    
        cmap = colormaps.relative_humidity_colormap()
    
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
    
        path, path_print = file_functions.obs_graphics_paths(state, gacc_region, f'Gridded Relative Humidity', reference_system, cwa, interp=True, interp_type=interpolation_type)
    
        fname = f"Gridded RH.png"
    
        try:
            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, s, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'NH' or state == 'nh' or state == 'VT' or state == 'vt' or state == 'NJ' or state == 'nj' or state == 'IN' or state == 'in' or state == 'IL' or state == 'il' or state == 'ID' or state == 'id' or state == 'AL' or state == 'al' or state == 'MS' or state == 'ms':
                western_bound = western_bound - 0.5
                eastern_bound = eastern_bound + 0.5
            shrink = settings.get_shrink(state, cwa)
            if cwa != None:
                western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
            else:
                pass
    
        except Exception as e:
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3            
    
        if data == False:
            sfc_data, metar_time = obs.get_metar_data()
        else:
            sfc_data = df 
            metar_time = time
    
        sfc_data['rh'] = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(sfc_data['air_temperature'], sfc_data['dew_point_temperature'])
    
    
        clat = (southern_bound + northern_bound) / 2
        clon = (western_bound + eastern_bound) / 2
        if state == 'AK' or state == 'ak':
            parallel = 65
        elif state == 'HI' or state == 'hi':
            parallel = 20
        else:
            parallel = 35
    
        mapcrs = ccrs.LambertConformal(central_longitude=clon, central_latitude=clat, standard_parallels=[parallel])
        
        lon = sfc_data['longitude'].values
        lat = sfc_data['latitude'].values
        rh = sfc_data['rh'].values
        
        xp, yp, _ = mapcrs.transform_points(datacrs, lon, lat).T
        x_masked, y_masked, rh_vals = remove_nan_observations(xp, yp, rh)
        x_grid, y_grid, rh_values = interpolate_to_grid(x_masked, y_masked, rh_vals, interp_type=interpolation_type)
    
        point_locs = mapcrs.transform_points(ccrs.PlateCarree(), sfc_data['longitude'].values,
                                           sfc_data['latitude'].values)
        
        sfc_data = sfc_data[mpcalc.reduce_point_density(point_locs, mask)]
    
        metar_time = metar_time.replace(tzinfo=from_zone)
        metar_time = metar_time.astimezone(to_zone)
        metar_time_utc = metar_time.astimezone(from_zone)
    
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
    
        plt.title(f"RH OBSERVATIONS (%) & INTERPOLATION [SHADED (%)]\nINTERPOLATION METHOD: {interpolation_type.upper()}", fontsize=8, fontweight='bold', loc='left')
        
        plt.title("Analysis Valid: " + metar_time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + metar_time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')
    
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: thredds.ucar.edu", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  
    
        cs = ax.contourf(x_grid, y_grid, rh_values, levels=levels, cmap=cmap, alpha=0.5)
        
        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
        stn = mpplots.StationPlot(ax, sfc_data['longitude'], sfc_data['latitude'],
                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
        stn.plot_parameter('C', sfc_data['rh'], color='black',
                                path_effects=[withStroke(linewidth=1, foreground='white')])
    
        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        print(f"Saved {fname} to {path_print}")    

    def plot_temperature_observations(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, df=None, mask=300000, time=None, state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, interpolation_type='cressman', shrink=0.7):
    
        r'''
        This function makes a plot of the latest Gridded Temperature Observations. 
    
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
    
        26) data (Boolean) - Default = False. When set to False, the data is downloaded inside of the function.
            When making a lot of plots with the same dataset, download the data outside of the function and set
            date=True to pass the dataset into the function. 
    
        27) df (Pandas DataFrame) - Default = None. The Pandas DataFrame of the METAR data. Set df=df when 
            downloading the data outside of the function and passing it in. 
    
        28) mask (Integer or Float) - Default = 300000. This determines how many METARs show up on the graphic. 
            Lower values equal more METAR observations. Default reflects that of CONUS so when looking at a
            smaller area, you most likely would want to set this to a lower value. The value must be a positive
            non-zero number. 
    
        29) time (datetime) - Default = None. This is the time of the METAR dataset. 
            When downloading the data outside of the function and passing in the data
            into the function, set time=time. 
    
        30) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
            or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
        41) interpolation_type (String) - Default='cressman'. This determines the type of interpolation method used. 
    
            Here are the various interpolation methods:
    
            1) cressman
            2) barnes
            3) linear
            4) nearest
            5) cubic
            6) rbf
            7) natural neighbor
    
        42) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
            This is a feature of matplotlib, as per their definition, the shrink is:
            "Fraction by which to multiply the size of the colorbar." 
            This should only be changed if the user wishes to change the size of the colorbar. 
            Preset values are called from the settings module for each state and/or gacc_region.
        
        Return: Saves individual images to f:Weather Data/Observations/GRIDDED TEMPERATURE/{state}/{reference_system}/{interpolation_type}. 
        If the user selects a cwa the path will look like this: f:Weather Data/Observations/GRIDDED TEMPERATURE/{state}/{reference_system}/{cwa}/{interpolation_type}.
    
        '''
    
        PSAs = get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        state = state
    
        if gacc_region != None:
            state = gacc_region
        else:
            state = state
    
        reference_system = reference_system

        if state == 'AK' or state == 'ak':

            if utc_time.month >= 4 and utc_time.month <= 10:
                levels = np.arange(0, 81, 1)
            else:
                levels = np.arange(-30, 51, 1)

        else:

            if utc_time.month >= 4 and utc_time.month <= 10:
                levels = np.arange(10, 111, 1)
            else:
                levels = np.arange(-10, 91, 1)
        
        
        ticks = levels[::5]
    
        cmap = colormaps.temperature_colormap()
    
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
    
        path, path_print = file_functions.obs_graphics_paths(state, gacc_region, f'Gridded Temperature', reference_system, cwa, interp=True, interp_type=interpolation_type)
    
        fname = f"Gridded TEMPERATURE.png"
    
        try:
            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, s, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'NH' or state == 'nh' or state == 'VT' or state == 'vt' or state == 'NJ' or state == 'nj' or state == 'IN' or state == 'in' or state == 'IL' or state == 'il' or state == 'ID' or state == 'id' or state == 'AL' or state == 'al' or state == 'MS' or state == 'ms':
                western_bound = western_bound - 0.5
                eastern_bound = eastern_bound + 0.5
            shrink = settings.get_shrink(state, cwa)
            if cwa != None:
                western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
            else:
                pass
    
        except Exception as e:
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3            
    
        if data == False:
            sfc_data, metar_time = obs.get_metar_data()
        else:
            sfc_data = df 
            metar_time = time
    
    
        clat = (southern_bound + northern_bound) / 2
        clon = (western_bound + eastern_bound) / 2
        if state == 'AK' or state == 'ak':
            parallel = 65
        elif state == 'HI' or state == 'hi':
            parallel = 20
        else:
            parallel = 35
    
        mapcrs = ccrs.LambertConformal(central_longitude=clon, central_latitude=clat, standard_parallels=[parallel])
        
        lon = sfc_data['longitude'].values
        lat = sfc_data['latitude'].values
        sfc_data['air_temperature_F'] = unit_conversion.celsius_to_fahrenheit(sfc_data['air_temperature'])
        temp = sfc_data['air_temperature_F'].values
        
        xp, yp, _ = mapcrs.transform_points(datacrs, lon, lat).T
        x_masked, y_masked, temp_vals = remove_nan_observations(xp, yp, temp)
        x_grid, y_grid, temp_values = interpolate_to_grid(x_masked, y_masked, temp_vals, interp_type=interpolation_type)
    
        point_locs = mapcrs.transform_points(ccrs.PlateCarree(), sfc_data['longitude'].values,
                                           sfc_data['latitude'].values)
        
        sfc_data = sfc_data[mpcalc.reduce_point_density(point_locs, mask)]
    
        metar_time = metar_time.replace(tzinfo=from_zone)
        metar_time = metar_time.astimezone(to_zone)
        metar_time_utc = metar_time.astimezone(from_zone)
    
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
    
        plt.title(f"TEMP OBSERVATIONS (°F) & INTERPOLATION [SHADED (°F)]\nINTERPOLATION METHOD: {interpolation_type.upper()}", fontsize=8, fontweight='bold', loc='left')
        
        plt.title("Analysis Valid: " + metar_time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + metar_time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')
    
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: thredds.ucar.edu", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  
    
        cs = ax.contourf(x_grid, y_grid, temp_values, levels=levels, cmap=cmap, alpha=0.5, extend='both')
        
        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
        stn = mpplots.StationPlot(ax, sfc_data['longitude'], sfc_data['latitude'],
                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
        stn.plot_parameter('C', sfc_data['air_temperature_F'], color='black',
                                path_effects=[withStroke(linewidth=1, foreground='white')])
    
        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        print(f"Saved {fname} to {path_print}")    


    def plot_wind_observations(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, df=None, mask=300000, time=None, state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, interpolation_type='cressman', shrink=0.7):
    
        r'''
        This function makes a plot of the latest Gridded Wind Observations. 
    
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
    
        26) data (Boolean) - Default = False. When set to False, the data is downloaded inside of the function.
            When making a lot of plots with the same dataset, download the data outside of the function and set
            date=True to pass the dataset into the function. 
    
        27) df (Pandas DataFrame) - Default = None. The Pandas DataFrame of the METAR data. Set df=df when 
            downloading the data outside of the function and passing it in. 
    
        28) mask (Integer or Float) - Default = 300000. This determines how many METARs show up on the graphic. 
            Lower values equal more METAR observations. Default reflects that of CONUS so when looking at a
            smaller area, you most likely would want to set this to a lower value. The value must be a positive
            non-zero number. 
    
        29) time (datetime) - Default = None. This is the time of the METAR dataset. 
            When downloading the data outside of the function and passing in the data
            into the function, set time=time. 
    
        30) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
            or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
        41) interpolation_type (String) - Default='cressman'. This determines the type of interpolation method used. 
    
            Here are the various interpolation methods:
    
            1) cressman
            2) barnes
            3) linear
            4) nearest
            5) cubic
            6) rbf
            7) natural neighbor
    
        42) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
            This is a feature of matplotlib, as per their definition, the shrink is:
            "Fraction by which to multiply the size of the colorbar." 
            This should only be changed if the user wishes to change the size of the colorbar. 
            Preset values are called from the settings module for each state and/or gacc_region.
        
        Return: Saves individual images to f:Weather Data/Observations/GRIDDED WIND/{state}/{reference_system}/{interpolation_type}. 
        If the user selects a cwa the path will look like this: f:Weather Data/Observations/GRIDDED WIND/{state}/{reference_system}/{cwa}/{interpolation_type}.
    
        '''
    
        PSAs = get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        state = state
    
        if gacc_region != None:
            state = gacc_region
        else:
            state = state
    
        reference_system = reference_system

        levels = np.arange(0, 81, 1)       
        ticks = levels[::5]
    
        cmap = colormaps.cross_section_wind_speed()
    
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
    
        path, path_print = file_functions.obs_graphics_paths(state, gacc_region, f'Gridded WIND', reference_system, cwa, interp=True, interp_type=interpolation_type)
    
        fname = f"Gridded WIND.png"
    
        try:
            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, s, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
            if state == 'NH' or state == 'nh' or state == 'VT' or state == 'vt' or state == 'NJ' or state == 'nj' or state == 'IN' or state == 'in' or state == 'IL' or state == 'il' or state == 'ID' or state == 'id' or state == 'AL' or state == 'al' or state == 'MS' or state == 'ms':
                western_bound = western_bound - 0.5
                eastern_bound = eastern_bound + 0.5
            shrink = settings.get_shrink(state, cwa)
            if cwa != None:
                western_bound, eastern_bound, southern_bound, northern_bound = get_cwa_coords(cwa)
            else:
                pass
    
        except Exception as e:
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3            
    
        if data == False:
            sfc_data, metar_time = obs.get_metar_data()
        else:
            sfc_data = df 
            metar_time = time
    
    
        clat = (southern_bound + northern_bound) / 2
        clon = (western_bound + eastern_bound) / 2
        if state == 'AK' or state == 'ak':
            parallel = 65
        elif state == 'HI' or state == 'hi':
            parallel = 20
        else:
            parallel = 35
    
        mapcrs = ccrs.LambertConformal(central_longitude=clon, central_latitude=clat, standard_parallels=[parallel])
        
        lon = sfc_data['longitude'].values
        lat = sfc_data['latitude'].values
        sfc_data['wind_speed_mph'] = sfc_data['wind_speed'] * 1.15078
        wind = sfc_data['wind_speed_mph'].values

        sfc_data['eastward_wind_mph'] = sfc_data['eastward_wind'] * 1.15078
        sfc_data['northward_wind_mph'] = sfc_data['northward_wind'] * 1.15078
        
        xp, yp, _ = mapcrs.transform_points(datacrs, lon, lat).T
        x_masked, y_masked, wind_vals = remove_nan_observations(xp, yp, wind)
        x_grid, y_grid, wind_values = interpolate_to_grid(x_masked, y_masked, wind_vals, interp_type=interpolation_type)
    
        point_locs = mapcrs.transform_points(ccrs.PlateCarree(), sfc_data['longitude'].values,
                                           sfc_data['latitude'].values)
        
        sfc_data = sfc_data[mpcalc.reduce_point_density(point_locs, mask)]
    
        metar_time = metar_time.replace(tzinfo=from_zone)
        metar_time = metar_time.astimezone(to_zone)
        metar_time_utc = metar_time.astimezone(from_zone)
    
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
    
        plt.title(f"WIND OBSERVATIONS (MPH) & INTERPOLATION [SHADED (MPH)]\nINTERPOLATION METHOD: {interpolation_type.upper()}", fontsize=8, fontweight='bold', loc='left')
        
        plt.title("Analysis Valid: " + metar_time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + metar_time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')
    
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: thredds.ucar.edu", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  
    
        cs = ax.contourf(x_grid, y_grid, wind_values, levels=levels, cmap=cmap, alpha=0.5, extend='max')
        
        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
        stn = mpplots.StationPlot(ax, sfc_data['longitude'], sfc_data['latitude'],
                             transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
    
        stn.plot_parameter('E', sfc_data['wind_speed_mph'], color='black',
                                path_effects=[withStroke(linewidth=1, foreground='white')])

        stn.plot_barb(sfc_data['eastward_wind_mph'], sfc_data['northward_wind_mph'], color='white')
    
        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        print(f"Saved {fname} to {path_print}")   

class scatter_observations:

    r'''
    This class hosts functions that plot observations as a scatter plot format. 

    '''

    def plot_relative_humidity(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, df=None, time=None, state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function makes a plot of the latest Relative Humidity observations. 
    
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
    
        26) data (Boolean) - Default = False. When set to False, the data is downloaded inside of the function.
            When making a lot of plots with the same dataset, download the data outside of the function and set
            date=True to pass the dataset into the function. 
    
        27) df (Pandas DataFrame) - Default = None. The Pandas DataFrame of the METAR data. Set df=df when 
            downloading the data outside of the function and passing it in. 
    
        28) time (datetime) - Default = None. This is the time of the METAR dataset. 
            When downloading the data outside of the function and passing in the data
            into the function, set time=time. 
    
        29) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
            or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 
    
        30) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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
    
        31) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 
    
        32) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 
    
        33) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.
    
        34) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.
    
        35) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.
    
        36) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.
    
        37) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 
    
            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks        
    
        38) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        39) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        Return: Saves individual images to f:Weather Data/Observations/SCATTER PLOT OBS RH/{state}/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/Observations/SCATTER PLOT OBS RH/{state}/{reference_system}/{cwa}
    
    
        '''
    
        PSAs = get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        state = state
    
        if gacc_region != None:
            state = gacc_region
        else:
            state = state
    
        reference_system = reference_system
        levels = np.arange(0, 102, 1)
        ticks = levels[::5]

        cmap = colormaps.relative_humidity_colormap()
    
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
    
        path, path_print = file_functions.obs_graphics_paths(state, gacc_region, f'SCATTER PLOT OBS RH', reference_system, cwa)
    
        fname = f"Relative Humidity.png"
    
        try:
            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
        except Exception as e:
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3            
    
        if data == False:
            sfc_data, metar_time = obs.get_metar_data()
        else:
            sfc_data = df 
            metar_time = time
    
        sfc_data['rh'] = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(sfc_data['air_temperature'], sfc_data['dew_point_temperature'])
    
        locs = pd.DataFrame()
        
        locs['longitude'] = sfc_data['longitude'].values
        locs['latitude'] = sfc_data['latitude'].values
    
        locs = locs.to_numpy()

        metar_time = metar_time.replace(tzinfo=from_zone)
        metar_time = metar_time.astimezone(to_zone)
        metar_time_utc = metar_time.astimezone(from_zone)
    
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
    
        plt.title("RELATIVE HUMIDITY OBSERVATIONS [%]", fontsize=8, fontweight='bold', loc='left')
        
        plt.title("Analysis Valid: " + metar_time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + metar_time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')
    
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: thredds.ucar.edu", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  
    
        cs = ax.scatter(sfc_data['longitude'], sfc_data['latitude'], c=sfc_data['rh'], transform=datacrs, cmap=cmap, vmin=0, vmax=100, alpha=0.5)
        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        print(f"Saved {fname} to {path_print}")


    def plot_temperature(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, df=None, time=None, state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function makes a plot of the latest Temperature observations. 
    
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
    
        26) data (Boolean) - Default = False. When set to False, the data is downloaded inside of the function.
            When making a lot of plots with the same dataset, download the data outside of the function and set
            date=True to pass the dataset into the function. 
    
        27) df (Pandas DataFrame) - Default = None. The Pandas DataFrame of the METAR data. Set df=df when 
            downloading the data outside of the function and passing it in. 
    
        28) time (datetime) - Default = None. This is the time of the METAR dataset. 
            When downloading the data outside of the function and passing in the data
            into the function, set time=time. 
    
        29) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
            or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 
    
        30) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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
    
        31) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 
    
        32) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 
    
        33) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.
    
        34) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.
    
        35) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.
    
        36) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.
    
        37) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 
    
            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks        
    
        38) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        39) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        Return: Saves individual images to f:Weather Data/Observations/SCATTER PLOT OBS TEMPERATURE/{state}/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/Observations/SCATTER PLOT OBS TEMPERATURE/{state}/{reference_system}/{cwa}
    
    
        '''
    
        PSAs = get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        state = state
    
        if gacc_region != None:
            state = gacc_region
        else:
            state = state
    
        reference_system = reference_system
        if state == 'AK' or state == 'ak':

            if utc_time.month >= 4 and utc_time.month <= 10:
                levels = np.arange(0, 81, 1)
                vmin = 0
                vmax = 80
            else:
                levels = np.arange(-30, 51, 1)
                vmin = -30
                vmax = 50

        else:

            if utc_time.month >= 4 and utc_time.month <= 10:
                levels = np.arange(10, 111, 1)
                vmin = 10
                vmax = 110
            else:
                levels = np.arange(-10, 91, 1)
                vmin = -10
                vmax = 90
        
        
        ticks = levels[::5]
    
        cmap = colormaps.temperature_colormap_alt()
    
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
    
        path, path_print = file_functions.obs_graphics_paths(state, gacc_region, f'SCATTER PLOT OBS TEMPERATURE', reference_system, cwa)
    
        fname = f"Temperature.png"
    
        try:
            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
        except Exception as e:
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3            
    
        if data == False:
            sfc_data, metar_time = obs.get_metar_data()
        else:
            sfc_data = df 
            metar_time = time
    
        sfc_data['air_temperature_F'] = unit_conversion.celsius_to_fahrenheit(sfc_data['air_temperature'])
    
        locs = pd.DataFrame()
        
        locs['longitude'] = sfc_data['longitude'].values
        locs['latitude'] = sfc_data['latitude'].values
    
        locs = locs.to_numpy()

        metar_time = metar_time.replace(tzinfo=from_zone)
        metar_time = metar_time.astimezone(to_zone)
        metar_time_utc = metar_time.astimezone(from_zone)
    
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
    
        plt.title("TEMPERATURE OBSERVATIONS [°F]", fontsize=8, fontweight='bold', loc='left')
        
        plt.title("Analysis Valid: " + metar_time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + metar_time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')
    
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: thredds.ucar.edu", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  
    
        cs = ax.scatter(sfc_data['longitude'], sfc_data['latitude'], c=sfc_data['air_temperature_F'], transform=datacrs, cmap=cmap, vmin=vmin, vmax=vmax, alpha=0.5)
        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        print(f"Saved {fname} to {path_print}")


    def plot_wind_speed(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, df=None, time=None, state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):


        r'''
        This function makes a plot of the latest Wind Speed observations. 
    
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
    
        26) data (Boolean) - Default = False. When set to False, the data is downloaded inside of the function.
            When making a lot of plots with the same dataset, download the data outside of the function and set
            date=True to pass the dataset into the function. 
    
        27) df (Pandas DataFrame) - Default = None. The Pandas DataFrame of the METAR data. Set df=df when 
            downloading the data outside of the function and passing it in. 
    
        28) time (datetime) - Default = None. This is the time of the METAR dataset. 
            When downloading the data outside of the function and passing in the data
            into the function, set time=time. 
    
        29) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
            or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
            changed to None. 
    
        30) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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
    
        31) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 
    
        32) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 
    
        33) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.
    
        34) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.
    
        35) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.
    
        36) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.
    
        37) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
            For a view of the entire state - set cwa=None. 
    
            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            
            2) ALU - NWS Anchorage West Domain
            
            3) AJK - NWS Juneau
            
            4) AFG - NWS Fairbanks        
    
        38) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        39) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        Return: Saves individual images to f:Weather Data/Observations/SCATTER PLOT OBS WIND SPEED/{state}/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/Observations/SCATTER PLOT OBS WIND SPEED/{state}/{reference_system}/{cwa}
    
    
        '''
    
        PSAs = get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        state = state
    
        if gacc_region != None:
            state = gacc_region
        else:
            state = state
    
        reference_system = reference_system        
        levels = np.arange(0, 81, 1)
        ticks = levels[::5]
    
        cmap = colormaps.cross_section_wind_speed()
    
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
    
        path, path_print = file_functions.obs_graphics_paths(state, gacc_region, f'SCATTER PLOT OBS WIND SPEED', reference_system, cwa)
    
        fname = f"Wind Speed.png"
    
        try:
            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
        except Exception as e:
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3            
    
        if data == False:
            sfc_data, metar_time = obs.get_metar_data()
        else:
            sfc_data = df 
            metar_time = time
    
        sfc_data['wind_speed_mph'] = sfc_data['wind_speed'] * 1.15078
    
        locs = pd.DataFrame()
        
        locs['longitude'] = sfc_data['longitude'].values
        locs['latitude'] = sfc_data['latitude'].values
    
        locs = locs.to_numpy()

        metar_time = metar_time.replace(tzinfo=from_zone)
        metar_time = metar_time.astimezone(to_zone)
        metar_time_utc = metar_time.astimezone(from_zone)
    
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
    
        plt.title("WIND SPEED OBSERVATIONS [MPH]", fontsize=8, fontweight='bold', loc='left')
        
        plt.title("Analysis Valid: " + metar_time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + metar_time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')
    
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: thredds.ucar.edu", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  
    
        cs = ax.scatter(sfc_data['longitude'], sfc_data['latitude'], c=sfc_data['wind_speed_mph'], transform=datacrs, cmap=cmap, vmin=0, vmax=80, alpha=0.5)
        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        print(f"Saved {fname} to {path_print}")


class METAR_Observations:

    r'''
    This class hosts the functions that plot METAR observations and make daily weather summaries for METAR observations

    '''


    def plot_observations_map(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, df=None, mask=3, time=None, state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5):
    
        r'''
        This function makes a plot of the latest METAR observations. 
    
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
    
        26) data (Boolean) - Default = False. When set to False, the data is downloaded inside of the function.
            When making a lot of plots with the same dataset, download the data outside of the function and set
            date=True to pass the dataset into the function. 
    
        27) df (Pandas DataFrame) - Default = None. The Pandas DataFrame of the METAR data. Set df=df when 
            downloading the data outside of the function and passing it in. 
    
        28) mask (Integer or Float) - Default = 3. This determines how many METARs show up on the graphic. 
            Lower values equal more METAR observations. Default reflects that of CONUS so when looking at a
            smaller area, you most likely would want to set this to a lower value. The value must be a positive
            non-zero number. 
    
        29) time (datetime) - Default = None. This is the time of the METAR dataset. 
            When downloading the data outside of the function and passing in the data
            into the function, set time=time. 
    
        30) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
            If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
            or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
            acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
        Return: Saves individual images to f:Weather Data/Observations/METAR MAP/{state}/{reference_system}. 
        If the user selects a cwa the path will look like this: f:Weather Data/Observations/METAR MAP/{state}/{reference_system}/{cwa}
    
    
        '''
    
        PSAs = get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        state = state
    
        if gacc_region != None:
            state = gacc_region
        else:
            state = state
    
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
    
        path, path_print = file_functions.obs_graphics_paths(state, gacc_region, f'METAR MAP', reference_system, cwa)
    
        fname = f"METAR Map.png"
    
        try:
            western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
        except Exception as e:
            western_bound = western_bound
            eastern_bound = eastern_bound
            southern_bound = southern_bound
            northern_bound = northern_bound
            x1=x1
            y1=y1
            x2=x2
            y2=y2
            x3=x3
            y3=y3            
    
        if data == False:
            sfc_data, metar_time = obs.get_metar_data()
        else:
            sfc_data = df 
            metar_time = time
    
        sfc_data['rh'] = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(sfc_data['air_temperature'], sfc_data['dew_point_temperature'])
    
        locs = pd.DataFrame()
        
        locs['longitude'] = sfc_data['longitude'].values
        locs['latitude'] = sfc_data['latitude'].values
    
        locs = locs.to_numpy()
    
        sfc_data = sfc_data[mpcalc.reduce_point_density(locs, mask)]
    
        metar_time = metar_time.replace(tzinfo=from_zone)
        metar_time = metar_time.astimezone(to_zone)
        metar_time_utc = metar_time.astimezone(from_zone)
    
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
    
        plt.title("METAR OBSERVATIONS", fontsize=8, fontweight='bold', loc='left')
        
        plt.title("Analysis Valid: " + metar_time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + metar_time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')
    
        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: thredds.ucar.edu", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  
    
        stn = mpplots.StationPlot(ax, sfc_data['longitude'], sfc_data['latitude'],
                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=10, clip_on=True)
        
        
        stn.plot_parameter('W', unit_conversion.celsius_to_fahrenheit(sfc_data['air_temperature']), color='red',
                          path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_parameter('SSW', unit_conversion.celsius_to_fahrenheit(sfc_data['dew_point_temperature']), color='blue',
                          path_effects=[withStroke(linewidth=1, foreground='black')])
        
        stn.plot_symbol('C', sfc_data['cloud_coverage'], mpplots.sky_cover)
        
        stn.plot_parameter('E', sfc_data['rh'], color='darkgreen',
                            path_effects=[withStroke(linewidth=1, foreground='black')])
    
        stn.plot_text('NNW', sfc_data['station_id'], color='black',
                            path_effects=[withStroke(linewidth=1, foreground='white')])    
        
        stn.plot_barb(sfc_data['eastward_wind'], sfc_data['northward_wind'])
    
        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        print(f"Saved {fname} to {path_print}")
    
    
    def graphical_daily_summary(station_id):
    
    
        r'''
        This function creates a graphical daily weather summary and solar information for the previous day's ASOS observations at any particular ASOS site. 
    
        Required Arguments: 1) station_id (String) - The 4-letter station identifier of the ASOS station
    
        Optional Arguments: None
    
        Returns: A saved figure to the observations folder showing a graphical daily weather summary and solar information for the previous day's ASOS observations. 
                 The parameters on this daily weather summary are: 1) Temperature
                                                                   2) Relative Humidity
                                                                   3) Wind Speed
                                                                   4) Solar Elevation Angle
                                                                   5) Solar Radiation
        
    
        '''
    
        station_id = station_id.upper()
    
        df, maximum_temperature, maximum_temperature_time, maximum_temperature_time_local, minimum_temperature, minimum_temperature_time, minimum_temperature_time_local, minimum_relative_humidity, minimum_relative_humidity_time, minimum_relative_humidity_time_local, maximum_relative_humidity, maximum_relative_humidity_time, maximum_relative_humidity_time_local, maximum_wind_speed, wind_dir, maximum_wind_speed_time, maximum_wind_speed_time_local, maximum_wind_gust, maximum_wind_gust_time, maximum_wind_gust_time_local, station_id, previous_day_utc = obs.previous_day_weather_summary(station_id)
    
        time = df['date_time']
        time = pd.to_datetime(time)
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        start = time.iloc[0]
        year = start.year
        month = start.month
        day = start.day
        
        start = datetime(year, month, day, tzinfo=to_zone)
        start_summer_solstice = datetime(year, 6, 21, tzinfo=to_zone)
        start_winter_solstice = datetime(year, 12, 21, tzinfo=to_zone)
        start_equinox = datetime(year, 3, 21, tzinfo=to_zone)
        times_list = [start + timedelta(minutes=i *15) for i in range(24*4)]
        times_list_summer_solstice = [start_summer_solstice + timedelta(minutes=i *15) for i in range(24*4)]
        times_list_winter_solstice = [start_winter_solstice + timedelta(minutes=i *15) for i in range(24*4)]
        times_list_equinox = [start_equinox + timedelta(minutes=i *15) for i in range(24*4)]
        
        temperature = df['air_temperature']
        relative_humidity = df['relative_humidity']
        wind_speed = df['wind_speed']
        latitude = df['latitude'].iloc[0]
        longitude = df['longitude'].iloc[0]
        
        
        solar_elevation = [solar.get_altitude(latitude, longitude, t) for t in times_list]
        solar_radiation = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list, solar_elevation)]
        
        solar_elevation_summer = [solar.get_altitude(latitude, longitude, t) for t in times_list_summer_solstice]
        solar_radiation_summer = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list_summer_solstice, solar_elevation_summer)]
        
        solar_elevation_winter = [solar.get_altitude(latitude, longitude, t) for t in times_list_winter_solstice]
        solar_radiation_winter = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list_winter_solstice, solar_elevation_winter)]
        
        solar_elevation_equinox = [solar.get_altitude(latitude, longitude, t) for t in times_list_equinox]
        solar_radiation_equinox = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list_equinox, solar_elevation_equinox)]
        
        max_elevation = np.nanmax(solar_elevation)
        min_elevation = np.nanmin(solar_elevation)
    
        max_elevation_summer = np.nanmax(solar_elevation_summer)
        min_elevation_summer = np.nanmin(solar_elevation_summer)
    
        max_elevation_winter = np.nanmax(solar_elevation_winter)
        min_elevation_winter = np.nanmin(solar_elevation_winter)
    
        max_elevation_equinox = np.nanmax(solar_elevation_equinox)
        min_elevation_equinox = np.nanmin(solar_elevation_equinox)
    
        max_rad = np.nanmax(solar_radiation)
    
        diff_ele_ss = max_elevation - max_elevation_summer
        diff_ele_ws = max_elevation - max_elevation_winter
        diff_ele_e = max_elevation - max_elevation_equinox
    
    
        plt.style.use('seaborn-v0_8-darkgrid')
        
        
        fig = plt.figure(figsize=(10,12))
        fig.suptitle(station_id + " Daily Weather Summary | Date: " + previous_day_utc.strftime('%m/%d/%Y'), color='white', fontsize=28, fontweight='bold')
        
        if latitude >= 0 and longitude <= 0:
            fig.text(0.125, 0.925, "Station Latitude: " + str(round(abs(latitude), 1)) + " (\N{DEGREE SIGN}N) | Station Longitude: " + str(round(abs(longitude), 1)) + " (\N{DEGREE SIGN}W)", color='white', fontsize=20, fontweight='bold')
        if latitude >= 0 and longitude > 0:
            fig.text(0.125, 0.925, "Station Latitude: " + str(round(abs(latitude), 1)) + " (\N{DEGREE SIGN}N) | Station Longitude: " + str(round(abs(longitude), 1)) + " (\N{DEGREE SIGN}E)", color='white', fontsize=20, fontweight='bold')
        if latitude < 0 and longitude <= 0:
            fig.text(0.125, 0.925, "Station Latitude: " + str(round(abs(latitude), 1)) + " (\N{DEGREE SIGN}S) | Station Longitude: " + str(round(abs(longitude), 1)) + " (\N{DEGREE SIGN}W)", color='white', fontsize=20, fontweight='bold')
        if latitude < 0 and longitude > 0:
            fig.text(0.125, 0.925, "Station Latitude: " + str(round(abs(latitude), 1)) + " (\N{DEGREE SIGN}S) | Station Longitude: " + str(round(abs(longitude), 1)) + " (\N{DEGREE SIGN}E)", color='white', fontsize=20, fontweight='bold')
        
        
        
        fig.set_facecolor('gray')
        gs = gridspec.GridSpec(3, 2)
        
        
        ax0 = fig.add_subplot(gs[0:1, 0:1])
        ax0.plot(time, temperature, c='red')
        ax0.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
        ax0.set_ylim(int(round(minimum_temperature - 2, 0)), int(round(maximum_temperature + 2, 0)))
        ax0.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
        ax0.set_ylabel("Temperature (\N{DEGREE SIGN}F)", color='white', fontsize=8, fontweight='bold')
        ax0.set_title("Temperature", color='white', fontsize=11, fontweight='bold')
        ax0.tick_params(axis='x', colors='white')
        ax0.tick_params(axis='y', colors='white')
        
        ax1 = fig.add_subplot(gs[1:2, 0:1])
        ax1.plot(time, relative_humidity, c='green')
        ax1.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
        ax1.set_ylim(minimum_relative_humidity - 5, maximum_relative_humidity + 5)
        ax1.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
        ax1.set_ylabel("Relative Humidity (%)", color='white', fontsize=8, fontweight='bold')
        ax1.set_title("Relative Humidity", color='white', fontsize=11, fontweight='bold')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        
        ax2 = fig.add_subplot(gs[2:3, 0:1])
        ax2.plot(time, wind_speed, c='purple')
        ax2.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
        ax2.set_ylim(0, maximum_wind_speed + 2)
        ax2.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
        ax2.set_ylabel("Wind Speed (MPH)", color='white', fontsize=8, fontweight='bold')
        ax2.set_title("Wind Speed", color='white', fontsize=11, fontweight='bold')
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')
        
        ax3 = fig.add_subplot(gs[0:1, 1:2])
        ax3.plot(times_list, solar_elevation, c='orange', label=start.strftime('%m/%d'), alpha=0.5)
        ax3.plot(times_list, solar_elevation_summer, c='red', label='Summer Solstice', alpha=0.5)
        ax3.plot(times_list, solar_elevation_winter, c='blue', label='Winter Solstice', alpha=0.5)
        ax3.plot(times_list, solar_elevation_equinox, c='magenta', label='Equinox', alpha=0.5)
        ax3.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
        ax3.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
        ax3.set_ylabel("Solar Elevation Angle (Degrees)", color='white', fontsize=8, fontweight='bold')
        ax3.set_title("Solar Elevation Angle", color='white', fontsize=11, fontweight='bold')
        ax3.axhline(0, c='black', linestyle='--', linewidth=2)
        fig.text(0.55, 0.855, "Elevation Angle > 0 = Day\nElevation Angle < 0 = Night", fontsize=9, fontweight='bold')
        ax3.tick_params(axis='x', colors='white')
        ax3.tick_params(axis='y', colors='white')
        ax3.legend(loc=(0.3,0.01), prop={'size': 8})
        
        ax4 = fig.add_subplot(gs[1:2, 1:2])
        ax4.plot(times_list, solar_radiation, c='orange')
        ax4.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
        ax4.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
        ax4.set_ylabel("Solar Radiation (W/m^2)", color='white', fontsize=8, fontweight='bold')
        ax4.set_title("Solar Radiation", color='white', fontsize=11, fontweight='bold')
        ax4.tick_params(axis='x', colors='white')
        ax4.tick_params(axis='y', colors='white')
    
    
        try:
            maximum_temperature = int(round(maximum_temperature, 0))
            maximum_temperature = str(maximum_temperature)
            maximum_temperature_time_local = maximum_temperature_time_local.strftime('%H:%M Local')
            maximum_temperature_time = maximum_temperature_time.strftime('%H:%M UTC')
        except Exception as e:
            maximum_temperature = 'NA'
            maximum_temperature_time_local = 'NA'
            maximum_temperature_time = 'NA'
        try:
            minimum_temperature = int(round(minimum_temperature, 0))
            minimum_temperature = str(minimum_temperature)
            minimum_temperature_time_local = minimum_temperature_time_local.strftime('%H:%M Local')
            minimum_temperature_time = minimum_temperature_time.strftime('%H:%M UTC')
        except Exception as e:
            minimum_temperature = 'NA'
            minimum_temperature_time_local = 'NA'
            minimum_temperature_time = 'NA'
        try:
            maximum_relative_humidity = int(round(maximum_relative_humidity, 0))
            maximum_relative_humidity = str(maximum_relative_humidity)
            maximum_relative_humidity_time_local = maximum_relative_humidity_time_local.strftime('%H:%M Local')
            maximum_relative_humidity_time = maximum_relative_humidity_time.strftime('%H:%M UTC')
        except Exception as e:
            maximum_relative_humidity = 'NA'
            maximum_relative_humidity_time_local = 'NA'
            maximum_relative_humidity_time = 'NA'
        try:
            minimum_relative_humidity = int(round(minimum_relative_humidity, 0))
            minimum_relative_humidity = str(minimum_relative_humidity)
            minimum_relative_humidity_time_local = minimum_relative_humidity_time_local.strftime('%H:%M Local')
            minimum_relative_humidity_time = minimum_relative_humidity_time.strftime('%H:%M UTC')
        except Exception as e:
            minimum_relative_humidity = 'NA'
            minimum_relative_humidity_time_local = 'NA'
            minimum_relative_humidity_time = 'NA'
        try:
            maximum_wind_speed = int(round(maximum_wind_speed, 0))
            maximum_wind_speed = str(maximum_wind_speed)
            maximum_wind_speed_time_local = maximum_wind_speed_time_local.strftime('%H:%M Local')
            maximum_wind_speed_time = maximum_wind_speed_time.strftime('%H:%M UTC')
        except Exception as e:
            maximum_wind_speed = 'NA'
            maximum_wind_speed_time_local = 'NA'
            maximum_wind_speed_time = 'NA'
        try:
            maximum_wind_gust = int(round(maximum_wind_gust, 0))
            maximum_wind_gust = str(maximum_wind_gust)
            maximum_wind_gust_time_local = maximum_wind_gust_time_local.strftime('%H:%M Local')
            maximum_wind_gust_time = maximum_wind_gust_time.strftime('%H:%M UTC')
        except Exception as e:
            maximum_wind_gust = 'NA'
            maximum_wind_gust_time_local = 'NA'
            maximum_wind_gust_time = 'NA'
    
        if diff_ele_e >= 0:
            sym='+'
        else:
            sym=''
    
        if max_elevation >= 0:
            sym1 = '+'
        else:
            sym1 = ''
    
        if min_elevation >= 0:
            sym2 = '+'
        else:
            sym2 = ''
    
        if max_elevation_equinox >= 0:
            sym3 = '+'
        else:
            sym3 = ''
    
        if max_elevation_winter >= 0:
            sym4 = '+'
        else:
            sym4 = ''
    
        fig.text(0.55, 0.115, "Maximum Temperature: " +maximum_temperature +" [\N{DEGREE SIGN}F] " + maximum_temperature_time_local + " ("+ maximum_temperature_time+")\n\nMinimum Temperature: " + minimum_temperature +" [\N{DEGREE SIGN}F] "+ minimum_temperature_time_local + " ("+ minimum_temperature_time+")\n\nMaximum RH: " + maximum_relative_humidity +" [%] "+ maximum_relative_humidity_time_local + " ("+ maximum_relative_humidity_time +")\n\nMinimum RH: " + minimum_relative_humidity +" [%] "+ minimum_relative_humidity_time_local + " ("+ minimum_relative_humidity_time +")\n\nMaximum Wind Speed: " + maximum_wind_speed +" [MPH] "+ maximum_wind_speed_time_local + " ("+ maximum_wind_speed_time +")\n\nMaximum Wind Gust: " + maximum_wind_gust +" [MPH] "+ maximum_wind_gust_time_local + " ("+ maximum_wind_gust_time +")\n\nMaximum Elevation: "+sym1+""+ str(round(max_elevation, 1)) + " [\N{DEGREE SIGN} From Horizon]\n\nMinimum Elevation: "+sym2+""+ str(round(min_elevation, 1)) + " [\N{DEGREE SIGN} From Horizon]\n\nMaximum Elevation Difference:\nSummer Solstice: "+str(round(diff_ele_ss,1))+" [\N{DEGREE SIGN}] | Max Elevation: "+sym1+""+str(round(max_elevation_summer,1))+" [\N{DEGREE SIGN} From Horizon]\nEquinox: "+sym+""+str(round(diff_ele_e,1))+" [\N{DEGREE SIGN}] | Max Elevation: "+sym3+""+str(round(max_elevation_equinox,1))+" [\N{DEGREE SIGN} From Horizon]\nWinter Solstice: "+str(round(diff_ele_ws,1))+" [\N{DEGREE SIGN}] | Max Elevation: "+sym4+""+str(round(max_elevation_winter,1))+" [\N{DEGREE SIGN} From Horizon]\n\nMaximum Solar Radiation: " + str(round(max_rad, 1)) + " (W/m^2)", color='black', fontsize=8, fontweight='bold', bbox=props, zorder=6)
    
        
        fig.text(0.27, 0.07, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=14, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)    
    
        file_functions.save_daily_weather_summary(fig, station_id)

    
