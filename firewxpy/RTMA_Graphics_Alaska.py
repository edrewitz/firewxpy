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
import matplotlib.gridspec as gridspec
import firewxpy.settings as settings
import firewxpy.standard as standard
import firewxpy.dims as dims
import warnings



from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from dateutil import tz
from firewxpy.calc import scaling, Thermodynamics, unit_conversion
from firewxpy.utilities import file_functions
from metpy.units import units
from firewxpy.data_access import RTMA_Alaska

mpl.rcParams['font.weight'] = 'bold'

mpl.rcParams['font.weight'] = 'bold'

warnings.filterwarnings('ignore')

def plot_relative_humidity(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Relative Humidity. 
    
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

                            42) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            44) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            45) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            46) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    reference_system = reference_system

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    contourf = np.arange(0, 101, 1)

    labels = contourf[::4]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False)
            

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8



    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None and cwa == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    
    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.relative_humidity_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            
            rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            
            rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            print("Unpacked the data successfully!")
            
        except Exception as e:

            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")
            
            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
                dwpt = ds['dpt2m']
                lat = ds['lat']
                lon = ds['lon']
                temp = temp - 273.15
                dwpt = dwpt - 273.15
                
                rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                            
                print("Unpacked the data successfully!")

            except Exception as e:
                pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    print("Preparing Graphic - Please Wait...")

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    plt.title("RTMA Relative Humidity (%)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, rtma_data[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, zorder=2)

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Relative Humidity (%)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        rtma_data = rtma_data[0, ::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', rtma_data, color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA RH', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA RH')


def plot_low_and_high_relative_humidity(low_rh_threshold=25, high_rh_threshold=80, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9, x1=None, x2=None, y=None, x_size=None, colorbar_fontsize=None, labels_low_increment=None, labels_high_increment=None):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Relative Humidity filtered for areas of low RH and high RH. 
    
        Required Arguments: None

        Optional Arguments: 1) low_rh_threshold (Integer) - Default = 15%. The top bound of what is considered low relative humidity. 

                            2) high_rh_threshold (Integer) - Default = 80%. The bottom bound of what is considered high relative humidity.         
        
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

                            7) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            8) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            9) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            10) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            11) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            12) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            13) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            14) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            15) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            16) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            17) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                                                   
    
                            18) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            19) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            20) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            21) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            22) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            23) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            24) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            25) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            26) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            27) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            28) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            29) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            30) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            31) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            32) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            35) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            36) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            37) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            38) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            39) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            40) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            41) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            42) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            43) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            44) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            45) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            46) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            47) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            48) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            49) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            50) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            51) x1 (Float) - The x-position of the low relative humidity colorbar. Defaults are in the settings module. Only edit this if making a custom plot. 

                            52) x2 (Float) - The x-position of the high relative humidity colorbar. Defaults are in the settings module. Only edit this if making a custom plot. 

                            53) y (Float) - The y-position of both colorbars. Defaults are in the settings module. Only edit this if making a custom plot. 

                            54) x_size (Float) - The horizontal size of the colorbars. Defaults are in the settings module. Only edit this if making a custom plot. 

                            55) labels_low_increment (Integer) - Default = None. The increment of the low relative humidity colorbar. 

                            56) labels_high_increment (Integer) - Default = None. The increment of the high relative humidity colorbar. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    reference_system = reference_system

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    low_rh_thresh = low_rh_threshold + 1


    contourf_low = np.arange(0, low_rh_thresh, 1)
    contourf_high = np.arange(high_rh_threshold, 101, 1)
    
    if low_rh_threshold <= 15:
        labels_low = contourf_low
    elif low_rh_threshold > 15 and low_rh_threshold < 40:
        if (low_rh_threshold % 2) == 0:
            labels_low = contourf_low[::2]
        else:
            labels_low = contourf_low[::5]
    else:
        labels_low = contourf_low[::5]

    if high_rh_threshold >= 80:
        labels_high = contourf_high
    elif high_rh_threshold >= 60 and high_rh_threshold < 80:
        if (high_rh_threshold % 2) == 0:
            labels_high = contourf_high[::4]
        else:
            labels_high = contourf_high[::5]
    else:
        labels_high = contourf_high[::5]


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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False, 'Low and High RH')

        mpl.rcParams['xtick.labelsize'] = 7
        mpl.rcParams['ytick.labelsize'] = 7

        if cwa == None:
            x1, x2, y, x_size, colorbar_fontsize = 0.13, 0.52, 0.28, 0.36, 12
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            x1, x2, y, x_size, colorbar_fontsize = 0.13, 0.52, 0.22, 0.36, 12
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            x1, x2, y, x_size, colorbar_fontsize = 0.13, 0.52, 0.25, 0.36, 12
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            x1, x2, y, x_size, colorbar_fontsize = 0.13, 0.52, 0.29, 0.36, 12
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            x1, x2, y, x_size, colorbar_fontsize = 0.13, 0.52, 0.29, 0.36, 12
            title_fontsize, subplot_title_fontsize = 9, 8

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect
        x1 = x1 
        x2 = x2
        y = y
        x_size = x_size
        colorbar_fontsize = colorbar_fontsize
        labels_low = contourf_low[::labels_low_increment]
        labels_high = contourf_high[::labels_high_increment]
    
    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap_low = colormaps.low_relative_humidity_colormap()
    cmap_high = colormaps.excellent_recovery_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            
            rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            
            rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            print("Unpacked the data successfully!")
            
        except Exception as e:

            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")
            
            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
                dwpt = ds['dpt2m']
                lat = ds['lat']
                lon = ds['lon']
                temp = temp - 273.15
                dwpt = dwpt - 273.15
                
                rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                            
                print("Unpacked the data successfully!")

            except Exception as e:
                pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    print("Creating Image - Please Wait...")

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    plt.title("RTMA Low and High Relative Humidity\n[RH <= "+str(low_rh_threshold)+" (%) & RH >= "+str(high_rh_threshold)+" (%)]", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    if x_size <= 0.25:
        labels_low = contourf_low[::5]
        labels_high = contourf_high[::5]
    else:
        labels_low = labels_low
        labels_high = labels_high

    x_cbar_0, y_cbar_0, x_cbar_size, y_cbar_size = x1, y, x_size, 0.02
    x_cbar2_0, y_cbar2_0, x_cbar2_size, y_cbar2_size = x2, y, x_size, 0.02
    
    cs_low = ax.contourf(lon, lat, rtma_data[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=contourf_low, cmap=cmap_low, alpha=alpha, zorder=2)

    cs_high = ax.contourf(lon, lat, rtma_data[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=contourf_high, cmap=cmap_high, alpha=alpha, zorder=2)

    ax_cbar = plt.gcf().add_axes([x_cbar_0, y_cbar_0, x_cbar_size, y_cbar_size])
    ax_cbar_2 = plt.gcf().add_axes([x_cbar2_0, y_cbar2_0, x_cbar2_size, y_cbar2_size])
    cbar_low = plt.gcf().colorbar(cs_low, cax=ax_cbar, orientation='horizontal',
     label='Low Relative Humidity (%)', pad=0.01, ticks=labels_low)
    cbar_high = plt.gcf().colorbar(cs_high, cax=ax_cbar_2, orientation='horizontal',
     label='High Relative Humidity (%)', pad=0.01, ticks=labels_high)

    cbar_low.set_label(label="Low Relative Humidity (%)", size=colorbar_fontsize, fontweight='bold')

    cbar_high.set_label(label="High Relative Humidity (%)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        rtma_data = rtma_data[0, ::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', rtma_data, color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA LOW AND HIGH RH', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA LOW AND HIGH RH')

def plot_24_hour_relative_humidity_comparison(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, data_24=None, time=None, time_24=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Relative Humidity. 
    
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

                            42) data (Array) - Default = None. A data array (for latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) data_24 (Array) - Default = None. A data array (for 24hrs prior to the latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data_24=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data_24=None to data_24=data for example.  

                            44) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            45) time_24 (Array) - Default = None. A time array (for the dataset that is 24-hours prior to current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            46) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            47) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            48) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            49) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            50) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    data_24 = data_24
    time_24 = time_24
    state = 'ak'
    cwa = cwa

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    contourf = np.arange(-50, 51, 1)

    linewidths = 1

    labels = contourf[::4]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False, '24 Hour RH Comparison')

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    
    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.relative_humidity_change_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
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
            
            rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            rtma_data_24 = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_24, dwpt_24)

            diff = rtma_data[0, :, :] - rtma_data_24[0, :, :]
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time
            ds_24 = data_24
            rtma_time_24 = time_24
    
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
            
            rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            rtma_data_24 = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_24, dwpt_24)
    
            diff = rtma_data[0, :, :] - rtma_data_24[0, :, :]

            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")
            try:
                ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
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
                
                rtma_data = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                rtma_data_24 = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp_24, dwpt_24)
    
                diff = rtma_data[0, :, :] - rtma_data_24[0, :, :]
                            
                print("Unpacked the data successfully!")

            except Exception as e:
                pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc_24 = rtma_time_24.astimezone(from_zone)  

    print("Creating Image - Please Wait...")

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
    if show_rivers == True:
        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
    
    plt.title("RTMA 24-Hour Relative Humidity Comparison (Δ%)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Current: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")\n[Current - 24HRS]: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_24.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, diff[:, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both', zorder=2)

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        diff = diff[::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', diff, color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Relative Humidity Trend (Δ%)", size=colorbar_fontsize, fontweight='bold')

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, '24HR RTMA RH COMPARISON', reference_system)
    file_functions.update_images(fig, path, gif_path, '24HR RTMA RH COMPARISON')


def plot_temperature(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Temperature. 
    
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

                            42) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            44) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            45) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            46) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    local_time, utc_time = standard.plot_creation_time()

    month = utc_time.month

    if month >= 5 and month <= 9:
        contourf = np.arange(0, 91, 1)
    if month == 4 or month == 10:
        contourf = np.arange(-20, 61, 1)
    if month >= 11 or month <= 3:
        contourf = np.arange(-40, 51, 1)

    labels = contourf[::5]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False)


        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.temperature_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            temp = ds['tmp2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
            
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
                lat = ds['lat']
                lon = ds['lon']
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                            
                print("Unpacked the data successfully!")   

            except Exception as e:
                pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    plt.title("RTMA Temperature (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, temp[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both', zorder=2)

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        temp = temp[0, ::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA TEMPERATURE', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA TEMPERATURE')


def plot_temperature_advection(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Temperature Advection. 
    
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

                            42) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            44) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            45) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            46) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    local_time, utc_time = standard.plot_creation_time()

    month = utc_time.month

    contourf = np.arange(-20, 21, 1)

    labels = contourf[::2]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8


    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.temperature_change_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            u = ds['ugrd10m']
            v = ds['vgrd10m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            temp = ds['tmp2m']
            lat = ds['lat']
            u = ds['ugrd10m']
            v = ds['vgrd10m']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
            
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
                u = ds['ugrd10m']
                v = ds['vgrd10m']
                lat = ds['lat']
                lon = ds['lon']
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                            
                print("Unpacked the data successfully!")

            except Exception as e:
                pass
                
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    plt.title("RTMA Temperature Advection [\N{DEGREE SIGN}F/Hour]", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    dx = units('meters') * 2500
    dy = units('meters') * 2500
    temp = units('degF') * temp
    u = units('m/s') * u
    v = units('m/s') * v

    advection = mpcalc.advection(temp[0, :, :], u[0, :, :], v[0, :, :], dx=dx, dy=dy)

    advection = advection * 3600

    cs = ax.contourf(lon, lat, advection[:, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both', zorder=2)

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Temperature Advection (\N{DEGREE SIGN}F/Hour)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize


    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)

    stn.plot_barb(u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='darkgreen', label=rtma_time.strftime('%m/%d %H:00'), alpha=1, zorder=9, linewidth=2)


    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA TEMPERATURE ADVECTION', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA TEMPERATURE ADVECTION')


def plot_dew_point_advection(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Dew Point Advection. 
    
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

                            42) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            44) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            45) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            46) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder. 
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    local_time, utc_time = standard.plot_creation_time()

    month = utc_time.month

    contourf = np.arange(-20, 21, 1)

    labels = contourf[::2]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False)


        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.dew_point_change_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            temp = ds['dpt2m']
            u = ds['ugrd10m']
            v = ds['vgrd10m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            temp = ds['dpt2m']
            lat = ds['lat']
            u = ds['ugrd10m']
            v = ds['vgrd10m']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
            
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                temp = ds['dpt2m']
                u = ds['ugrd10m']
                v = ds['vgrd10m']
                lat = ds['lat']
                lon = ds['lon']
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass
                 
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    plt.title("RTMA Dew Point Advection [\N{DEGREE SIGN}F/Hour]", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    dx = units('meters') * 2500
    dy = units('meters') * 2500
    temp = units('degF') * temp
    u = units('m/s') * u
    v = units('m/s') * v

    advection = mpcalc.advection(temp[0, :, :], u[0, :, :], v[0, :, :], dx=dx, dy=dy)

    advection = advection * 3600

    cs = ax.contourf(lon, lat, advection[:, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both', zorder=2)

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Dew Point Advection (\N{DEGREE SIGN}F/Hour)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize


    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)

    stn.plot_barb(u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='darkred', label=rtma_time.strftime('%m/%d %H:00'), alpha=1, zorder=9, linewidth=2)

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA DEW POINT ADVECTION', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA DEW POINT ADVECTION')


def plot_relative_humidity_advection(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Relative Humidity Advection. 
    
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

                            42) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            44) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            45) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            46) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    local_time, utc_time = standard.plot_creation_time()

    month = utc_time.month

    contourf = np.arange(-30, 31, 1)

    labels = contourf[::2]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8


    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.relative_humidity_change_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            u = ds['ugrd10m']
            v = ds['vgrd10m']
            lat = ds['lat']
            lon = ds['lon']
      
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            u = ds['ugrd10m']
            v = ds['vgrd10m']
            lat = ds['lat']
            lon = ds['lon']
            
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
                dwpt = ds['dpt2m']
                temp = temp - 273.15
                dwpt = dwpt - 273.15
                rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                u = ds['ugrd10m']
                v = ds['vgrd10m']
                lat = ds['lat']
                lon = ds['lon']
    
                print("Unpacked the data successfully!")

            except Exception as e:
                pass

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    plt.title("RTMA Relative Humidity Advection [%/Hour]", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    dx = units('meters') * 2500
    dy = units('meters') * 2500
    rh = units('percent') * rh
    u = units('m/s') * u
    v = units('m/s') * v

    advection = mpcalc.advection(rh[0, :, :], u[0, :, :], v[0, :, :], dx=dx, dy=dy)

    advection = advection * 3600

    cs = ax.contourf(lon, lat, advection[:, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both', zorder=2)

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Relative Humidity Advection (%/Hour)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                 transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)

    stn.plot_barb(u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='blue', label=rtma_time.strftime('%m/%d %H:00'), alpha=1, zorder=9, linewidth=2)
    
    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA RH ADVECTION', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA RH ADVECTION')

def plot_frost_freeze(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Frost/Freeze Areas (RTMA Temperature <= 32F). 
    
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

                            42) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            44) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            45) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            46) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    local_time, utc_time = standard.plot_creation_time()

    month = utc_time.month

    contourf = np.arange(-10, 33, 1)

    labels = contourf[::2]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8


    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.cool_temperatures_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            temp = ds['tmp2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
            
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
                lat = ds['lat']
                lon = ds['lon']
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass

    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    plt.title("RTMA Frost Freeze Areas\n[Temperature <= 32 (\N{DEGREE SIGN}F)]", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, temp[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='min', zorder=2)

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        temp = temp[0, ::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA FROST FREEZE', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA FROST FREEZE')

def plot_extreme_heat(temperature_threshold=70, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Extreme Heat. 
    
        Required Arguments: None

        Optional Arguments: 1) temperature_threshold (Integer) - Default = 100F. The threshold at which the user defines extreme heat. 
                               Extreme Heat = RTMA Temperature >= temperature_threshold.
        
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

                            43) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            44) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            45) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            46) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            47) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            48) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            49) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder. 
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    local_time, utc_time = standard.plot_creation_time()

    month = utc_time.month

    contourf = np.arange(temperature_threshold, (temperature_threshold + 21), 1)

    labels = contourf[::1]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8
    
    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.cool_temperatures_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            temp = ds['tmp2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
            
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
                lat = ds['lat']
                lon = ds['lon']
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass    
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    plt.title("RTMA Extreme Heat Areas\n[Temperature >= "+str(temperature_threshold)+" (\N{DEGREE SIGN}F)]", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, temp[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap='hot', alpha=alpha, extend='max', zorder=2)

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        temp = temp[0, ::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA EXTREME HEAT', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA EXTREME HEAT')

def plot_24_hour_temperature_comparison(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, data_24=None, time=None, time_24=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Temperature. 
    
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

                            42) data (Array) - Default = None. A data array (for latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) data_24 (Array) - Default = None. A data array (for 24hrs prior to the latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data_24=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data_24=None to data_24=data for example.  

                            44) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            45) time_24 (Array) - Default = None. A time array (for the dataset that is 24-hours prior to current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            46) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            47) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            48) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            49) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            50) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    data_24 = data_24
    time_24 = time_24
    state = 'ak'
    cwa = cwa

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    contourf = np.arange(-25, 26, 1)

    linewidths = 1

    labels = contourf[::2]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False, '24 Hour Temperature Comparison')

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    
    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.temperature_change_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
            temp = ds['tmp2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)

            temp_24 = ds_24['tmp2m']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']
            temp_24 = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_24)

            diff = temp[0, :, :] - temp_24[0, :, :]
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time
            ds_24 = data_24
            rtma_time_24 = time_24

            temp = ds['tmp2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = temp - 273.15

            temp_24 = ds_24['tmp2m']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']
            temp_24 = temp_24 - 273.15

            diff = temp[0, :, :] - temp_24[0, :, :]

            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
                temp = ds['tmp2m']
                lat = ds['lat']
                lon = ds['lon']
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
    
                temp_24 = ds_24['tmp2m']
                lat_24 = ds_24['lat']
                lon_24 = ds_24['lon']
                temp_24 = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_24)
    
                diff = temp[0, :, :] - temp_24[0, :, :]
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass    
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc_24 = rtma_time_24.astimezone(from_zone)   

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
    if show_rivers == True:
        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
    
    plt.title("RTMA 24-Hour Temperature Comparison (Δ\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Current: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")\n[Current - 24HRS]: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_24.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, diff[:, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both', zorder=2)

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        diff = diff[::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', diff, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Temperature Trend (Δ\N{DEGREE SIGN}F)", size=colorbar_fontsize, fontweight='bold')

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, '24HR RTMA TEMPERATURE COMPARISON', reference_system)
    file_functions.update_images(fig, path, gif_path, '24HR RTMA TEMPERATURE COMPARISON')

def plot_dew_point(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Dew Point. 
    
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

                            42) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            44) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            45) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            46) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    local_time, utc_time = standard.plot_creation_time()

    month = utc_time.month

    if month >= 5 and month <= 9:
        contourf = np.arange(-10, 71, 1)
    if month == 4 or month == 10:
        contourf = np.arange(-30, 51, 1)
    if month >= 11 or month <= 3:
        contourf = np.arange(-50, 41, 1)

    labels = contourf[::5]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8
    

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.dew_point_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            temp = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            temp = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
            
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                temp = ds['dpt2m']
                lat = ds['lat']
                lon = ds['lon']
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    plt.title("RTMA Dew Point (\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, temp[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both', zorder=2)

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Dew Point (\N{DEGREE SIGN}F)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        temp = temp[0, ::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', temp, color='darkred', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA DEW POINT', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA DEW POINT')

def plot_24_hour_dew_point_comparison(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, data_24=None, time=None, time_24=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Dew Point. 
    
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

                            42) data (Array) - Default = None. A data array (for latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) data_24 (Array) - Default = None. A data array (for 24hrs prior to the latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data_24=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data_24=None to data_24=data for example.  

                            44) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            45) time_24 (Array) - Default = None. A time array (for the dataset that is 24-hours prior to current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            46) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            47) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            48) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            49) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            50) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    data_24 = data_24
    time_24 = time_24
    state = 'ak'
    cwa = cwa

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    contourf = np.arange(-25, 26, 1)

    linewidths = 1

    labels = contourf[::2]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False, '24 Hour Dewpoint Comparison')

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8


    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    
    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.dew_point_change_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
            temp = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)

            temp_24 = ds_24['dpt2m']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']
            temp_24 = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_24)

            diff = temp[0, :, :] - temp_24[0, :, :]
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time
            ds_24 = data_24
            rtma_time_24 = time_24

            temp = ds['dpt2m']
            lat = ds['lat']
            lon = ds['lon']
            temp = temp - 273.15

            temp_24 = ds_24['dpt2m']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']
            temp_24 = temp_24 - 273.15

            diff = temp[0, :, :] - temp_24[0, :, :]

            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
                temp = ds['dpt2m']
                lat = ds['lat']
                lon = ds['lon']
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp)
    
                temp_24 = ds_24['dpt2m']
                lat_24 = ds_24['lat']
                lon_24 = ds_24['lon']
                temp_24 = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(temp_24)
    
                diff = temp[0, :, :] - temp_24[0, :, :]
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc_24 = rtma_time_24.astimezone(from_zone)   

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
    if show_rivers == True:
        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
    
    plt.title("RTMA 24-Hour Dew Point Comparison (Δ\N{DEGREE SIGN}F)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Current: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")\n[Current - 24HRS]: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_24.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, diff[:, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both', zorder=2)

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        diff = diff[::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', diff, color='darkred', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Dew Point Trend (Δ\N{DEGREE SIGN}F)", size=colorbar_fontsize, fontweight='bold')

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, '24HR RTMA DEW POINT COMPARISON', reference_system)
    file_functions.update_images(fig, path, gif_path, '24HR RTMA DEW POINT COMPARISON')

def plot_total_cloud_cover(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Total Cloud Cover. 
    
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

                            42) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            44) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            45) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            46) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    local_time, utc_time = standard.plot_creation_time()

    month = utc_time.month

    contourf = np.arange(0, 101, 1)

    labels = contourf[::4]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.cloud_cover_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            lat = ds['lat']
            lon = ds['lon']
            tcdcclm = ds['tcdcclm']
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            tcdcclm = ds['tcdcclm']
            lat = ds['lat']
            lon = ds['lon']
            
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                lat = ds['lat']
                lon = ds['lon']
                tcdcclm = ds['tcdcclm']
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    plt.title("RTMA Total Cloud Cover (% Of Sky)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, tcdcclm[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, zorder=2)

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Total Cloud Cover (% Of Sky)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        tcdcclm = tcdcclm[0, ::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', tcdcclm, color='red', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA TOTAL CLOUD COVER', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA TOTAL CLOUD COVER')

def plot_24_hour_total_cloud_cover_comparison(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, data_24=None, time=None, time_24=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Total Cloud Cover. 
    
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

                            42) data (Array) - Default = None. A data array (for latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) data_24 (Array) - Default = None. A data array (for 24hrs prior to the latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data_24=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data_24=None to data_24=data for example.  

                            44) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            45) time_24 (Array) - Default = None. A time array (for the dataset that is 24-hours prior to current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            46) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            47) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            48) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            49) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            50) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder. 
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    data_24 = data_24
    time_24 = time_24
    state = 'ak'
    cwa = cwa

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    contourf = np.arange(-60, 61, 1)

    linewidths = 1

    labels = contourf[::5]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False, '24 Hour Total Cloud Cover Comparison')

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    
    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.cloud_cover_change_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
            tcdcclm= ds['tcdcclm']
            lat = ds['lat']
            lon = ds['lon']

            tcdcclm_24 = ds_24['tcdcclm']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']

            diff = tcdcclm[0, :, :] - tcdcclm_24[0, :, :]
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time
            ds_24 = data_24
            rtma_time_24 = time_24

            tcdcclm= ds['tcdcclm']
            lat = ds['lat']
            lon = ds['lon']

            tcdcclm_24 = ds_24['tcdcclm']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']

            diff = tcdcclm[0, :, :] - tcdcclm_24[0, :, :]

            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
                tcdcclm= ds['tcdcclm']
                lat = ds['lat']
                lon = ds['lon']
    
                tcdcclm_24 = ds_24['tcdcclm']
                lat_24 = ds_24['lat']
                lon_24 = ds_24['lon']
    
                diff = tcdcclm[0, :, :] - tcdcclm_24[0, :, :]
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc_24 = rtma_time_24.astimezone(from_zone)   

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
    if show_rivers == True:
        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
    
    plt.title("RTMA 24-Hour Total Cloud Cover Comparison (Δ% Of Sky)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Current: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")\n[Current - 24HRS]: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_24.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, diff[:, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both', zorder=2)

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        diff = diff[::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', diff, color='red', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Total Cloud Cover Trend (Δ% Of Sky)", size=colorbar_fontsize, fontweight='bold')

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, '24HR RTMA TOTAL CLOUD COVER COMPARISON', reference_system)
    file_functions.update_images(fig, path, gif_path, '24HR RTMA TOTAL CLOUD COVER COMPARISON')


def plot_wind_speed(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Wind Speed. 
    
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

                            42) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            44) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            45) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            46) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder. 
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    local_time, utc_time = standard.plot_creation_time()

    month = utc_time.month

    contourf = np.arange(0, 61, 1)

    labels = contourf[::4]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.wind_speed_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            lat = ds['lat']
            lon = ds['lon']
            ws = ds['wind10m']
            ws = unit_conversion.meters_per_second_to_mph(ws)
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            ws = ds['wind10m']
            lat = ds['lat']
            lon = ds['lon']
            ws = unit_conversion.meters_per_second_to_mph(ws)
            
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                lat = ds['lat']
                lon = ds['lon']
                ws = ds['wind10m']
                ws = unit_conversion.meters_per_second_to_mph(ws)
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    plt.title("RTMA Wind Speed (MPH)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, ws[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='max', zorder=2)

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Wind Speed (MPH)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        ws = ws[0, ::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', ws, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA WIND SPEED', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA WIND SPEED')

def plot_24_hour_wind_speed_comparison(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, data_24=None, time=None, time_24=None, cwa=None, colorbar_pad=0.02, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Wind Speed. 
    
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

                            42) data (Array) - Default = None. A data array (for latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) data_24 (Array) - Default = None. A data array (for 24hrs prior to the latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data_24=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data_24=None to data_24=data for example.  

                            44) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            45) time_24 (Array) - Default = None. A time array (for the dataset that is 24-hours prior to current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            46) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            47) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            48) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            49) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            50) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    data_24 = data_24
    time_24 = time_24
    state = 'ak'
    cwa = cwa

    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    contourf = np.arange(-20, 21, 1)

    linewidths = 1

    labels = contourf[::2]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False, '24 Hour Wind Speed Comparison')

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    
    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.wind_speed_change_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
            ws = ds['wind10m']
            lat = ds['lat']
            lon = ds['lon']
            ws = unit_conversion.meters_per_second_to_mph(ws)

            ws_24 = ds_24['wind10m']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']
            ws_24 = unit_conversion.meters_per_second_to_mph(ws_24)

            diff = ws[0, :, :] - ws_24[0, :, :]
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time
            ds_24 = data_24
            rtma_time_24 = time_24

            ws = ds['wind10m']
            lat = ds['lat']
            lon = ds['lon']
            ws = unit_conversion.meters_per_second_to_mph(ws)

            ws_24 = ds_24['wind10m']
            lat_24 = ds_24['lat']
            lon_24 = ds_24['lon']
            ws_24 = unit_conversion.meters_per_second_to_mph(ws_24)

            diff = ws[0, :, :] - ws_24[0, :, :]

            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
                ws = ds['wind10m']
                lat = ds['lat']
                lon = ds['lon']
                ws = unit_conversion.meters_per_second_to_mph(ws)
    
                ws_24 = ds_24['wind10m']
                lat_24 = ds_24['lat']
                lon_24 = ds_24['lon']
                ws_24 = unit_conversion.meters_per_second_to_mph(ws_24)
    
                diff = ws[0, :, :] - ws_24[0, :, :]
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc_24 = rtma_time_24.astimezone(from_zone)   

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
    if show_rivers == True:
        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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
    
    plt.title("RTMA Wind Speed Comparison (ΔMPH)", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Current: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")\n[Current - 24HRS]: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_24.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, diff[:, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both', zorder=2)

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    plot_lon, plot_lat = np.meshgrid(lon[::decimate], lat[::decimate])

    if show_sample_points == True:

        stn = mpplots.StationPlot(ax, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        diff = diff[::decimate, ::decimate].to_numpy().flatten()
    
        stn.plot_parameter('C', diff, color='darkred', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Wind Speed Difference (ΔMPH)", size=colorbar_fontsize, fontweight='bold')

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, '24HR RTMA WIND SPEED COMPARISON', reference_system)
    file_functions.update_images(fig, path, gif_path, '24HR RTMA WIND SPEED COMPARISON')


def plot_wind_speed_and_direction(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, barbs_or_quivers='barbs', barb_quiver_alpha=1, barb_quiver_fontsize=7, barb_linewidth=1, quiver_linewidth=0.5, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) for Wind Speed & Direction. 
    
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

                            42) data (Array) - Default = None. A data array (for latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            44) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            45) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            46) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            47) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            48) barbs_or_quivers (String) - Default = 'barbs'. Sets the plot to either be wind barbs or vectors. Proper syntax for wind barbs: 'barbs', 'b', 'Barbs',
                                'BARBS', 'B'. Proper syntax for quivers (vectors): 'quivers', 'q', 'Quivers', 'QUIVERS', 'Q'

                            49) barb_quiver_alpha (Float) - Default = 1. Number between 0 and 1 for the transparency of the barb or quiver. 0 is completely transparent while 1 is completely opaque. 

                            50) barb_quiver_fontsize (Integer) - Default = 6. Fontsize of the barb or quiver. 

                            51) barb_linewidth (Float) - Default = 0.5. The width or thickness of the wind barb. 

                            52) quiver_linewidth (Float) - Default = 0.5. The width or thickness of the quiver. 

                            53) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            54) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa

    if barbs_or_quivers == 'barbs' or barbs_or_quivers == 'Barbs' or barbs_or_quivers == 'BARBS' or barbs_or_quivers == 'B' or barbs_or_quivers == 'b':

        barbs = True

    if barbs_or_quivers == 'quivers' or barbs_or_quivers == 'Quivers' or barbs_or_quivers == 'QUIVERS' or barbs_or_quivers == 'Q' or barbs_or_quivers == 'q':

        barbs = False

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    local_time, utc_time = standard.plot_creation_time()

    month = utc_time.month

    contourf = np.arange(0, 61, 1)

    labels = contourf[::4]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.wind_speed_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            u = ds['ugrd10m']
            v = ds['vgrd10m']
            ws = ds['wind10m']
            lon = ds['lon']
            lat = ds['lat']
            ws = unit_conversion.meters_per_second_to_mph(ws)
            lon_2d, lat_2d = np.meshgrid(lon, lat)
            u = unit_conversion.meters_per_second_to_mph(u)
            v = unit_conversion.meters_per_second_to_mph(v)    
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time

            u = ds['ugrd10m']
            v = ds['vgrd10m']
            ws = ds['wind10m']
            lon = ds['lon']
            lat = ds['lat']
            ws = unit_conversion.meters_per_second_to_mph(ws)
            lon_2d, lat_2d = np.meshgrid(lon, lat)
            u = unit_conversion.meters_per_second_to_mph(u)
            v = unit_conversion.meters_per_second_to_mph(v)         
            
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                u = ds['ugrd10m']
                v = ds['vgrd10m']
                ws = ds['wind10m']
                lon = ds['lon']
                lat = ds['lat']
                ws = unit_conversion.meters_per_second_to_mph(ws)
                lon_2d, lat_2d = np.meshgrid(lon, lat)
                u = unit_conversion.meters_per_second_to_mph(u)
                v = unit_conversion.meters_per_second_to_mph(v)    
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass    
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.patch.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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
    
    if barbs == True:
    
        plt.title("RTMA Wind Speed & Direction\n[MPH (Shaded) + Wind Barbs]", fontsize=title_fontsize, fontweight='bold', loc='left')

    if barbs == False:

        plt.title("RTMA Wind Speed & Direction\n[MPH (Shaded) + Wind Vectors]", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, ws[0, :, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='max', zorder=2)

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Wind Speed (MPH)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    if barbs == True:

        stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                         transform=ccrs.PlateCarree(), zorder=9, fontsize=barb_quiver_fontsize, clip_on=True)

        stn.plot_barb(u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='lime', label=rtma_time.strftime('%m/%d %H:00'), alpha=barb_quiver_alpha, zorder=9, linewidth=barb_linewidth)

        file_name_end = ' WIND BARBS'

    if barbs == False:

        minshaft, headlength, headwidth = dims.get_quiver_dims(state, gacc_region)

        ax.quiver(lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate], u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='lime', minshaft=minshaft, headlength=headlength, headwidth=headwidth, alpha=barb_quiver_alpha, label=rtma_time.strftime('%m/%d %H:00'), zorder=9, linewidth=quiver_linewidth, transform=ccrs.PlateCarree())

        file_name_end = ' WIND VECTORS'

    fname = 'RTMA WIND SPEED & DIRECTION'+ file_name_end

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, fname, reference_system)
    file_functions.update_images(fig, path, gif_path, fname)

