# **National Weather Service Forecast Graphics**

### **Classes**
1) [Relative Humidity](#relative-humidity-class) (`nws_relative_humidity_forecast`)
2) [Temperature](#temperature-class) (`nws_temperature_forecast`)
3) Dry and Windy

#### Relative Humidity Class

The `nws_relative_humidity_forecast` class hosts 7 functions that plot the NWS Relative Humidity Forecasts:

1) [Poor Overnight Recovery Forecast](#poor-overnight-recovery-forecast) 

2) [Excellent Overnight Recovery Forecast](#excellent-overnight-recovery-forecast)

3) [Maximum Relative Humidity Forecast](#maximum-relative-humidity-forecast)

4) [Maximum Relative Humidity Trend Forecast](#maximum-relative-humidity-trend-forecast)

5) [Low Minimum Relative Humidity Forecast](#low-minimum-relative-humidity-forecast)

6) [Minimum Relative Humidity Forecast](#minimum-relative-humidity-forecast)

7) [Minimum Relative Humidity Trend Forecast](#minimum-relative-humidity-trend-forecast)

  ##### Poor Overnight Recovery Forecast

  This function plots the latest available NOAA/NWS Poor Overnight Recovery RH Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L64)

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

44) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

46) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

47) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

48) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

49) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

50) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

51) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

52) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

54) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

55) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

  Return: Saves individual images to a folder and creates a GIF from those images.

  ##### Excellent Overnight Recovery Forecast

This function plots the latest available NOAA/NWS Excellent Overnight Recovery RH Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L799)
    
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

44) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

46) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

47) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

48) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

49) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

50) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

51) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

52) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

54) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

55) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

  Return: Saves individual images to a folder and creates a GIF from those images.

  ##### Maximum Relative Humidity Forecast

This function plots the latest available NOAA/NWS Maximum RH Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L1504)

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

45) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

46) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

47) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

48) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

49) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

50) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

51) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

53) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

54) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

  ##### Maximum Relative Humidity Trend Forecast


This function plots the latest available NOAA/NWS Maximum RH Trend Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L2203)

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

45) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

46) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

47) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

48) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

49) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

50) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

51) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

53) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

54) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

  ##### Low Minimum Relative Humidity Forecast

This function plots the latest available NOAA/NWS Low Minimum RH Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L2869)

Required Arguments: None

Optional Arguments: 

1) low_minimum_rh_threshold (Integer) -  Default = 15%. The relative humidity threshold for 
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

44) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

45) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

46) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

47) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

48) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

49) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

50) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

51) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

52) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

53) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 
  
Return: Saves individual images to a folder and creates a GIF from those images. 
  ##### Minimum Relative Humidity Forecast

This function plots the latest available NOAA/NWS Minimum RH Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L3960)

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

45) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

46) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

47) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

48) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

49) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

50) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

51) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

53) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

54) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

  ##### Minimum Relative Humidity Trend Forecast

This function plots the latest available NOAA/NWS Minimum RH Trend Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L5030)

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

45) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

46) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

47) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

48) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

49) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

50) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

51) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

53) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

54) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

  #### Temperature Class

The `nws_temperature_forecast` class hosts 7 functions that plot the NWS Relative Humidity Forecasts:

1) [Extreme Heat Forecast](#extreme-heat-forecast)

2) [Extremely Warm Low Temperature Forecast](#extremely-warm-low-temperature-forecast)

3) [Frost/Freeze Forecast](#frostfreeze-forecast) 

4) [Maximum Temperature Forecast](#maximum-temperature-forecast)

5) [Minimum Temperature Forecast](#minimum-temperature-forecast)

6) [Maximum Temperature Trend Forecast](#maximum-temperature-trend-forecast)

7) [Minimum Temperature Trend Forecast](#minimum-temperature-trend-forecast)

 ##### Extreme Heat Forecast

This function plots the latest available NOAA/NWS Extreme Heat Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L5755)

Required Arguments: None

Optional Arguments: 

1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

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
                       

26) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

27) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

28) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

29) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

30) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

31) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

32) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

33) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

34) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

35) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

36) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

37) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
    To change to a dashed line, users should set state_border_linestyle='--'. 

38) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
    To change to a dashed line, users should set county_border_linestyle='--'. 

39) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
    To change to a dashed line, users should set gacc_border_linestyle='--'. 

40) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

41) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

42) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

43) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

44) psa_color (String) - Default = 'black'. Color of the PSA borders.

45) gacc_color (String) - Default = 'black'. Color of the GACC borders.

46) cwa_color (String) - Default = 'black'. Color of the CWA borders.

47) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

48) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

49) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

50) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

51) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 

52) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

54) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

55) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

56) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

57) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

58) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

59) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

60) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

62) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

63) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

 ##### Extremely Warm Low Temperature Forecast

 This function plots the latest available NOAA/NWS Extremely Warm Low Temperature Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L6586)

Required Arguments: None

Optional Arguments: 

1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

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

26) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

27) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

28) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

29) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

30) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

31) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

32) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

33) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

34) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

35) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

36) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

37) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
    To change to a dashed line, users should set state_border_linestyle='--'. 

38) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
    To change to a dashed line, users should set county_border_linestyle='--'. 

39) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
    To change to a dashed line, users should set gacc_border_linestyle='--'. 

40) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

41) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

42) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

43) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

44) psa_color (String) - Default = 'black'. Color of the PSA borders.

45) gacc_color (String) - Default = 'black'. Color of the GACC borders.

46) cwa_color (String) - Default = 'black'. Color of the CWA borders.

47) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

48) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

49) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

50) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

51) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 

52) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

54) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

55) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

56) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

57) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

58) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

59) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

60) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

62) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

63) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 


 ##### Frost/Freeze Forecast

This function plots the latest available NOAA/NWS Frost/Freeze Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L7417)

Required Arguments: None

Optional Arguments: 

1) temperature_bottom_bound (Integer) - Default = -10. The temperature value in Fahrenheit for the bottom bound of the temperature scale. 
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

44) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

 ##### Maximum Temperature Forecast

This function plots the latest available NOAA/NWS Maximum Temperature Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L8163)

Required Arguments: None

Optional Arguments: 

1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

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


 ##### Minimum Temperature Forecast

This function plots the latest available NOAA/NWS Minimum Temperature Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L8985)

Required Arguments: None

Optional Arguments: 

1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

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


 ##### Maximum Temperature Trend Forecast

This function plots the latest available NOAA/NWS Maximum Temperature Trend Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L10493)

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

45) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

46) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

47) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

48) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

49) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

50) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

51) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

53) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

54) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

 ##### Minimum Temperature Trend Forecast

This function plots the latest available NOAA/NWS Minimum Temperature Trend Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/firewxpy/NWS_Forecast_Graphics.py#L9805)

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

45) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

46) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

47) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

48) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

49) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

50) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

51) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

53) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

54) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

#### Dry And Windy Class

The `dry_and_windy` 

