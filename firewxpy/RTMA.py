import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import metpy.calc as mpcalc
import numpy as np
import firewxpy.parsers as parsers
import firewxpy.geometry as geometry
import firewxpy.colormaps as colormaps
import pandas as pd
import firewxpy.settings as settings
import firewxpy.standard as standard
import firewxpy.dims as dims
import warnings
warnings.filterwarnings('ignore')


from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from dateutil import tz
from firewxpy.calc import scaling, Thermodynamics, unit_conversion
from firewxpy.utilities import file_functions
from metpy.units import units
from firewxpy.data_access import RTMA

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

def plot_relative_humidity(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=False, ds=None, time=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, low_rh_threshold=15, high_rh_threshold=80, show_low_high_thresholds=False):

    r'''
    This function plots the latest available Real Time Mesoscale Analysis (RTMA) Relative Humidity. 

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


    26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
        sample points are displayed on the graphic. Default setting is True. If the user wants 
        to hide the sample point values and only have the contour shading, this value will need 
        to be changed to False. 

    27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
        Default setting is a 10 point fontsize. 

    28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
        A value of 0 is completely transparent while a value of 1 is completely opaque. 
        Default setting is 0.5. 

    29) data (Boolean) - Default = False. If set to True, the user must download the data outside of the function and pass it in. 
        If set to False, the data is downloaded inside of the function. 

    30) ds (xarray.data array) - Default = None. If the user downloads the data outside of the function and passes it in, then ds must
        be changed from ds=None to ds=ds. 

    31) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
        If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
        it is recommended to download the data outside of the function and change time=None to time=time for example. 

    32) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
        or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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

    41) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    42) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    43) low_rh_threshold (Integer) -  Default = 15%. The low relative humidity threshold. 
    
    44) high_rh_threshold (Integer) - Default = 80%. The high relative humidity threshold. 

    45) show_low_high_thresholds (Boolean) - Default = False. When set to True, the low and high threshold contours are shown. 
        When set to False, those threshold contours are hidden. 

    Return: Saves individual images to f:Weather Data/RTMA/RTMA RH {With or Without Contours}/{reference_system}. 
    If the user selects a cwa the path will look like this: f:Weather Data/RTMA/RTMA RH {With or Without Contours}/{reference_system}/{cwa}
    
    '''
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if show_low_high_thresholds == True:
        text = 'With Contour Thresholds'
    else:
        text = 'Without Contour Thresholds'


    state = state

    if gacc_region != None:
        state = gacc_region
    else:
        state = state

    levels = np.arange(0, 102, 1)
    ticks = levels[::5]

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

    path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f'RTMA RH {text}', reference_system, cwa)

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
        ds, ds_24, time, time_24 = RTMA.get_rtma_datasets(state, utc_time)
    else:
        ds = ds
        time = time

    temp = ds['tmp2m']
    dwpt = ds['dpt2m']
    lat = ds['lat']
    lon = ds['lon']
    temp = temp - 273.15
    dwpt = dwpt - 273.15
    
    rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)

    time = time.replace(tzinfo=from_zone)
    time = time.astimezone(to_zone)
    time_utc = time.astimezone(from_zone)

    decimate = scaling.get_nomads_decimation(western_bound, eastern_bound, southern_bound, northern_bound, True)

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])
        
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

    plt.title("RTMA Relative Humidity (%)", fontsize=8, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')

    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
    ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

    cs = ax.contourf(lon, lat, rh[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=levels, cmap=cmap, alpha=0.5, zorder=1)

    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

    if show_low_high_thresholds == True:
        sp, x, y = settings.get_sp_dims_and_textbox_coords(state)
        ax.text(x, y, f"Red Contour Line: RH = {low_rh_threshold}% | Blue Contour Line: RH = {high_rh_threshold}%", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
        c_low = ax.contour(lon, lat, mpcalc.smooth_gaussian(rh[0, :, :] * units('percent'), n=8), levels=[low_rh_threshold], colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_low, levels=[low_rh_threshold], inline=True, fontsize=8, rightside_up=True)  
    
        c_high = ax.contour(lon, lat, mpcalc.smooth_gaussian(rh[0, :, :] * units('percent'), n=8), levels=[high_rh_threshold], colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_high, levels=[high_rh_threshold], inline=True, fontsize=8, rightside_up=True) 
    else:
        pass

    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=7, clip_on=True)

    rh = rh[0, ::decimate, ::decimate].to_numpy().flatten()

    stn.plot_parameter('C', rh, color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=7)

    fig.savefig(f"{path}/RTMA RH.png", bbox_inches='tight')
    print(f"Saved RTMA RH graphic to {path_print}")


def plot_temperature(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=False, ds=None, time=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, low_temperature_threshold=32, high_temperature_threshold=100, show_low_high_thresholds=False):

    r'''
    This function plots the latest available Real Time Mesoscale Analysis (RTMA) Temperature. 

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

    26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
        sample points are displayed on the graphic. Default setting is True. If the user wants 
        to hide the sample point values and only have the contour shading, this value will need 
        to be changed to False. 

    27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
        Default setting is a 10 point fontsize. 

    28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
        A value of 0 is completely transparent while a value of 1 is completely opaque. 
        Default setting is 0.5. 

    29) data (Boolean) - Default = False. If set to True, the user must download the data outside of the function and pass it in. 
        If set to False, the data is downloaded inside of the function. 

    30) ds (xarray.data array) - Default = None. If the user downloads the data outside of the function and passes it in, then ds must
        be changed from ds=None to ds=ds. 

    31) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
        If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
        it is recommended to download the data outside of the function and change time=None to time=time for example. 

    32) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
        or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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

    41) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    42) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    43) low_temperature_threshold (Integer) -  Default = 32F. The low temperature threshold.  

    44) high_temperature_threshold (Integer) - Default = 100F. The high temperature threshold. 

    45) show_low_high_thresholds (Boolean) - Default = False. When set to True, the low and high contours are shown. 
        When set to False, those threshold contours are hidden. 

    Return: Saves individual images to f:Weather Data/RTMA/RTMA Temperature {With or Without Contours}/{reference_system}. 
    If the user selects a cwa the path will look like this: f:Weather Data/RTMA/RTMA Temperature {With or Without Contours}/{reference_system}/{cwa}
    
    '''
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if show_low_high_thresholds == True:
        text = 'With Contour Thresholds'
    else:
        text = 'Without Contour Thresholds'

    state = state

    if gacc_region != None:
        state = gacc_region
    else:
        state = state

    if utc_time.month >= 5 and utc_time.month <= 9:
        levels = np.arange(30, 111, 1)
    if utc_time.month == 4 or utc_time.month == 10:
        levels = np.arange(10, 101, 1)
    if utc_time.month >= 11 or utc_time.month <= 3:
        levels = np.arange(-20, 91, 1)
    ticks = levels[::5]

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

    path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f'RTMA Temperature {text}', reference_system, cwa)

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
        ds, ds_24, time, time_24 = RTMA.get_rtma_datasets(state, utc_time)
    else:
        ds = ds
        time = time

    temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'])
    lat = ds['lat']
    lon = ds['lon']

    time = time.replace(tzinfo=from_zone)
    time = time.astimezone(to_zone)
    time_utc = time.astimezone(from_zone)

    decimate = scaling.get_nomads_decimation(western_bound, eastern_bound, southern_bound, northern_bound, True)

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])
        
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

    plt.title("RTMA Temperature (°F)", fontsize=8, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')

    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
    ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

    cs = ax.contourf(lon, lat, temp[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=levels, cmap=cmap, alpha=0.5, zorder=1, extend='both')

    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

    if show_low_high_thresholds == True:
        sp, x, y = settings.get_sp_dims_and_textbox_coords(state)
        ax.text(x, y, f"Red Contour Line: T = {low_temperature_threshold}°F | Blue Contour Line: T = {high_temperature_threshold}°F", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
        c_low = ax.contour(lon, lat, mpcalc.smooth_gaussian(temp[0, :, :] * units('degF'), n=8), levels=[low_temperature_threshold], colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_low, levels=[low_temperature_threshold], inline=True, fontsize=8, rightside_up=True)  
    
        c_high = ax.contour(lon, lat, mpcalc.smooth_gaussian(temp[0, :, :] * units('degF'), n=8), levels=[high_temperature_threshold], colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_high, levels=[high_temperature_threshold], inline=True, fontsize=8, rightside_up=True) 
    else:
        pass

    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=7, clip_on=True)

    temp = temp[0, ::decimate, ::decimate].to_numpy().flatten()

    stn.plot_parameter('C', temp, color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=7)

    fig.savefig(f"{path}/RTMA Temperature.png", bbox_inches='tight')
    print(f"Saved RTMA Temperature graphic to {path_print}")

def plot_dewpoint(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=False, ds=None, time=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, low_dwpt_threshold=10, high_dwpt_threshold=60, show_low_high_thresholds=False):

    r'''
    This function plots the latest available Real Time Mesoscale Analysis (RTMA) Dewpoint. 

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

    26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
        sample points are displayed on the graphic. Default setting is True. If the user wants 
        to hide the sample point values and only have the contour shading, this value will need 
        to be changed to False. 

    27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
        Default setting is a 10 point fontsize. 

    28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
        A value of 0 is completely transparent while a value of 1 is completely opaque. 
        Default setting is 0.5. 

    29) data (Boolean) - Default = False. If set to True, the user must download the data outside of the function and pass it in. 
        If set to False, the data is downloaded inside of the function. 

    30) ds (xarray.data array) - Default = None. If the user downloads the data outside of the function and passes it in, then ds must
        be changed from ds=None to ds=ds. 

    31) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
        If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
        it is recommended to download the data outside of the function and change time=None to time=time for example. 

    32) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
        or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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

    37) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    39) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

    40) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
        For a view of the entire state - set cwa=None. 

        NWS CWA Abbreviations:

        1) AER - NWS Anchorage East Domain
        
        2) ALU - NWS Anchorage West Domain
        
        3) AJK - NWS Juneau
        
        4) AFG - NWS Fairbanks        

    41) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    42) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    43) low_rh_threshold (Integer) -  Default = 15%. The low dewpoint threshold. 
    
    44) high_rh_threshold (Integer) - Default = 80%. The high dewpoint threshold. 

    45) show_low_high_thresholds (Boolean) - Default = False. When set to True, the low and high threshold contours are shown. 
        When set to False, those threshold contours are hidden. 

    Return: Saves individual images to f:Weather Data/RTMA/RTMA Dewpoint {With or Without Contours}/{reference_system}. 
    If the user selects a cwa the path will look like this: f:Weather Data/RTMA/RTMA Dewpoint {With or Without Contours}/{reference_system}/{cwa}
    
    '''
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if show_low_high_thresholds == True:
        text = 'With Contour Thresholds'
    else:
        text = 'Without Contour Thresholds'


    state = state

    if gacc_region != None:
        state = gacc_region
    else:
        state = state


    levels = np.arange(-10, 71, 1)
    ticks = levels[::5]

    cmap = colormaps.dew_point_colormap()

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

    path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f'RTMA Dewpoint {text}', reference_system, cwa)

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
        ds, ds_24, time, time_24 = RTMA.get_rtma_datasets(state, utc_time)
    else:
        ds = ds
        time = time

    dwpt = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['dpt2m'])
    lat = ds['lat']
    lon = ds['lon']

    time = time.replace(tzinfo=from_zone)
    time = time.astimezone(to_zone)
    time_utc = time.astimezone(from_zone)

    decimate = scaling.get_nomads_decimation(western_bound, eastern_bound, southern_bound, northern_bound, True)

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])
        
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

    plt.title("RTMA Dewpoint (°F)", fontsize=8, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')

    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
    ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

    cs = ax.contourf(lon, lat, dwpt[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=levels, cmap=cmap, alpha=0.5, zorder=1, extend='both')

    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

    if show_low_high_thresholds == True:
        sp, x, y = settings.get_sp_dims_and_textbox_coords(state)
        ax.text(x, y, f"Red Contour Line: DWPT = {low_dwpt_threshold}°F | Blue Contour Line: DWPT = {high_dwpt_threshold}°F", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
        c_low = ax.contour(lon, lat, mpcalc.smooth_gaussian(dwpt[0, :, :] * units('degF'), n=8), levels=[low_dwpt_threshold], colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_low, levels=[low_dwpt_threshold], inline=True, fontsize=8, rightside_up=True)  
    
        c_high = ax.contour(lon, lat, mpcalc.smooth_gaussian(dwpt[0, :, :] * units('degF'), n=8), levels=[high_dwpt_threshold], colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_high, levels=[high_dwpt_threshold], inline=True, fontsize=8, rightside_up=True) 
    else:
        pass

    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=7, clip_on=True)

    dwpt = dwpt[0, ::decimate, ::decimate].to_numpy().flatten()

    stn.plot_parameter('C', dwpt, color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=7)

    fig.savefig(f"{path}/RTMA Dewpoint.png", bbox_inches='tight')
    print(f"Saved RTMA Dewpoint graphic to {path_print}")

def plot_total_cloud_cover(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=False, ds=None, time=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, low_threshold=20, high_threshold=80, show_low_high_thresholds=False):

    r'''
    This function plots the latest available Real Time Mesoscale Analysis (RTMA) Total Cloud Cover (%). 

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

    26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
        sample points are displayed on the graphic. Default setting is True. If the user wants 
        to hide the sample point values and only have the contour shading, this value will need 
        to be changed to False. 

    27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
        Default setting is a 10 point fontsize. 

    28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
        A value of 0 is completely transparent while a value of 1 is completely opaque. 
        Default setting is 0.5. 

    29) data (Boolean) - Default = False. If set to True, the user must download the data outside of the function and pass it in. 
        If set to False, the data is downloaded inside of the function. 

    30) ds (xarray.data array) - Default = None. If the user downloads the data outside of the function and passes it in, then ds must
        be changed from ds=None to ds=ds. 

    31) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
        If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
        it is recommended to download the data outside of the function and change time=None to time=time for example. 

    32) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
        or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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

    41) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    42) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    43) low_threshold (Integer) -  Default = 20%.  
    
    44) high_threshold (Integer) - Default = 80%. 

    45) show_low_high_thresholds (Boolean) - Default = False. When set to True, the low and high threshold contours are shown. 
        When set to False, those threshold contours are hidden. 

    Return: Saves individual images to f:Weather Data/RTMA/RTMA Total Cloud Cover {With or Without Contours}/{reference_system}. 
    If the user selects a cwa the path will look like this: f:Weather Data/RTMA/RTMA Total Cloud Cover {With or Without Contours}/{reference_system}/{cwa}
    
    '''
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if show_low_high_thresholds == True:
        text = 'With Contour Thresholds'
    else:
        text = 'Without Contour Thresholds'


    state = state

    if gacc_region != None:
        state = gacc_region
    else:
        state = state


    levels = np.arange(0, 102, 1)
    ticks = levels[::5]

    cmap = colormaps.cloud_cover_colormap()

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

    path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f'RTMA Total Cloud Cover {text}', reference_system, cwa)

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
        ds, ds_24, time, time_24 = RTMA.get_rtma_datasets(state, utc_time)
    else:
        ds = ds
        time = time

    tccl = ds['tcdcclm']
    lat = ds['lat']
    lon = ds['lon']

    time = time.replace(tzinfo=from_zone)
    time = time.astimezone(to_zone)
    time_utc = time.astimezone(from_zone)

    decimate = scaling.get_nomads_decimation(western_bound, eastern_bound, southern_bound, northern_bound, True)

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])
        
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

    plt.title("RTMA Total Cloud Cover (%)", fontsize=8, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')

    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
    ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

    cs = ax.contourf(lon, lat, tccl[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=levels, cmap=cmap, alpha=0.5, zorder=1)

    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

    if show_low_high_thresholds == True:
        sp, x, y = settings.get_sp_dims_and_textbox_coords(state)
        ax.text(x, y, f"Blue Contour Line: {low_threshold}% | Gray Contour Line: {high_threshold}%", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
        c_low = ax.contour(lon, lat, mpcalc.smooth_gaussian(tccl[0, :, :] * units('percent'), n=8), levels=[low_threshold], colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_low, levels=[low_threshold], inline=True, fontsize=8, rightside_up=True)  
    
        c_high = ax.contour(lon, lat, mpcalc.smooth_gaussian(tccl[0, :, :] * units('percent'), n=8), levels=[high_threshold], colors='gray', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_high, levels=[high_threshold], inline=True, fontsize=8, rightside_up=True) 
    else:
        pass

    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=7, clip_on=True)

    tccl = tccl[0, ::decimate, ::decimate].to_numpy().flatten()

    stn.plot_parameter('C', tccl, color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=7)

    fig.savefig(f"{path}/RTMA Total Cloud Cover.png", bbox_inches='tight')
    print(f"Saved RTMA Total Cloud Cover graphic to {path_print}")

def plot_wind_speed(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=False, ds=None, time=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, sample_points='barbs'):

    r'''
    This function plots the latest available Real Time Mesoscale Analysis (RTMA) Wind Speed. 

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

    26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
        sample points are displayed on the graphic. Default setting is True. If the user wants 
        to hide the sample point values and only have the contour shading, this value will need 
        to be changed to False. 

    27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
        Default setting is a 10 point fontsize. 

    28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
        A value of 0 is completely transparent while a value of 1 is completely opaque. 
        Default setting is 0.5. 

    29) data (Boolean) - Default = False. If set to True, the user must download the data outside of the function and pass it in. 
        If set to False, the data is downloaded inside of the function. 

    30) ds (xarray.data array) - Default = None. If the user downloads the data outside of the function and passes it in, then ds must
        be changed from ds=None to ds=ds. 

    31) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
        If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
        it is recommended to download the data outside of the function and change time=None to time=time for example. 

    32) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
        or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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

    41) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    42) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    43) sample_points (String) - Default = 'barbs'. The type of sample point. When set to 'barbs' wind barbs will be displayed. 
        To display the numbers, change the setting to 'values'. 

    Return: Saves individual images to f:Weather Data/RTMA/RTMA Wind Speed {Barbs or Values}/{reference_system}. 
    If the user selects a cwa the path will look like this: f:Weather Data/RTMA/RTMA Wind Speed {Barbs or Values}/{reference_system}/{cwa}
    
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


    levels = np.arange(0, 71, 1)
    ticks = levels[::5]

    cmap = colormaps.cross_section_wind_speed()

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

    path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f'RTMA Wind Speed {sample_points}', reference_system, cwa)

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
        ds, ds_24, time, time_24 = RTMA.get_rtma_datasets(state, utc_time)
    else:
        ds = ds
        time = time

    ws = unit_conversion.meters_per_second_to_mph(ds['wind10m'])
    lat = ds['lat']
    lon = ds['lon']
    u = unit_conversion.meters_per_second_to_mph(ds['ugrd10m'])
    v = unit_conversion.meters_per_second_to_mph(ds['vgrd10m'])    

    time = time.replace(tzinfo=from_zone)
    time = time.astimezone(to_zone)
    time_utc = time.astimezone(from_zone)

    decimate = scaling.get_nomads_decimation(western_bound, eastern_bound, southern_bound, northern_bound, True)

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])
        
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

    plt.title("RTMA Wind Speed (MPH)", fontsize=8, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
    ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

    cs = ax.contourf(lon, lat, ws[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=levels, cmap=cmap, alpha=0.5, zorder=1, extend='max')

    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)


    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=7, clip_on=True)

    if sample_points == 'values':
        ws = ws[0, ::decimate, ::decimate].to_numpy().flatten()
        stn.plot_parameter('C', ws, color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=7)

    if sample_points == 'barbs':
        stn.plot_barb(u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='white', length=4.5, alpha=1, zorder=7, linewidth=0.8)        

    fig.savefig(f"{path}/RTMA Wind Speed.png", bbox_inches='tight')
    print(f"Saved RTMA Wind Speed graphic to {path_print}")

def plot_critical_firewx(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=False, ds=None, time=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, use_wind_gust=False, add_temperature_threshold=False, low_rh_threshold=15, high_wind_threshold=25, high_temperature_threshold=75):

    r'''
    This function plots the latest available Real Time Mesoscale Analysis (RTMA) Critical Fire Weather. 

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

    26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
        sample points are displayed on the graphic. Default setting is True. If the user wants 
        to hide the sample point values and only have the contour shading, this value will need 
        to be changed to False. 

    27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
        Default setting is a 10 point fontsize. 

    28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
        A value of 0 is completely transparent while a value of 1 is completely opaque. 
        Default setting is 0.5. 

    29) data (Boolean) - Default = False. If set to True, the user must download the data outside of the function and pass it in. 
        If set to False, the data is downloaded inside of the function. 

    30) ds (xarray.data array) - Default = None. If the user downloads the data outside of the function and passes it in, then ds must
        be changed from ds=None to ds=ds. 

    31) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
        If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
        it is recommended to download the data outside of the function and change time=None to time=time for example. 

    32) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
        or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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

    41) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    42) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    43) sample_points (String) - Default = 'barbs'. The type of sample point. When set to 'barbs' wind barbs will be displayed. 
        To display the numbers, change the setting to 'values'. 

    Return: Saves individual images to f:Weather Data/RTMA/RTMA Critical Fire Weather/{reference_system}. 
    If the user selects a cwa the path will look like this: f:Weather Data/RTMA/RTMA Critical Fire Weather/{reference_system}/{cwa}
    
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


    levels = np.arange(0, 71, 1)
    ticks = levels[::5]

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

        if add_temperature_threshold == True:            
            if use_wind_gust == False:
                path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f"RTMA Critical Fire Weather T {high_temperature_threshold} & RH {low_rh_threshold} & Wind Speed {high_wind_threshold}", reference_system, cwa)
            else:
                path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f"RTMA Critical Fire Weather T {high_temperature_threshold} & RH {low_rh_threshold} & Wind Gust {high_wind_threshold}", reference_system, cwa)
        else:
            if use_wind_gust == False:
                path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f"RTMA Critical Fire Weather RH {low_rh_threshold} & Wind Speed {high_wind_threshold}", reference_system, cwa)
            else:
                path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f"RTMA Critical Fire Weather RH {low_rh_threshold} & Wind Gust {high_wind_threshold}", reference_system, cwa)            

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

    sp, x, y = settings.get_sp_dims_and_textbox_coords(state)

    if data == False:
        ds, ds_24, time, time_24 = RTMA.get_rtma_datasets(state, utc_time)
    else:
        ds = ds
        time = time

    ws = unit_conversion.meters_per_second_to_mph(ds['wind10m'])
    lat = ds['lat']
    lon = ds['lon']
    u = unit_conversion.meters_per_second_to_mph(ds['ugrd10m'])
    v = unit_conversion.meters_per_second_to_mph(ds['vgrd10m'])
    gust = unit_conversion.meters_per_second_to_mph(ds['gust10m'])
    temp = ds['tmp2m']
    dwpt = ds['dpt2m']
    temp = temp - 273.15
    dwpt = dwpt - 273.15
    
    rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)

    temp_F = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'])

    if use_wind_gust == False:
        if add_temperature_threshold == False:
            mask = (rh <= low_rh_threshold) & (ws >= high_wind_threshold)
        else:
            mask = (rh <= low_rh_threshold) & (ws >= high_wind_threshold) & (temp_F >= high_temperature_threshold)
    else:
        wdir = ds['wdir10m']
        u, v = mpcalc.wind_components(gust * units('mph'), wdir * units('degrees'))
        if add_temperature_threshold == False:
            mask = (rh <= low_rh_threshold) & (gust >= high_wind_threshold)
        else:
            mask = (rh <= low_rh_threshold) & (gust >= high_wind_threshold) & (temp_F >= high_temperature_threshold)        

    time = time.replace(tzinfo=from_zone)
    time = time.astimezone(to_zone)
    time_utc = time.astimezone(from_zone)

    decimate = scaling.get_nomads_decimation(western_bound, eastern_bound, southern_bound, northern_bound, True)
    if state == 'CONUS' or state == 'conus':
        decimate = decimate + 20
    else:
        pass

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])
        
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

    if use_wind_gust == False:
        if add_temperature_threshold == False:
            plt.title(f"RTMA Critical Fire Weather Conditions (Shaded Red)\nRH <= {low_rh_threshold} % & Sustained Wind Speed >= {high_wind_threshold} MPH", fontsize=8, fontweight='bold', loc='left')
        else:
            plt.title(f"RTMA Critical Fire Weather Conditions (Shaded Red)\n T >= {high_temperature_threshold} °F & RH <= {low_rh_threshold} % & Sustained Wind Speed >= {high_wind_threshold} MPH", fontsize=8, fontweight='bold', loc='left')
    else:
        if add_temperature_threshold == False:
            plt.title(f"RTMA Critical Fire Weather Conditions (Shaded Red)\nRH <= {low_rh_threshold} % & Wind Gust >= {high_wind_threshold} MPH", fontsize=8, fontweight='bold', loc='left')
        else:
            plt.title(f"RTMA Critical Fire Weather Conditions (Shaded Red)\n T >= {high_temperature_threshold} °F & RH <= {low_rh_threshold} % & Wind Gust >= {high_wind_threshold} MPH", fontsize=8, fontweight='bold', loc='left')        
            
    plt.title("Analysis Valid: " + time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')

    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
    ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

    if add_temperature_threshold == True:
        if use_wind_gust == False:
            ax.text(x, y, f"Key: Cyan = Wind Speed | Green = RH | Red = Temperature", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
        else:
            ax.text(x, y, f"Key: Cyan = Wind Gust | Green = RH | Red = Temperature", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
    else:
        if use_wind_gust == False:
            ax.text(x, y, f"Key: Cyan = Wind Speed | Green = RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
        else:
            ax.text(x, y, f"Key: Cyan = Wind Gust | Green = RH", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)   

    try:
        ax.pcolormesh(mask['lon'], mask['lat'], mask[0, :, :], cmap=cmap, zorder=1, alpha=0.5, transform=datacrs)
    except Exception as e:
        pass

    if state == 'CONUS' or state == 'conus':
        size = 6
    else:
        size = 8

    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=size, zorder=7, clip_on=True)

    if use_wind_gust == False:
        speed = ws[0, ::decimate, ::decimate].to_numpy().flatten()
    else:
        speed = gust[0, ::decimate, ::decimate].to_numpy().flatten()

    rh = rh[0, ::decimate, ::decimate].to_numpy().flatten()
        
    stn.plot_parameter('NW', speed, color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    stn.plot_parameter('SW', rh, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    if add_temperature_threshold == True:
        temp_F = temp_F[0, ::decimate, ::decimate].to_numpy().flatten()
            
        stn.plot_parameter('NE', temp_F, color='red', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)        

    stn.plot_barb(u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='black', length=4.5, alpha=1, zorder=7, linewidth=0.8)        

    fig.savefig(f"{path}/RTMA Critical Fire Weather.png", bbox_inches='tight')
    print(f"Saved RTMA Critical Fire Weather graphic to {path_print}")

def plot_24_hour_relative_humidity_comparison(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=False, ds=None, ds_24=None, time=None, time_24=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, show_low_high_thresholds=False):

    r'''
    This function plots the latest available 24-Hour RTMA RH Comparison. 

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


    26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
        sample points are displayed on the graphic. Default setting is True. If the user wants 
        to hide the sample point values and only have the contour shading, this value will need 
        to be changed to False. 

    27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
        Default setting is a 10 point fontsize. 

    28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
        A value of 0 is completely transparent while a value of 1 is completely opaque. 
        Default setting is 0.5. 

    29) data (Boolean) - Default = False. If set to True, the user must download the data outside of the function and pass it in. 
        If set to False, the data is downloaded inside of the function. 

    30) ds (xarray.data array) - Default = None. If the user downloads the data outside of the function and passes it in, then ds must
        be changed from ds=None to ds=ds. 

    31) ds_24 (xarray.data array) - Default = None. This is the dataset from 24 hours ago to make the comparison. 
        If the user downloads the data outside of the function and passes it in, then ds must be changed from ds=None to ds=ds. 

    32) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
        Set time=time when downloading the data outside of the function. 
         
    33) time_24 (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. This
        is the time for the RTMA from 24-hours ago. Set time_24=time_24 when downloading the data outside of the function. 

    34) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
        or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
        changed to None. 

    35) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

    36) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    37) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    38) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    39) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    40) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    41) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

    42) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
        For a view of the entire state - set cwa=None. 

        NWS CWA Abbreviations:

        1) AER - NWS Anchorage East Domain
        
        2) ALU - NWS Anchorage West Domain
        
        3) AJK - NWS Juneau
        
        4) AFG - NWS Fairbanks        

    43) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    44) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    45) show_low_high_thresholds (Boolean) - Default = False. When set to True, the low and high threshold contours are shown. 
        When set to False, those threshold contours are hidden. 

    Return: Saves individual images to f:Weather Data/RTMA/24 HOUR RTMA RH COMPARISON {With or Without Contours}/{reference_system}. 
    If the user selects a cwa the path will look like this: f:Weather Data/RTMA/24 HOUR RTMA RH COMPARISON {With or Without Contours}/{reference_system}/{cwa}
    
    '''
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if show_low_high_thresholds == True:
        text = 'With Contour Thresholds'
    else:
        text = 'Without Contour Thresholds'


    state = state

    if gacc_region != None:
        state = gacc_region
    else:
        state = state

    levels = np.arange(-60, 61, 1)
    ticks = levels[::5]

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

    path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f'24 HOUR RTMA RH COMPARISON {text}', reference_system, cwa)

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
        ds, ds_24, time, time_24 = RTMA.get_rtma_datasets(state, utc_time)
    else:
        ds = ds
        ds_24 = ds_24
        time = time
        time_24 = time_24

    temp = ds['tmp2m']
    dwpt = ds['dpt2m']
    lat = ds['lat']
    lon = ds['lon']
    temp = temp - 273.15
    dwpt = dwpt - 273.15

    temp_24 = ds_24['tmp2m']
    dwpt_24 = ds_24['dpt2m']
    lat_24 = ds_24['lat']
    lon_24 = ds_24['lon']
    temp_24 = temp_24 - 273.15
    dwpt_24 = dwpt_24 - 273.15
    
    rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
    rh_24 = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_24, dwpt_24)

    diff = rh[0, :, :] - rh_24[0, :, :]

    time = time.replace(tzinfo=from_zone)
    time = time.astimezone(to_zone)
    time_utc = time.astimezone(from_zone)

    time_24 = time_24.replace(tzinfo=from_zone)
    time_24 = time_24.astimezone(to_zone)
    time_24_utc = time_24.astimezone(from_zone)

    decimate = scaling.get_nomads_decimation(western_bound, eastern_bound, southern_bound, northern_bound, True)

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])
        
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

    plt.title("24-Hour RTMA Relative Humidity Comparison (Δ%)", fontsize=8, fontweight='bold', loc='left')
    
    plt.title("End: " + time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_utc.strftime('%H:00 UTC')+")\nStart: "+ time_24.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_24_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')

    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
    ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

    cs = ax.contourf(lon, lat, diff, 
                     transform=ccrs.PlateCarree(), levels=levels, cmap=cmap, alpha=0.5, zorder=1, extend='both')

    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

    if show_low_high_thresholds == True:
        c_low = ax.contour(lon, lat, mpcalc.smooth_gaussian(diff * units('percent'), n=8), levels=[-60, -40, -20], colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_low, levels=[-60, -40, -20], inline=True, fontsize=8, rightside_up=True)  
    
        c_high = ax.contour(lon, lat, mpcalc.smooth_gaussian(diff * units('percent'), n=8), levels=[20, 40, 60], colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_high, levels=[20, 40, 60], inline=True, fontsize=8, rightside_up=True) 
    else:
        pass

    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=7, clip_on=True)

    diff = diff[::decimate, ::decimate].to_numpy().flatten()

    stn.plot_parameter('C', diff, color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=7)

    fig.savefig(f"{path}/24-Hour RTMA TEMPERATURE Comparison.png", bbox_inches='tight')
    print(f"Saved 24-Hour RTMA TEMPERATURE Comparison graphic to {path_print}")

def plot_24_hour_dew_point_comparison(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=False, ds=None, ds_24=None, time=None, time_24=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, show_low_high_thresholds=False):

    r'''
    This function plots the latest available 24-Hour RTMA Dew Point Comparison. 

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


    26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
        sample points are displayed on the graphic. Default setting is True. If the user wants 
        to hide the sample point values and only have the contour shading, this value will need 
        to be changed to False. 

    27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
        Default setting is a 10 point fontsize. 

    28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
        A value of 0 is completely transparent while a value of 1 is completely opaque. 
        Default setting is 0.5. 

    29) data (Boolean) - Default = False. If set to True, the user must download the data outside of the function and pass it in. 
        If set to False, the data is downloaded inside of the function. 

    30) ds (xarray.data array) - Default = None. If the user downloads the data outside of the function and passes it in, then ds must
        be changed from ds=None to ds=ds. 

    31) ds_24 (xarray.data array) - Default = None. This is the dataset from 24 hours ago to make the comparison. 
        If the user downloads the data outside of the function and passes it in, then ds must be changed from ds=None to ds=ds. 

    32) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
        Set time=time when downloading the data outside of the function. 
         
    33) time_24 (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. This
        is the time for the RTMA from 24-hours ago. Set time_24=time_24 when downloading the data outside of the function. 

    34) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
        or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
        changed to None. 

    35) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

    36) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    37) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    38) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    39) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    40) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    41) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

    42) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
        For a view of the entire state - set cwa=None. 

        NWS CWA Abbreviations:

        1) AER - NWS Anchorage East Domain
        
        2) ALU - NWS Anchorage West Domain
        
        3) AJK - NWS Juneau
        
        4) AFG - NWS Fairbanks        

    43) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    44) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    45) show_low_high_thresholds (Boolean) - Default = False. When set to True, the low and high threshold contours are shown. 
        When set to False, those threshold contours are hidden. 

    Return: Saves individual images to f:Weather Data/RTMA/24 HOUR RTMA DEW POINT COMPARISON {With or Without Contours}/{reference_system}. 
    If the user selects a cwa the path will look like this: f:Weather Data/RTMA/24 HOUR RTMA DEW POINT COMPARISON {With or Without Contours}/{reference_system}/{cwa}
    
    '''
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if show_low_high_thresholds == True:
        text = 'With Contour Thresholds'
    else:
        text = 'Without Contour Thresholds'


    state = state

    if gacc_region != None:
        state = gacc_region
    else:
        state = state

    levels = np.arange(-30, 31, 1)
    ticks = levels[::5]

    cmap = colormaps.dew_point_change_colormap()

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

    path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f'24 HOUR RTMA DEW POINT COMPARISON {text}', reference_system, cwa)

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
        ds, ds_24, time, time_24 = RTMA.get_rtma_datasets(state, utc_time)
    else:
        ds = ds
        ds_24 = ds_24
        time = time
        time_24 = time_24

    dwpt = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['dpt2m'])
    lat = ds['lat']
    lon = ds['lon']

    dwpt_24 = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds_24['dpt2m'])
    lat_24 = ds_24['lat']

    diff = dwpt[0, :, :] - dwpt_24[0, :, :]

    time = time.replace(tzinfo=from_zone)
    time = time.astimezone(to_zone)
    time_utc = time.astimezone(from_zone)

    time_24 = time_24.replace(tzinfo=from_zone)
    time_24 = time_24.astimezone(to_zone)
    time_24_utc = time_24.astimezone(from_zone)

    decimate = scaling.get_nomads_decimation(western_bound, eastern_bound, southern_bound, northern_bound, True)

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])
        
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

    plt.title("24-Hour RTMA Dew Point Comparison (Δ°F)", fontsize=8, fontweight='bold', loc='left')
    
    plt.title("End: " + time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_utc.strftime('%H:00 UTC')+")\nStart: "+ time_24.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_24_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')

    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
    ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

    cs = ax.contourf(lon, lat, diff, 
                     transform=ccrs.PlateCarree(), levels=levels, cmap=cmap, alpha=0.5, zorder=1, extend='both')

    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

    if show_low_high_thresholds == True:
        c_low = ax.contour(lon, lat, mpcalc.smooth_gaussian(diff * units('degF'), n=12), levels=[-30, -15], colors='darkblue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_low, levels=[-30, -15], inline=True, fontsize=8, rightside_up=True)  
    
        c_high = ax.contour(lon, lat, mpcalc.smooth_gaussian(diff * units('degF'), n=12), levels=[15, 30], colors='darkred', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
        ax.clabel(c_high, levels=[15, 30], inline=True, fontsize=8, rightside_up=True) 
    else:
        pass

    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=7, clip_on=True)

    diff = diff[::decimate, ::decimate].to_numpy().flatten()

    stn.plot_parameter('C', diff, color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=7)

    fig.savefig(f"{path}/24-Hour RTMA DEW POINT Comparison.png", bbox_inches='tight')
    print(f"Saved 24-Hour RTMA DEW POINT Comparison graphic to {path_print}")

def plot_24_hour_wind_comparison(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.5, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=False, ds=None, ds_24=None, time=None, time_24=None, decimate='default', state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, cwa=None, signature_fontsize=6, stamp_fontsize=5, sample_points='barbs'):

    r'''
    This function plots the latest available 24-Hour RTMA Wind Comparison. 

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


    26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
        sample points are displayed on the graphic. Default setting is True. If the user wants 
        to hide the sample point values and only have the contour shading, this value will need 
        to be changed to False. 

    27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
        Default setting is a 10 point fontsize. 

    28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
        A value of 0 is completely transparent while a value of 1 is completely opaque. 
        Default setting is 0.5. 

    29) data (Boolean) - Default = False. If set to True, the user must download the data outside of the function and pass it in. 
        If set to False, the data is downloaded inside of the function. 

    30) ds (xarray.data array) - Default = None. If the user downloads the data outside of the function and passes it in, then ds must
        be changed from ds=None to ds=ds. 

    31) ds_24 (xarray.data array) - Default = None. This is the dataset from 24 hours ago to make the comparison. 
        If the user downloads the data outside of the function and passes it in, then ds must be changed from ds=None to ds=ds. 

    32) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
        Set time=time when downloading the data outside of the function. 
         
    33) time_24 (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. This
        is the time for the RTMA from 24-hours ago. Set time_24=time_24 when downloading the data outside of the function. 

    34) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
        or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
        changed to None. 

    35) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

    36) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    37) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    38) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    39) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    40) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    41) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

    42) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
        For a view of the entire state - set cwa=None. 

        NWS CWA Abbreviations:

        1) AER - NWS Anchorage East Domain
        
        2) ALU - NWS Anchorage West Domain
        
        3) AJK - NWS Juneau
        
        4) AFG - NWS Fairbanks        

    43) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    44) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    45) sample_points (String) - Default = 'barbs'. The type of sample point. When set to 'barbs' wind barbs will be displayed. 
        To display the numbers, change the setting to 'values'. 

    Return: Saves individual images to f:Weather Data/RTMA/24 HOUR RTMA WIND COMPARISON {With or Without Contours}/{reference_system}. 
    If the user selects a cwa the path will look like this: f:Weather Data/RTMA/24 HOUR RTMA WIND COMPARISON {With or Without Contours}/{reference_system}/{cwa}
    
    '''
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if sample_points == 'barbs':
        text = 'Barbs'
    else:
        text = 'Values'

    state = state

    if gacc_region != None:
        state = gacc_region
    else:
        state = state

    levels = np.arange(-30, 31, 1)
    ticks = levels[::5]

    cmap = colormaps.wind_speed_change_colormap()

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

    path, path_print = file_functions.rtma_graphics_paths(state, gacc_region, f'24 HOUR RTMA WIND COMPARISON {text}', reference_system, cwa)

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
        ds, ds_24, time, time_24 = RTMA.get_rtma_datasets(state, utc_time)
    else:
        ds = ds
        ds_24 = ds_24
        time = time
        time_24 = time_24

    ws = ds['wind10m'] * 2.23694
    u = ds['ugrd10m'] * 2.23694
    v = ds['vgrd10m'] * 2.23694
    lat = ds['lat']
    lon = ds['lon']

    lat_24 = ds_24['lat']
    lon_24 = ds_24['lon']
    ws_24 = ds_24['wind10m'] * 2.23694
    u_24= ds_24['ugrd10m'] * 2.23694
    v_24 = ds_24['vgrd10m'] * 2.23694

    diff = ws[0, :, :] - ws_24[0, :, :]

    time = time.replace(tzinfo=from_zone)
    time = time.astimezone(to_zone)
    time_utc = time.astimezone(from_zone)

    time_24 = time_24.replace(tzinfo=from_zone)
    time_24 = time_24.astimezone(to_zone)
    time_24_utc = time_24.astimezone(from_zone)

    decimate = scaling.get_nomads_decimation(western_bound, eastern_bound, southern_bound, northern_bound, True)

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])
    plot_lon_24, plot_lat_24 = np.meshgrid(lon_24[::decimate], lat_24[::decimate])
        
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

    plt.title("24-Hour RTMA Wind Comparison (ΔMPH)", fontsize=8, fontweight='bold', loc='left')
    
    plt.title("End: " + time.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_utc.strftime('%H:00 UTC')+")\nStart: "+ time_24.strftime(f'%m/%d/%Y %H:00 {timezone}') + " (" + time_24_utc.strftime('%H:00 UTC')+")", fontsize=7, fontweight='bold', loc='right')

    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
    ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

    cs = ax.contourf(lon, lat, diff, 
                     transform=ccrs.PlateCarree(), levels=levels, cmap=cmap, alpha=0.5, zorder=1, extend='both')

    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=8, zorder=7, clip_on=True)

    stn1 = mpplots.StationPlot(ax, plot_lon_24.flatten(), plot_lat_24.flatten(),
                                 transform=ccrs.PlateCarree(), zorder=7, fontsize=8, clip_on=True)

    if sample_points == 'values':
        diff = diff[::decimate, ::decimate].to_numpy().flatten()
        stn.plot_parameter('C', diff, color='black', path_effects=[withStroke(linewidth=1, foreground='white')], zorder=7)

    if sample_points == 'barbs':
        stn.plot_barb(u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='crimson', length=4.5, alpha=1, zorder=7, linewidth=0.8, label=time.strftime(f'%m/%d %H:00 {timezone}'))     
        stn1.plot_barb(u_24[0, :, :][::decimate, ::decimate], v_24[0, :, :][::decimate, ::decimate], color='lime', length=4.5, alpha=1, zorder=7, linewidth=0.8, label=time_24.strftime(f'%m/%d %H:00 {timezone}')) 
        leg = ax.legend(loc=(0.01, 0.06), framealpha=1, fontsize='x-small')
        leg.set_zorder(12)

    fig.savefig(f"{path}/24-Hour RTMA WIND Comparison.png", bbox_inches='tight')
    print(f"Saved 24-Hour RTMA WIND Comparison graphic to {path_print}")


