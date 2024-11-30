'''
This file hosts the functions to plot the latest critical fire weather outlook and dry lightning forecast
from the NOAA Storm Prediction Center (SPC). 

This file has 2 classes which are based on the geographical reference perspective:

1) Counties_Perspective: Uses state and county boundaries. 
2) Predictive_Services_Areas_Perspective: Uses Geographic Area Coordination Center (GACC) and 
                                          Predictive Services Areas (PSAs) boundaries. 

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
import firewxpy.geometry as geometry
import firewxpy.colormaps as colormaps
import firewxpy.standard as standard
import firewxpy.settings as settings
import firewxpy.dims as dims
import warnings
warnings.filterwarnings('ignore')

from metpy.plots import USCOUNTIES
from metpy.plots import colortables
from dateutil import tz
from firewxpy.utilities import file_functions
from firewxpy.data_access import NDFD_CONUS

mpl.rcParams['font.weight'] = 'bold'

def plot_critical_fire_weather_risk_outlook(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, state='us', gacc_region=None, cwa=None, aspect=30, colorbar_pad=0.02):

    r'''
        This function plots the latest available Storm Prediction Center Critical Fire Weather Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 
    
                            2) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 
    
                            3) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 
    
                            4) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.
              
                            5) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            6) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            7) signature_x_position (Integer or Float) - The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            8) signature_y_position (Integer or Float) - The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            9) color_table_shrink (Integer or Float) - This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." The default setting is None. 
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
    
                            15) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide state borders. 

                            16) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide county borders. 

                            17) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            17) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            18) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            19) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            20) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            21) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            22) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            23) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            24) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            25) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 


                            26) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            27) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

                            28) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            29) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            30) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            31) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
    '''


    local_time, utc_time = standard.plot_creation_time()
    grid_time_interval = 24

    if gacc_region != None:
        state = None
    else:
        state = state
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    cmap = colormaps.SPC_Critical_Fire_Weather_Risk_Outlook_colormap()
        
    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    x1, x2, x3, y = dims.get_colorbar_label_coords(state, gacc_region, 'critical fire')

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
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'spc', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick


    if state == None and gacc_region != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_gacc_region_data_and_coords(gacc_region, 'spc', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick


    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None and gacc_region == None:

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


        if file_path == None:
            directory_name = settings.check_NDFD_directory_name('us')
        else:
            directory_name = settings.check_NDFD_directory_name(directory_name)

    else:
        pass

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    directory_name = settings.check_NDFD_directory_name(directory_name)

    if file_path == None:

        grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.critfireo.bin')

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.critfireo.bin', 24, False, count_short, count_extended, directory_name)

    if file_path != None:

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 24, False, count_short, count_extended, directory_name)

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
        
    files = count

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    
    figs = [] 

    fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig1.set_facecolor('aliceblue')
    
    fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

    ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax1.set_title('SPC Critical Fire Wx Forecast [Day 1]', fontsize=title_fontsize, fontweight='bold', loc='left')
    
    ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 12, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar1 = fig1.colorbar(cs1, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar1.set_ticks([])

    fig1.text(x1, y,'ELEVATED', fontsize=legend_fontsize, fontweight='bold')
    fig1.text(x2, y,'CRITICAL', fontsize=legend_fontsize, fontweight='bold')
    fig1.text(x3, y,'EXTREME', fontsize=legend_fontsize, fontweight='bold')
    
    fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig2.set_facecolor('aliceblue')
    fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
    ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax2.set_title('SPC Critical Fire Wx Forecast [Day 2]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
    ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 12, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar2 = fig2.colorbar(cs2, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar2.set_ticks([])

    fig2.text(x1, y,'ELEVATED', fontsize=legend_fontsize, fontweight='bold')
    fig2.text(x2, y,'CRITICAL', fontsize=legend_fontsize, fontweight='bold')
    fig2.text(x3, y,'EXTREME', fontsize=legend_fontsize, fontweight='bold')

    fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig3.set_facecolor('aliceblue')
    fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

    ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax3.set_title('SPC Critical Fire Wx Forecast [Day 3]', fontsize=title_fontsize, fontweight='bold', loc='left')
    
    ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 12, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar3 = fig3.colorbar(cs3, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar3.set_ticks([])

    fig3.text(x1, y,'ELEVATED', fontsize=legend_fontsize, fontweight='bold')
    fig3.text(x2, y,'CRITICAL', fontsize=legend_fontsize, fontweight='bold')
    fig3.text(x3, y,'EXTREME', fontsize=legend_fontsize, fontweight='bold')
    
    fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig4.set_facecolor('aliceblue')
    fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

    ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax4.set_title('SPC Critical Fire Wx Forecast [Day 4]', fontsize=title_fontsize, fontweight='bold', loc='left')
    
    ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 12, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar4 = fig4.colorbar(cs4, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar4.set_ticks([])

    fig4.text(x1, y,'ELEVATED', fontsize=legend_fontsize, fontweight='bold')
    fig4.text(x2, y,'CRITICAL', fontsize=legend_fontsize, fontweight='bold')
    fig4.text(x3, y,'EXTREME', fontsize=legend_fontsize, fontweight='bold')

    fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig5.set_facecolor('aliceblue')
    fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

    ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
    ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax5.set_title('SPC Critical Fire Wx Forecast [Day 5]', fontsize=title_fontsize, fontweight='bold', loc='left')
    
    ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(4, 12, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar5 = fig5.colorbar(cs5, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar5.set_ticks([])

    fig5.text(x1, y,'ELEVATED', fontsize=legend_fontsize, fontweight='bold')
    fig5.text(x2, y,'CRITICAL', fontsize=legend_fontsize, fontweight='bold')
    fig5.text(x3, y,'EXTREME', fontsize=legend_fontsize, fontweight='bold')

    fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig6.set_facecolor('aliceblue')
    fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)
    
    ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
    ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax6.set_title('SPC Critical Fire Wx Forecast [Day 6]', fontsize=title_fontsize, fontweight='bold', loc='left')
    
    ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(4, 12, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar6 = fig6.colorbar(cs6, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar6.set_ticks([])

    fig6.text(x1, y,'ELEVATED', fontsize=legend_fontsize, fontweight='bold')
    fig6.text(x2, y,'CRITICAL', fontsize=legend_fontsize, fontweight='bold')
    fig6.text(x3, y,'EXTREME', fontsize=legend_fontsize, fontweight='bold')

    if test_7 == True:

        fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig7.set_facecolor('aliceblue')
        fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
        ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

        ax7.set_title('SPC Critical Fire Wx Forecast [Day 7]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(4, 12, 2), cmap=cmap, transform=datacrs, zorder=2)

        cbar7 = fig7.colorbar(cs7, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
        cbar7.set_ticks([])
    
        fig7.text(x1, y,'ELEVATED', fontsize=legend_fontsize, fontweight='bold')
        fig7.text(x2, y,'CRITICAL', fontsize=legend_fontsize, fontweight='bold')
        fig7.text(x3, y,'EXTREME', fontsize=legend_fontsize, fontweight='bold')
    
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

    path, gif_path = file_functions.check_file_paths(state, gacc_region, 'SPC CRITICAL FIRE WEATHER OUTLOOK', reference_system)
    file_functions.update_images(figs, path, gif_path, 'SPC CRITICAL FIRE WEATHER OUTLOOK')


def plot_dry_lightning_outlook(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, fig_x_length=None, fig_y_length=None, signature_x_position=None, signature_y_position=None, color_table_shrink=0.7, title_fontsize=12, subplot_title_fontsize=10, signature_fontsize=10, colorbar_fontsize=8, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=2, county_border_linewidth=1, gacc_border_linewidth=2, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', psa_color='black', gacc_color='black', cwa_color='black', fwz_color='black', pz_color='black', alpha=0.5, directory_name='CONUS', file_path=None, data_array=None, count_short=None, count_extended=None, state='us', gacc_region=None, cwa=None, aspect=30, colorbar_pad=0.02):

    r'''
        This function plots the latest available Storm Prediction Dry Lightning Forecast. 
    
        Required Arguments: None

        Optional Arguments: 1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 
    
                            2) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Negative values denote the western hemisphere and positive 
                               values denote the eastern hemisphere. 
    
                            3) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere. 
    
                            4) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees. 
                               The default setting is None. If set to None, the user must select a state or gacc_region. 
                               This setting should be changed from None to an integer or float value if the user wishes to
                               have a custom area selected. Positive values denote the northern hemisphere and negative 
                               values denote the southern hemisphere.
              
                            5) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            6) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 
                               The default setting is None since preset values are called from the settings module 
                               for each state and/or gacc_region. This parameter is to be changed if the user selects
                               a custom area with custom latitude and longitude coordinates. 
    
                            7) signature_x_position (Integer or Float) - The x-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region. 
                            
                            8) signature_y_position (Integer or Float) - The y-position of the signature 
                               The signature is where the credit is given to the developer of FireWxPy and
                               to the source at which the data is accessed from. The default setting is None. 
                               This setting is only to be changed if the user makes a graphic with custom coordinates
                               since preset values are called from the settings module for each state and/or gacc_region.
                            
                            9) color_table_shrink (Integer or Float) - This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." The default setting is None. 
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
    
                            15) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide state borders. 

                            16) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide county borders. 

                            17) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            17) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            18) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            19) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            20) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            21) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            22) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            23) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            24) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            25) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 


                            26) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            27) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

                            28) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
                                This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
                                binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
                                Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
                                function. 

                            29) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            30) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
                                is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
                                data_access module. This value is to be passed in if and only if the user downloads the data outside 
                                of this function. Default setting is None. 

                            31) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                                If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                                or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                                acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
        Return: Saves individual images to a folder and creates a GIF from those images. 
    '''

    if gacc_region != None:
        state = None
    else:
        state = state

    local_time, utc_time = standard.plot_creation_time()
    grid_time_interval = 24
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    cmap = colormaps.SPC_Dry_Lightning_Risk_Outlook_colormap()

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)
        
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    reference_system = reference_system
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()

    x1, x2, x3, y = dims.get_colorbar_label_coords(state, gacc_region, 'dry lightning')

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
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_state_data_and_coords(state, 'spc', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick


    if state == None and gacc_region != None:
        directory_name, western_bound, eastern_bound, southern_bound, northern_bound, fig_x_length, fig_y_length, signature_x_position, signature_y_position, title_fontsize, subplot_title_fontsize, signature_fontsize, sample_point_fontsize, colorbar_fontsize, color_table_shrink, legend_fontsize, mapcrs, datacrs, title_x_position, aspect, tick = settings.get_gacc_region_data_and_coords(gacc_region, 'spc', False)

        mpl.rcParams['xtick.labelsize'] = tick
        mpl.rcParams['ytick.labelsize'] = tick


    if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None and fig_x_length != None and fig_y_length != None and signature_x_position != None and signature_y_position != None and state == None and gacc_region == None:

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


        if file_path == None:
            directory_name = settings.check_NDFD_directory_name('us')
        else:
            directory_name = settings.check_NDFD_directory_name(directory_name)

    else:
        pass

    PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", psa_color, 'psa')
    
    GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", gacc_color, 'gacc')

    CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", cwa_color, 'cwa')

    FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", fwz_color, 'fwz')

    PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", pz_color, 'pz')

    directory_name = settings.check_NDFD_directory_name(directory_name)

    if file_path == None:

        grbs, ds, count_short, count_extended = NDFD_CONUS.download_NDFD_grids(directory_name, 'ds.dryfireo.bin')

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period('ds.dryfireo.bin', 24, False, count_short, count_extended, directory_name)

    if file_path != None:

        grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard = parsers.NDFD.parse_GRIB_files_full_forecast_period(file_path, 24, False, count_short, count_extended, directory_name)

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
        
    files = count

    
    figs = [] 

    fig1 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig1.set_facecolor('aliceblue')
    fig1.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

    ax1 = fig1.add_subplot(1, 1, 1, projection=mapcrs)
    ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax1.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax1.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax1.set_title('SPC Dry Lightning Forecast [Day 1]', fontsize=title_fontsize, fontweight='bold', loc='left')
    
    ax1.set_title('Start: '+ grb_1_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_1_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs1 = ax1.contourf(lons_1, lats_1, grb_1_vals, levels=np.arange(4, 10, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar1 = fig1.colorbar(cs1, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar1.set_ticks([])

    fig1.text(x1, y,'ISOLATED', fontsize=legend_fontsize, fontweight='bold')
    fig1.text(x2, y,'SCATTERED', fontsize=legend_fontsize, fontweight='bold')
    
    fig2 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig2.set_facecolor('aliceblue')
    fig2.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

    ax2 = fig2.add_subplot(1, 1, 1, projection=mapcrs)
    ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax2.set_title('SPC Dry Lightning Forecast [Day 2]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
    ax2.set_title('Start: '+ grb_2_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_2_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs2 = ax2.contourf(lons_2, lats_2, grb_2_vals, levels=np.arange(4, 10, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar2 = fig2.colorbar(cs2, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar2.set_ticks([])

    fig2.text(x1, y,'ISOLATED', fontsize=legend_fontsize, fontweight='bold')
    fig2.text(x2, y,'SCATTERED', fontsize=legend_fontsize, fontweight='bold')

    fig3 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig3.set_facecolor('aliceblue')
    fig3.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

    ax3 = fig3.add_subplot(1, 1, 1, projection=mapcrs)
    ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax3.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax3.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax3.set_title('SPC Dry Lightning Forecast [Day 3]', fontsize=title_fontsize, fontweight='bold', loc='left')
    
    ax3.set_title('Start: '+ grb_3_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_3_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs3 = ax3.contourf(lons_3, lats_3, grb_3_vals, levels=np.arange(4, 10, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar3 = fig3.colorbar(cs3, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar3.set_ticks([])

    fig3.text(x1, y,'ISOLATED', fontsize=legend_fontsize, fontweight='bold')
    fig3.text(x2, y,'SCATTERED', fontsize=legend_fontsize, fontweight='bold')
    
    fig4 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig4.set_facecolor('aliceblue')
    fig4.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

    ax4 = fig4.add_subplot(1, 1, 1, projection=mapcrs)
    ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax4.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax4.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax4.set_title('SPC Dry Lightning Forecast [Day 4]', fontsize=title_fontsize, fontweight='bold', loc='left')
    
    ax4.set_title('Start: '+ grb_4_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_4_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs4 = ax4.contourf(lons_4, lats_4, grb_4_vals, levels=np.arange(4, 10, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar4 = fig4.colorbar(cs4, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar4.set_ticks([])

    fig4.text(x1, y,'ISOLATED', fontsize=legend_fontsize, fontweight='bold')
    fig4.text(x2, y,'SCATTERED', fontsize=legend_fontsize, fontweight='bold')

    fig5 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig5.set_facecolor('aliceblue')
    fig5.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

    fig5.suptitle('SPC Dry Lightning Forecast [Day 5]', fontsize=title_fontsize, fontweight='bold')
    
    ax5 = fig5.add_subplot(1, 1, 1, projection=mapcrs)
    ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax5.set_title('SPC Dry Lightning Forecast [Day 5]', fontsize=title_fontsize, fontweight='bold', loc='left')
    
    ax5.set_title('Start: '+ grb_5_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_5_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs5 = ax5.contourf(lons_5, lats_5, grb_5_vals, levels=np.arange(4, 10, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar5 = fig5.colorbar(cs5, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar5.set_ticks([])

    fig5.text(x1, y,'ISOLATED', fontsize=legend_fontsize, fontweight='bold')
    fig5.text(x2, y,'SCATTERED', fontsize=legend_fontsize, fontweight='bold')

    fig6 = plt.figure(figsize=(fig_x_length, fig_y_length))
    fig6.set_facecolor('aliceblue')
    fig6.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

    ax6 = fig6.add_subplot(1, 1, 1, projection=mapcrs)
    ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
    ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
    ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

    ax6.set_title('SPC Dry Lightning Forecast [Day 6]', fontsize=title_fontsize, fontweight='bold', loc='left')
    
    ax6.set_title('Start: '+ grb_6_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_6_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
        
    cs6 = ax6.contourf(lons_6, lats_6, grb_6_vals, levels=np.arange(4, 10, 2), cmap=cmap, transform=datacrs, zorder=2)

    cbar6 = fig6.colorbar(cs6, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
    cbar6.set_ticks([])

    fig6.text(x1, y,'ISOLATED', fontsize=legend_fontsize, fontweight='bold')
    fig6.text(x2, y,'SCATTERED', fontsize=legend_fontsize, fontweight='bold')

    if test_7 == True:

        fig7 = plt.figure(figsize=(fig_x_length, fig_y_length))
        fig7.set_facecolor('aliceblue')
        fig7.text(signature_x_position, signature_y_position, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nReference System: '+reference_system+'\nData Source: NOAA/NWS/SPC\nImage Created: ' + utc_time.strftime('%a %m/%d/%Y %H:%MZ'), fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=10)

        ax7 = fig7.add_subplot(1, 1, 1, projection=mapcrs)
        ax7.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax7.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax7.add_feature(cfeature.OCEAN, color='lightcyan', zorder=3)
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

        ax7.set_title('SPC Dry Lightning Forecast [Day 7]', fontsize=title_fontsize, fontweight='bold', loc='left')
        
        ax7.set_title('Start: '+ grb_7_start.strftime('%a %m/%d %H:00 Local') + '\nEnd: '+ grb_7_end.strftime('%a %m/%d %H:00 Local'), fontsize=subplot_title_fontsize, fontweight='bold', loc='right')
            
        cs7 = ax7.contourf(lons_7, lats_7, grb_7_vals, levels=np.arange(4, 10, 2), cmap=cmap, transform=datacrs, zorder=2)

        cbar7 = fig7.colorbar(cs7, location='bottom', shrink=color_table_shrink, pad=colorbar_pad)
        cbar7.set_ticks([])
    
        fig7.text(x1, y,'ISOLATED', fontsize=legend_fontsize, fontweight='bold')
        fig7.text(x2, y,'SCATTERED', fontsize=legend_fontsize, fontweight='bold')
    
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

    path, gif_path = file_functions.check_file_paths(state, gacc_region, 'SPC DRY LIGHTNING OUTLOOK', reference_system)
    file_functions.update_images(figs, path, gif_path, 'SPC DRY LIGHTNING OUTLOOK')