def plot_24_hour_wind_speed_and_direction_comparison(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', alpha=0.5, data=None, data_24=None, time=None, time_24=None, cwa=None, colorbar_pad=0.02, barbs_or_quivers='barbs', barb_quiver_alpha=1, barb_quiver_fontsize=6, barb_linewidth=0.5, quiver_linewidth=0.5, aspect=30, tick=9):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Wind Speed & Direction. 
    
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

                            42) data (Array) - Default = None. A data array (for latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            43) data_24 (Array) - Default = None. A data array (for 24hrs prior to the latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data_24=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data_24=None to data_24=data for example.  

                            44) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            45) time_24 (Array) - Default = None. A time array (for the dataset that is 24-hours prior to current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            46) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            47) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            48) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            49) barbs_or_quivers (String) - Default = 'barbs'. Sets the plot to either be wind barbs or vectors. Proper syntax for wind barbs: 'barbs', 'b', 'Barbs',
                                'BARBS', 'B'. Proper syntax for quivers (vectors): 'quivers', 'q', 'Quivers', 'QUIVERS', 'Q'

                            50) barb_quiver_alpha (Float) - Default = 1. Number between 0 and 1 for the transparency of the barb or quiver. 0 is completely transparent while 1 is completely opaque. 

                            51) barb_quiver_fontsize (Integer) - Default = 6. Fontsize of the barb or quiver. 

                            52) barb_linewidth (Float) - Default = 0.5. The width or thickness of the wind barb. 

                            53) quiver_linewidth (Float) - Default = 0.5. The width or thickness of the quiver. 

                            54) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            55) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
    
        Return: Saves individual images to the RTMA subfolder.
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    data_24 = data_24
    time_24 = time_24
    state = 'ak'
    cwa = cwa

    if gacc_region == 'OSCC' or gacc_region == 'oscc' or gacc_region == 'SOPS' or gacc_region == 'sops' or gacc_region == 'RMCC' or gacc_region == 'rmcc' or gacc_region == 'RM' or gacc_region == 'rm':
        if barb_quiver_fontsize <= 6:
            barb_quiver_fontsize = 8
    else:
        pass


    if barbs_or_quivers == 'barbs' or barbs_or_quivers == 'Barbs' or barbs_or_quivers == 'BARBS' or barbs_or_quivers == 'B' or barbs_or_quivers == 'b':

        barbs = True

    if barbs_or_quivers == 'quivers' or barbs_or_quivers == 'Quivers' or barbs_or_quivers == 'QUIVERS' or barbs_or_quivers == 'Q' or barbs_or_quivers == 'q':

        barbs = False


    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    contourf = np.arange(-20, 21, 1)

    linewidths = 1

    labels = contourf[::2]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', False, '24 Hour Wind Speed & Direction Comparison')


        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8

    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect

    
    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.wind_speed_change_colormap()

    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False

    if test == True and time == None:
        
        try:
            ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
            u = ds['ugrd10m']
            v = ds['vgrd10m']
            u_24 = ds_24['ugrd10m']
            v_24 = ds_24['vgrd10m']
            ws = ds['wind10m']
            ws_24 = ds_24['wind10m']
            lon = ds['lon']
            lat = ds['lat']
            lon_24 = ds_24['lon']
            lat_24 = ds_24['lat']
            ws = unit_conversion.meters_per_second_to_mph(ws)
            ws_24 = unit_conversion.meters_per_second_to_mph(ws_24)
            diff = ws[0, :, :] - ws_24[0, :, :]
            lon_2d, lat_2d = np.meshgrid(lon, lat)
            lon_24_2d, lat_24_2d = np.meshgrid(lon_24, lat_24)
            u = unit_conversion.meters_per_second_to_mph(u)
            v = unit_conversion.meters_per_second_to_mph(v)
            u_24 = unit_conversion.meters_per_second_to_mph(u_24)
            v_24 = unit_conversion.meters_per_second_to_mph(v_24)            
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time
            ds_24 = data_24
            rtma_time_24 = time_24

            u = ds['ugrd10m']
            v = ds['vgrd10m']
            u_24 = ds_24['ugrd10m']
            v_24 = ds_24['vgrd10m']
            ws = ds['wind10m']
            ws_24 = ds_24['wind10m']
            lon = ds['lon']
            lat = ds['lat']
            lon_24 = ds_24['lon']
            lat_24 = ds_24['lat']
            ws = unit_conversion.meters_per_second_to_mph(ws)
            ws_24 = unit_conversion.meters_per_second_to_mph(ws_24)
            diff = ws[0, :, :] - ws_24[0, :, :]
            lon_2d, lat_2d = np.meshgrid(lon, lat)
            lon_24_2d, lat_24_2d = np.meshgrid(lon_24, lat_24)
            u = unit_conversion.meters_per_second_to_mph(u)
            v = unit_conversion.meters_per_second_to_mph(v)
            u_24 = unit_conversion.meters_per_second_to_mph(u_24)
            v_24 = unit_conversion.meters_per_second_to_mph(v_24)     

            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, ds_24, rtma_time, rtma_time_24 = RTMA_Alaska.get_RTMA_24_hour_comparison_datasets(utc_time)
                u = ds['ugrd10m']
                v = ds['vgrd10m']
                u_24 = ds_24['ugrd10m']
                v_24 = ds_24['vgrd10m']
                ws = ds['wind10m']
                ws_24 = ds_24['wind10m']
                lon = ds['lon']
                lat = ds['lat']
                lon_24 = ds_24['lon']
                lat_24 = ds_24['lat']
                ws = unit_conversion.meters_per_second_to_mph(ws)
                ws_24 = unit_conversion.meters_per_second_to_mph(ws_24)
                diff = ws[0, :, :] - ws_24[0, :, :]
                lon_2d, lat_2d = np.meshgrid(lon, lat)
                lon_24_2d, lat_24_2d = np.meshgrid(lon_24, lat_24)
                u = unit_conversion.meters_per_second_to_mph(u)
                v = unit_conversion.meters_per_second_to_mph(v)
                u_24 = unit_conversion.meters_per_second_to_mph(u_24)
                v_24 = unit_conversion.meters_per_second_to_mph(v_24)            
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass    
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)
    
    rtma_time_24 = rtma_time_24.replace(tzinfo=from_zone)
    rtma_time_24 = rtma_time_24.astimezone(to_zone)
    rtma_time_utc_24 = rtma_time_24.astimezone(from_zone)   

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.patch.set_facecolor('aliceblue')

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if cwa == None:
        ax.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax.set_extent([-170, -140.75, 59, 72], datacrs)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
    if show_rivers == True:
        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=3)
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

    if barbs == True:
    
        plt.title("RTMA Wind Speed & Direction Comparison\n[ΔMPH (Shaded) + Wind Barbs]", fontsize=title_fontsize, fontweight='bold', loc='left')

    if barbs == False:

        plt.title("RTMA Wind Speed & Direction Comparison\n[ΔMPH (Shaded) + Wind Vectors]", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Current: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")\n[Current - 24HRS]: " + rtma_time_24.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc_24.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    cs = ax.contourf(lon, lat, diff[:, :], 
                     transform=ccrs.PlateCarree(), levels=contourf, cmap=cmap, alpha=alpha, extend='both', zorder=2)

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    if barbs == True:

        stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                         transform=ccrs.PlateCarree(), zorder=9, fontsize=barb_quiver_fontsize, clip_on=True)
    
        stn1 = mpplots.StationPlot(ax, lon_24_2d[::decimate, ::decimate], lat_24_2d[::decimate, ::decimate],
                         transform=ccrs.PlateCarree(), zorder=9, fontsize=barb_quiver_fontsize, clip_on=True)

        stn.plot_barb(u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='red', label=rtma_time.strftime('%m/%d %H:00'), alpha=barb_quiver_alpha, zorder=9, linewidth=barb_linewidth)

        stn1.plot_barb(u_24[0, :, :][::decimate, ::decimate], v_24[0, :, :][::decimate, ::decimate], color='blue', label=rtma_time_24.strftime('%m/%d %H:00'), alpha=barb_quiver_alpha, zorder=9, linewidth=barb_linewidth)

        file_name_end = ' WIND BARBS'

    if barbs == False:

        minshaft, headlength, headwidth = dims.get_quiver_dims(state, gacc_region)

        ax.quiver(lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate], u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='red', minshaft=minshaft, headlength=headlength, headwidth=headwidth, alpha=barb_quiver_alpha, label=rtma_time.strftime('%m/%d %H:00'), zorder=9, linewidth=quiver_linewidth, transform=ccrs.PlateCarree())
    
        ax.quiver(lon_24_2d[::decimate, ::decimate], lat_24_2d[::decimate, ::decimate], u_24[0, :, :][::decimate, ::decimate], v_24[0, :, :][::decimate, ::decimate], color='blue', minshaft=minshaft, headlength=headlength, headwidth=headwidth, alpha=barb_quiver_alpha, label=rtma_time_24.strftime('%m/%d %H:00'), zorder=9, linewidth=quiver_linewidth, transform=ccrs.PlateCarree())

        file_name_end = ' WIND VECTORS'

    cbar = fig.colorbar(cs, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=labels)
    cbar.set_label(label="Wind Speed Difference (ΔMPH)", size=colorbar_fontsize, fontweight='bold')

    x_loc, y_loc = dims.get_label_coords(state, gacc_region)
    
    leg = ax.legend(loc=(x_loc, y_loc), framealpha=1, fontsize='x-small')
    leg.set_zorder(12)

    fname = '24HR RTMA WIND SPEED & DIRECTION COMPARISON'+ file_name_end
    
    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, fname, reference_system)
    file_functions.update_images(fig, path, gif_path, fname)


def plot_hot_dry_and_windy_areas(pre_greenup_temperature_threshold=5, post_greenup_temperature_threshold=15, low_rh_threshold=80, high_wind_threshold=5, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, sample_point_type='barbs', barb_quiver_linewidth=1, barb_fontsize=10, row1=None, row2=None, row3=None, row4=None, row5=None, row6=None, col1=None, col2=None, col3=None, col4=None, col5=None, col6=None, tick=9, aspect=30):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Dry and Windy Areas along with the components. 
    
        Required Arguments: None

        Optional Arguments: 1) low_rh_threshold (Integer) - Default = 15%. Threshold for low relative humidity. Any value less than this threshold is considered "dry."

                            2) high_wind_threshold (Integer) - Default = 25 MPH. Threshold for high winds. Any value greater than this threshold is considered "windy."         
        
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

                            7) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            8) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            9) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            10) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            11) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            12) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            13) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            14) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            15) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            16) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            17) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                                                   
    
                            18) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            19) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            20) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            21) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            22) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            23) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            24) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            25) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            26) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            27) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            28) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            29) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            30) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            31) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            32) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            35) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            36) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            37) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            38) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            39) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            40) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            41) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            42) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            43) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            44) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            45) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            46) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            47) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            48) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            49) sample_point_type (String) - Default='barbs'. The type of sample point. The options are either wind barbs or the raw numbers for the wind speeds. Wind barbs
                                are the default since barbs incorporates wind direction.

                            50) barb_quiver_linewidth (Float) - Default = 0.5. The width or thickness of the wind barb or quiver. 

                            51) barb_fontsize (Integer) - Default = 6. Fontsize of the barb. 

                            52) row1 (Integer) - Default=None. The starting row for the first subplot (the main subplot). The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot. 

                            53) row2 (Integer) - Default=None. The ending row for the first subplot (the main subplot). The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot. 

                            54) row3 (Integer) - Default=None. The starting row for the second subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.    

                            55) row4 (Integer) - Default=None. The ending row for the second subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot. 

                            56) row5 (Integer) - Default=None. The starting row for the third subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot. 

                            57) row6 (Integer) - Default=None. The ending row for the third subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot. 

                            58) col1 (Integer) - Default=None. The starting column for the first subplot (the main subplot). The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.

                            59) col2 (Integer) - Default=None. The ending column for the first subplot (the main subplot). The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.

                            60) col3 (Integer) - Default=None. The starting column for the second subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.

                            61) col4 (Integer) - Default=None. The ending column for the second subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.

                            62) col5 (Integer) - Default=None. The starting column for the third subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.

                            63) col6 (Integer) - Default=None. The starting column for the third subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.
                            
                            64) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
                            
                            65) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 
    
        Return: Saves individual images to the RTMA subfolder.
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa
    low_rh_threshold = low_rh_threshold
    high_wind_threshold = high_wind_threshold

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()


    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    low_rh_thresh = low_rh_threshold + 1

    rh_contourf = np.arange(0, low_rh_thresh, 1)

    high_wind = high_wind_threshold + 36
    
    wind_speed_contourf = np.arange(high_wind_threshold, high_wind, 1)

    if low_rh_threshold <= 15:
        rh_labels = rh_contourf
    elif low_rh_threshold > 15 and low_rh_threshold < 40:
        if (low_rh_threshold % 2) == 0:
            rh_labels = rh_contourf[::2]
        else:
            rh_labels = rh_contourf[::5]
    else:
        rh_labels = rh_contourf[::5]
        
    wind_labels = wind_speed_contourf[::5]

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
    

    directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', True, 'Dry and Windy Areas')
        

    mpl.rcParams['xtick.labelsize'] = tick
    mpl.rcParams['ytick.labelsize'] = tick

    row1, row2, row3, row4, row5, row6, col1, col2, col3, col4, col5, col6 = 0, 8, 5, 10, 5, 10, 0, 10, 0, 5, 5, 10
    
    if cwa == None:
        title_fontsize, subplot_title_fontsize = 9, 8
    if cwa == 'AER' or cwa == 'aer':
        title_fontsize, subplot_title_fontsize = 9, 8
    if cwa == 'AJK' or cwa == 'ajk':
        title_fontsize, subplot_title_fontsize = 9, 8
    if cwa == 'AFG' or cwa == 'afg':
        title_fontsize, subplot_title_fontsize = 9, 8
    if cwa == 'ALU' or cwa == 'alu':
        title_fontsize, subplot_title_fontsize = 9, 8

    fig_x_length = fig_x_length + 2
    fig_y_length = fig_y_length + 2
    sample_point_fontsize = sample_point_fontsize - 2

    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap_pre = colormaps.red_flag_warning_criteria_colormap()
    cmap_post = colormaps.red_flag_warning_criteria_colormap_alt()

    low_rh_cmap = colormaps.low_relative_humidity_colormap()

    wind_cmap = colormaps.wind_speed_colormap()
    
    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['wind10m']
            u = ds['ugrd10m']
            v = ds['vgrd10m']
            u = unit_conversion.meters_per_second_to_mph(u)
            v = unit_conversion.meters_per_second_to_mph(v)
            rtma_wind = unit_conversion.meters_per_second_to_mph(rtma_wind)
            rtma_rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            rtma_temp = unit_conversion.celsius_to_fahrenheit(temp)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :] 
            rtma_temp = rtma_temp[0, :, :]
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['wind10m']
            u = ds['ugrd10m']
            v = ds['vgrd10m']
            u = unit_conversion.meters_per_second_to_mph(u)
            v = unit_conversion.meters_per_second_to_mph(v)
            rtma_wind = unit_conversion.meters_per_second_to_mph(rtma_wind)
            rtma_rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
            rtma_temp = unit_conversion.celsius_to_fahrenheit(temp)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :] 
            rtma_temp = rtma_temp[0, :, :]
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
                dwpt = ds['dpt2m']
                temp = temp - 273.15
                dwpt = dwpt - 273.15
                rtma_wind = ds['wind10m']
                u = ds['ugrd10m']
                v = ds['vgrd10m']
                u = unit_conversion.meters_per_second_to_mph(u)
                v = unit_conversion.meters_per_second_to_mph(v)
                rtma_wind = unit_conversion.meters_per_second_to_mph(rtma_wind)
                rtma_rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
                rtma_temp = unit_conversion.celsius_to_fahrenheit(temp)
        
                rtma_rh = rtma_rh[0, :, :]
                rtma_wind = rtma_wind[0, :, :] 
                rtma_temp = rtma_temp[0, :, :]
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass    
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    mask_pre = (rtma_rh <= low_rh_threshold) & (rtma_wind >= high_wind_threshold) & (rtma_temp >= pre_greenup_temperature_threshold)
    lon_pre = mask_pre['lon']
    lat_pre = mask_pre['lat']

    lons = ds['lon']
    lats = ds['lat']

    mask_post = (rtma_rh <= low_rh_threshold) & (rtma_wind >= high_wind_threshold) & (rtma_temp >= post_greenup_temperature_threshold)
    lon_post = mask_post['lon']
    lat_post = mask_post['lat']

    lons = ds['lon']
    lats = ds['lat']

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')
    
    gs = gridspec.GridSpec(10, 10)

    ax1 = fig.add_subplot(gs[row1:row2, col1:col2], projection=ccrs.PlateCarree())
    if cwa == None:
        ax1.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax1.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax1.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax1.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax1.set_extent([-170, -140.75, 59, 72], datacrs)
    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=8)
    ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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
    
    plt.title("RTMA Dry & Windy Areas\n[Relative Humidity <= "+str(low_rh_threshold)+" (%) & Wind Speed >= "+str(high_wind_threshold)+" (MPH)]", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax1.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    try:
        ax1.pcolormesh(lon_pre,lat_pre,mask_pre, transform=ccrs.PlateCarree(), color='red', zorder=2, alpha=0.3)

    except Exception as e:
        pass   

    try:
        ax1.pcolormesh(lon_post,lat_post,mask_post, transform=ccrs.PlateCarree(), color='purple', zorder=3, alpha=0.3)

    except Exception as e:
        pass   

    ax2 = fig.add_subplot(gs[row3:row4, col3:col4], projection=ccrs.PlateCarree())
    if cwa == None:
        ax2.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax2.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax2.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax2.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax2.set_extent([-170, -140.75, 59, 72], datacrs)
    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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

    cs1 = ax2.contourf(lons, lats, rtma_rh[:, :], 
                     transform=ccrs.PlateCarree(), levels=rh_contourf, cmap=low_rh_cmap, alpha=alpha)

    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=rh_labels)
    cbar1.set_label(label="Relative Humidity (%)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    decimate = decimate *2

    plot_lon, plot_lat = np.meshgrid(lons[::decimate], lats[::decimate])
    plot_lons, plot_lats = np.meshgrid(lons, lats)

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        stn1 = mpplots.StationPlot(ax2, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        rtma_rh = rtma_rh[::decimate, ::decimate].to_numpy().flatten()
    
        stn1.plot_parameter('C', rtma_rh, color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    ax3 = fig.add_subplot(gs[row5:row6, col5:col6], projection=ccrs.PlateCarree())
    if cwa == None:
        ax3.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax3.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax3.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax3.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax3.set_extent([-170, -140.75, 59, 72], datacrs)
    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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

    cs2 = ax3.contourf(lons, lats, rtma_wind[:, :], 
                     transform=ccrs.PlateCarree(), levels=wind_speed_contourf, cmap=wind_cmap, alpha=alpha, extend='max', zorder=2)

    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=wind_labels)
    cbar2.set_label(label="Wind Speed (MPH)", size=colorbar_fontsize, fontweight='bold')

    plot_lon, plot_lat = np.meshgrid(lons[::decimate], lats[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        if sample_point_type == 'points':

            stn2 = mpplots.StationPlot(ax3, plot_lon.flatten(), plot_lat.flatten(),
                                         transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
        
            rtma_wind = rtma_wind[::decimate, ::decimate].to_numpy().flatten()
        
            stn2.plot_parameter('C', rtma_wind, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

        fname_end = ' SAMPLE POINTS'

        if sample_point_type == 'barbs':


            barb_fontsize = 8


            stn2 = mpplots.StationPlot(ax3, plot_lons[::decimate, ::decimate], plot_lats[::decimate, ::decimate],
                             transform=ccrs.PlateCarree(), zorder=11, fontsize=barb_fontsize, clip_on=True)
    
            stn2.plot_barb(u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='lime', label=rtma_time.strftime('%m/%d %H:00'), zorder=11, linewidth=barb_quiver_linewidth)
    
            fname_end = ' WIND BARBS'

        if sample_point_type == 'quivers' or sample_point_type == 'vectors':

            minshaft, headlength, headwidth = 0.000005, 5, 3
    
            ax3.quiver(plot_lons[::decimate, ::decimate], plot_lats[::decimate, ::decimate], u[0, :, :][::decimate, ::decimate], v[0, :, :][::decimate, ::decimate], color='lime', minshaft=minshaft, headlength=headlength, headwidth=headwidth, zorder=11, linewidth=barb_quiver_linewidth, transform=ccrs.PlateCarree())
    
            fname_end = ' WIND VECTORS'            
            
    else:
        pass

    fname = 'RTMA DRY & WINDY AREAS' + fname_end

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, fname, reference_system)
    file_functions.update_images(fig, path, gif_path, fname)


def plot_hot_dry_and_gusty_areas(pre_greenup_temperature_threshold=65, post_greenup_temperature_threshold=75, low_rh_threshold=25, high_wind_threshold=15, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=1, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', show_sample_points=True, sample_point_fontsize=8, alpha=0.5, data=None, time=None, cwa=None, colorbar_pad=0.02, row1=None, row2=None, row3=None, row4=None, row5=None, row6=None, col1=None, col2=None, col3=None, col4=None, col5=None, col6=None, tick=9, aspect=30):

    r'''
        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Dry and Gusty Areas along with the components. 
    
        Required Arguments: None

        Optional Arguments: 1) low_rh_threshold (Integer) - Default = 15%. Threshold for low relative humidity. Any value less than this threshold is considered "dry."

                            2) high_wind_threshold (Integer) - Default = 25 MPH. Threshold for high wind gusts. Any value greater than this threshold is considered "gusty."         
        
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

                            7) fig_x_length (Integer) - Default = None. The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 

                            8) fig_y_length (Integer) - Default = None. The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            9) signature_x_position (Integer or Float) - Default = None. The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            10) signature_y_position (Integer or Float) - Default = None. The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            11) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            12) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            13) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            14) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            15) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            16) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            17) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                                                   
    
                            18) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            19) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            20) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            21) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            22) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            23) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            24) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            25) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            26) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            27) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            28) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            29) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            30) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            31) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            32) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            33) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            34) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            35) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            36) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            37) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            38) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            39) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            40) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            41) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            42) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            43) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            44) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            45) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            46) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                                changed to None. 

                            47) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

                            48) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            49) sample_point_type (String) - Default='barbs'. The type of sample point. The options are either wind barbs or the raw numbers for the wind speeds. Wind barbs
                                are the default since barbs incorporates wind direction.

                            50) barb_quiver_linewidth (Float) - Default = 0.5. The width or thickness of the wind barb or quiver. 

                            51) barb_fontsize (Integer) - Default = 6. Fontsize of the barb. 

                            52) row1 (Integer) - Default=None. The starting row for the first subplot (the main subplot). The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot. 

                            53) row2 (Integer) - Default=None. The ending row for the first subplot (the main subplot). The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot. 

                            54) row3 (Integer) - Default=None. The starting row for the second subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.    

                            55) row4 (Integer) - Default=None. The ending row for the second subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot. 

                            56) row5 (Integer) - Default=None. The starting row for the third subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot. 

                            57) row6 (Integer) - Default=None. The ending row for the third subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot. 

                            58) col1 (Integer) - Default=None. The starting column for the first subplot (the main subplot). The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.

                            59) col2 (Integer) - Default=None. The ending column for the first subplot (the main subplot). The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.

                            60) col3 (Integer) - Default=None. The starting column for the second subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.

                            61) col4 (Integer) - Default=None. The ending column for the second subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.

                            62) col5 (Integer) - Default=None. The starting column for the third subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.

                            63) col6 (Integer) - Default=None. The starting column for the third subplot. The range is from 0 to 10. If set to default, the proper settings are imported from the
                                settings module. Only edit this when making a custom plot.
                            
                            64) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
                            
                            65) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 
    
        Return: Saves individual images to the RTMA subfolder. 
    
    '''
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    data = data
    time = time
    state = 'ak'
    cwa = cwa
    low_rh_threshold = low_rh_threshold
    high_wind_threshold = high_wind_threshold

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()


    if sample_point_fontsize != 8:
        sp_font_default = False
        sp_fontsize = sample_point_fontsize
    else:
        sp_font_default = True

    low_rh_thresh = low_rh_threshold + 1

    rh_contourf = np.arange(0, low_rh_thresh, 1)

    high_wind = high_wind_threshold + 36
    wind_speed_contourf = np.arange(high_wind_threshold, high_wind, 1)

    if low_rh_threshold <= 15:
        rh_labels = rh_contourf
    elif low_rh_threshold > 15 and low_rh_threshold < 40:
        if (low_rh_threshold % 2) == 0:
            rh_labels = rh_contourf[::2]
        else:
            rh_labels = rh_contourf[::5]
    else:
        rh_labels = rh_contourf[::5]
        
    wind_labels = wind_speed_contourf[::5]

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
    
    if state != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'rtma', True, 'Dry and Gusty Areas')
            

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick

        row1, row2, row3, row4, row5, row6, col1, col2, col3, col4, col5, col6 = dims.get_gridspec_dims(state, gacc_region)

        if cwa == None:
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AER' or cwa == 'aer':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AJK' or cwa == 'ajk':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'AFG' or cwa == 'afg':
            title_fontsize, subplot_title_fontsize = 9, 8
        if cwa == 'ALU' or cwa == 'alu':
            title_fontsize, subplot_title_fontsize = 9, 8
    
    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None:

        fig_x_length = fig_x_length
        fig_y_length = fig_y_length
        signature_x_position = signature_x_position
        signature_y_position = signature_y_position
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        state = 'Custom'
        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick
        aspect=aspect
        row1 = row1
        row2 = row2 
        row3 = row3
        row4 = row4 
        row5 = row5
        row6 = row6 
        col1 = col1 
        col2 = col2
        col3 = col3 
        col4 = col4 
        col5 = col5 
        col6 = col6

    fig_x_length = fig_x_length + 2
    fig_y_length = fig_y_length + 2
    sample_point_fontsize = sample_point_fontsize - 2

    
    local_time, utc_time = standard.plot_creation_time()

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    cmap = colormaps.red_flag_warning_criteria_colormap()

    low_rh_cmap = colormaps.low_relative_humidity_colormap()

    wind_cmap = colormaps.wind_speed_colormap()
    
    try:
        if data == None:
            test = True
        if data != None:
            test = False
    except Exception as a:
        test = False


    if test == True and time == None:
        
        try:
            ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['gust10m']
            rtma_wind = unit_conversion.meters_per_second_to_mph(rtma_wind)
            rtma_rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :] 
                        
            print("Unpacked the data successfully!")
        except Exception as e:
            pass

    elif test == False and time != None:
        try:
            ds = data
            rtma_time = time
            temp = ds['tmp2m']
            dwpt = ds['dpt2m']
            temp = temp - 273.15
            dwpt = dwpt - 273.15
            rtma_wind = ds['gust10m']
            rtma_wind = unit_conversion.meters_per_second_to_mph(rtma_wind)
            rtma_rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
    
            rtma_rh = rtma_rh[0, :, :]
            rtma_wind = rtma_wind[0, :, :] 
            print("Unpacked the data successfully!")
        except Exception as e:
            print("There was a problem with the data passed in by the user.\nNo worries! FireWxPy will now try downloading and unpacking the data for you!")

            try:
                ds, rtma_time = RTMA_Alaska.get_RTMA_dataset(utc_time)
                temp = ds['tmp2m']
                dwpt = ds['dpt2m']
                temp = temp - 273.15
                dwpt = dwpt - 273.15
                rtma_wind = ds['gust10m']
                rtma_wind = unit_conversion.meters_per_second_to_mph(rtma_wind)
                rtma_rh = Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(temp, dwpt)
        
                rtma_rh = rtma_rh[0, :, :]
                rtma_wind = rtma_wind[0, :, :] 
                            
                print("Unpacked the data successfully!")
            except Exception as e:
                pass    
        
    else:
        print("Error! Both values either need to have a value of None or have an array of the RTMA Data and RTMA Timestamp.")

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    rtma_time = rtma_time.replace(tzinfo=from_zone)
    rtma_time = rtma_time.astimezone(to_zone)
    rtma_time_utc = rtma_time.astimezone(from_zone)

    mask = (rtma_rh <= low_rh_threshold) & (rtma_wind >= high_wind_threshold)
    lon = mask['lon']
    lat = mask['lat']

    lons = ds['lon']
    lats = ds['lat']

    fig = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig.set_facecolor('aliceblue')

    gs = gridspec.GridSpec(10, 10)

    ax1 = fig.add_subplot(gs[row1:row2, col1:col2], projection=ccrs.PlateCarree())
    if cwa == None:
        ax1.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax1.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax1.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax1.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax1.set_extent([-170, -140.75, 59, 72], datacrs)
    ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=8)
    ax1.add_feature(cfeature.LAKES, color='lightcyan', zorder=4)
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
    
    plt.title("RTMA Dry & Gusty Areas\n[Relative Humidity <= "+str(low_rh_threshold)+" (%) & Wind Gust >= "+str(high_wind_threshold)+" (MPH)]", fontsize=title_fontsize, fontweight='bold', loc='left')
    
    plt.title("Analysis Valid: " + rtma_time.strftime('%m/%d/%Y %H:00 Local') + " (" + rtma_time_utc.strftime('%H:00 UTC')+")", fontsize=subplot_title_fontsize, fontweight='bold', loc='right')

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    ax1.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: "+reference_system+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=signature_fontsize, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)

    try:
        ax1.pcolormesh(lon,lat,mask, transform=ccrs.PlateCarree(),cmap=cmap, zorder=2, alpha=alpha)

    except Exception as e:
        pass   

    ax2 = fig.add_subplot(gs[row3:row4, col3:col4], projection=ccrs.PlateCarree())
    if cwa == None:
        ax2.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax2.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax2.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax2.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax2.set_extent([-170, -140.75, 59, 72], datacrs)
    ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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

    cs1 = ax2.contourf(lons, lats, rtma_rh[:, :], 
                     transform=ccrs.PlateCarree(), levels=rh_contourf, cmap=low_rh_cmap, alpha=alpha)

    cbar1 = fig.colorbar(cs1, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=rh_labels)
    cbar1.set_label(label="Relative Humidity (%)", size=colorbar_fontsize, fontweight='bold')

    if cwa == None:
        decimate = 60
    if cwa == 'AER' or cwa == 'aer':
        decimate = 20
    if cwa == 'ALU' or cwa == 'alu':
        decimate = 20
    if cwa == 'AJK' or cwa == 'ajk':
        decimate = 20
    if cwa == 'AFG' or cwa == 'afg':
        decimate = 40

    decimate = decimate * 2

    plot_lon, plot_lat = np.meshgrid(lons[::decimate], lats[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        stn1 = mpplots.StationPlot(ax2, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        rtma_rh = rtma_rh[::decimate, ::decimate].to_numpy().flatten()
    
        stn1.plot_parameter('C', rtma_rh, color='blue', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    ax3 = fig.add_subplot(gs[row5:row6, col5:col6], projection=ccrs.PlateCarree())
    if cwa == None:
        ax3.set_extent([-170, -125, 50, 72], datacrs)
    if cwa == 'AER' or cwa == 'aer':
        ax3.set_extent([-155, -140.75, 55.5, 64.5], datacrs)
    if cwa == 'ALU' or cwa == 'alu':
        ax3.set_extent([-170, -151, 52, 62.9], datacrs)
    if cwa == 'AJK' or cwa == 'ajk':
        ax3.set_extent([-145, -129.5, 54, 60.75], datacrs)
    if cwa == 'AFG' or cwa == 'afg':
        ax3.set_extent([-170, -140.75, 59, 72], datacrs)
    ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
    ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
    ax3.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
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

    cs2 = ax3.contourf(lons, lats, rtma_wind[:, :], 
                     transform=ccrs.PlateCarree(), levels=wind_speed_contourf, cmap=wind_cmap, alpha=alpha, extend='max', zorder=2)

    cbar2 = fig.colorbar(cs2, shrink=color_table_shrink, pad=colorbar_pad, location='bottom', aspect=aspect, ticks=wind_labels)
    cbar2.set_label(label="Wind Gust (MPH)", size=colorbar_fontsize, fontweight='bold')

    plot_lon, plot_lat = np.meshgrid(lons[::decimate], lats[::decimate])

    if sp_font_default == False:
        sample_point_fontsize = sp_fontsize
    else:
        sample_point_fontsize = sample_point_fontsize

    if show_sample_points == True:

        stn2 = mpplots.StationPlot(ax3, plot_lon.flatten(), plot_lat.flatten(),
                                     transform=ccrs.PlateCarree(), fontsize=sample_point_fontsize, zorder=7, clip_on=True)
    
        rtma_wind = rtma_wind[::decimate, ::decimate].to_numpy().flatten()
    
        stn2.plot_parameter('C', rtma_wind, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    else:
        pass

    path, gif_path = file_functions.check_file_paths_alaska(state, cwa, 'RTMA DRY & GUSTY AREAS', reference_system)
    file_functions.update_images(fig, path, gif_path, 'RTMA DRY & GUSTY AREAS')

