# **National Weather Service Forecast Graphics**

### **Classes**
1) [Relative Humidity](#relative-humidity-class) (`relative_humidity`)
2) [Temperature](#temperature-class) (`temperature`)

#### Relative Humidity Class

The `relative_humidity` class hosts 7 functions that plot the NWS Relative Humidity Forecasts:

1) [Poor Overnight Recovery Forecast](#poor-overnight-recovery-forecast) 

2) [Excellent Overnight Recovery Forecast](#excellent-overnight-recovery-forecast)

3) [Maximum Relative Humidity Forecast](#maximum-relative-humidity-forecast)

4) [Maximum Relative Humidity Trend Forecast](#maximum-relative-humidity-trend-forecast)

5) [Low Minimum Relative Humidity Forecast](#low-minimum-relative-humidity-forecast)

6) [Minimum Relative Humidity Forecast](#minimum-relative-humidity-forecast)

7) [Minimum Relative Humidity Trend Forecast](#minimum-relative-humidity-trend-forecast)

  ##### Poor Overnight Recovery Forecast

  <img width="628" alt="Screenshot 2024-08-03 150711" src="https://github.com/user-attachments/assets/72c217b5-9f9e-411b-9ca9-94835a6c5aa6">

  This function plots the latest available NOAA/NWS Poor Overnight Recovery RH Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L64)

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

  <img width="622" alt="Screenshot 2024-08-03 150951" src="https://github.com/user-attachments/assets/ccae6508-2322-4901-895f-a7980137a2cf">

This function plots the latest available NOAA/NWS Excellent Overnight Recovery RH Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L799)
    
Required Arguments: 
1) excellent_overnight_recovery_rh_threshold (Integer) - The relative humidity threshold for 
                       a poor overnight relative humidity recovery. This is the lower bound of values shaded. 
                       (i.e. a value of 80 means all values greater than 80% get shaded). 

2) contour_step (Integer) - The contour interval. (i.e. a value of 5 means the RH gets contoured every 5%). 

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

30) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

31) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

32) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

33) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

35) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
changed to None. 

36) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

Return: A list of figures for each forecast day.  

  ##### Maximum Relative Humidity Forecast

  <img width="629" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/87a4cf9b-7f6f-4bf7-9ccd-c559747c25c7">


This function plots the latest available NOAA/NWS Maximum RH Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L1504)

Required Arguments: 

1) contour_step (Integer) - The contour interval. (i.e. a value of 5 means the RH gets contoured every 5%). 

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

30) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

31) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

32) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

33) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

35) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
changed to None. 

36) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

Return: A list of figures for each forecast day. 

  ##### Maximum Relative Humidity Trend Forecast

  <img width="631" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/de35eba7-f474-4dab-90c2-03f1bc923332">


This function plots the latest available NOAA/NWS Maximum RH Trend Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L2203)

Required Arguments: 

1) contour_step (Integer) - The contour interval. (i.e. a value of 5 means the RH gets contoured every 5%). 

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

31) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

32) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

33) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

34) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

35) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
    or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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

Return: A list of figures for each forecast day.   

  ##### Low Minimum Relative Humidity Forecast

<img width="623" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/5be73151-2246-4caa-a20a-8cc56b5b7aee">


This function plots the latest available NOAA/NWS Low Minimum RH Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L2869)

Required Arguments: 

1) low_minimum_rh_threshold (Integer) - The relative humidity threshold for 
                       low minimum relative humidity. This is the upper bound of values shaded. 
                       (i.e. a value of 15 means all values less than 15% get shaded). 

2) contour_step (Integer) - The contour interval. (i.e. a value of 5 means the RH gets contoured every 5%). 

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

30) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

31) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

32) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

33) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

35) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
changed to None. 

36) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

Return: A list of figures for each forecast day. 

  ##### Minimum Relative Humidity Forecast

  <img width="626" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/9ebf4264-4ede-48b7-979a-76633f0dab45">


This function plots the latest available NOAA/NWS Minimum RH Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L3960)

Required Arguments: 

1) contour_step (Integer) - The contour interval. (i.e. a value of 5 means the RH gets contoured every 5%). 

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

31) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

32) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

33) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

35) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
Return: A list of figures for each forecast day. 

  ##### Minimum Relative Humidity Trend Forecast

<img width="627" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/98454272-efac-424d-a5e4-67db1ffdf494">


This function plots the latest available NOAA/NWS Minimum RH Trend Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L5030)

Required Arguments: 

1) contour_step (Integer) - The contour interval. (i.e. a value of 5 means the RH gets contoured every 5%). 

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

31) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

32) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

33) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

35) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
  Return: A list of figures for each forecast day. 

  #### Temperature Class

The `temperature` class hosts 7 functions that plot the NWS Relative Humidity Forecasts:

1) [Extreme Heat Forecast](#extreme-heat-forecast)

2) [Extremely Warm Low Temperature Forecast](#extremely-warm-low-temperature-forecast)

3) [Frost/Freeze Forecast](#frostfreeze-forecast) 

4) [Maximum Temperature Forecast](#maximum-temperature-forecast)

5) [Minimum Temperature Forecast](#minimum-temperature-forecast)

6) [Maximum Temperature Trend Forecast](#maximum-temperature-trend-forecast)

7) [Minimum Temperature Trend Forecast](#minimum-temperature-trend-forecast)

 ##### Extreme Heat Forecast

 <img width="629" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/a1c92f3c-0ca7-44eb-be93-9885cd915050">


This function plots the latest available NOAA/NWS Extreme Heat Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L5755)

Required Arguments: 

1) start_of_warm_season_month (Integer) - The numeric value for the month the warm season begins. 

2) end_of_warm_season_month (Integer) - The numeric value for the month the warm season ends. 

3) start_of_cool_season_month (Integer) - The numeric value for the month the cool season begins. 

4) end_of_cool_season_month (Integer) - The numeric value for the month the cool season ends.

5) temp_scale_warm_start (Integer) - The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

6) temp_scale_warm_stop (Integer) - The top bound temperature value in Fahrenheit of the warm season temperature range.

7) temp_scale_cool_start (Integer) - The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

8) temp_scale_cool_stop (Integer) - The top bound temperature value in Fahrenheit of the cool season temperature range. 

9) temp_scale_step (Integer) - The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                               (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

31) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

32) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

33) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

35) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
  Return: A list of figures for each forecast day. 

 ##### Extremely Warm Low Temperature Forecast

 <img width="629" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/7c735bf0-d767-407f-9f56-c158c0729113">


 This function plots the latest available NOAA/NWS Extremely Warm Low Temperature Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L6586)

Required Arguments: 

1) start_of_warm_season_month (Integer) - The numeric value for the month the warm season begins. 

2) end_of_warm_season_month (Integer) - The numeric value for the month the warm season ends. 

3) start_of_cool_season_month (Integer) - The numeric value for the month the cool season begins. 

4) end_of_cool_season_month (Integer) - The numeric value for the month the cool season ends.

5) temp_scale_warm_start (Integer) - The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

6) temp_scale_warm_stop (Integer) - The top bound temperature value in Fahrenheit of the warm season temperature range.

7) temp_scale_cool_start (Integer) - The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

8) temp_scale_cool_stop (Integer) - The top bound temperature value in Fahrenheit of the cool season temperature range. 

9) temp_scale_step (Integer) - The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                               (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

31) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

32) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

33) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

35) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
  Return: A list of figures for each forecast day. 

 ##### Frost/Freeze Forecast

 <img width="623" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/90ed6ba4-e10e-4498-9420-c8edd2e41aae">


This function plots the latest available NOAA/NWS Frost/Freeze Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L7417)

Required Arguments: 

1) temperature_bottom_bound (Integer) - The temperature value in Fahrenheit for the bottom bound of the temperature scale. 
                                        This value must be less than 32. 

2) temp_scale_step (Integer) - The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                               (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

31) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

32) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

33) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

35) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
  Return: A list of figures for each forecast day. 

 ##### Maximum Temperature Forecast

 <img width="632" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/338a98c7-a9f5-4103-8779-488422bb28ae">


This function plots the latest available NOAA/NWS Maximum Temperature Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L8163)

Required Arguments: 

1) start_of_warm_season_month (Integer) - The numeric value for the month the warm season begins. 

2) end_of_warm_season_month (Integer) - The numeric value for the month the warm season ends. 

3) start_of_cool_season_month (Integer) - The numeric value for the month the cool season begins. 

4) end_of_cool_season_month (Integer) - The numeric value for the month the cool season ends.

5) temp_scale_warm_start (Integer) - The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

6) temp_scale_warm_stop (Integer) - The top bound temperature value in Fahrenheit of the warm season temperature range.

7) temp_scale_cool_start (Integer) - The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

8) temp_scale_cool_stop (Integer) - The top bound temperature value in Fahrenheit of the cool season temperature range. 

9) temp_scale_step (Integer) - The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                               (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

31) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

32) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

33) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

35) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
  Return: A list of figures for each forecast day. 

 ##### Minimum Temperature Forecast

 <img width="632" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/039aa8f2-6ef4-4edf-917a-e8f6f6192c0e">


This function plots the latest available NOAA/NWS Minimum Temperature Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L8985)

Required Arguments: 

1) start_of_warm_season_month (Integer) - The numeric value for the month the warm season begins. 

2) end_of_warm_season_month (Integer) - The numeric value for the month the warm season ends. 

3) start_of_cool_season_month (Integer) - The numeric value for the month the cool season begins. 

4) end_of_cool_season_month (Integer) - The numeric value for the month the cool season ends.

5) temp_scale_warm_start (Integer) - The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

6) temp_scale_warm_stop (Integer) - The top bound temperature value in Fahrenheit of the warm season temperature range.

7) temp_scale_cool_start (Integer) - The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

8) temp_scale_cool_stop (Integer) - The top bound temperature value in Fahrenheit of the cool season temperature range. 

9) temp_scale_step (Integer) - The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                               (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

31) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

32) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

33) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

35) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
  Return: A list of figures for each forecast day. 

 ##### Maximum Temperature Trend Forecast

 <img width="633" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/26a7b292-9ef6-40c8-ab30-301316d6d6fa">


This function plots the latest available NOAA/NWS Maximum Temperature Trend Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L10493)

Required Arguments: 

1) contour_step (Integer) - The contour interval. (i.e. a value of 5 means the Temperature gets contoured every 5 degrees Fahrenheit). 

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

31) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

32) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

33) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

35) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
  Return: A list of figures for each forecast day. 

 ##### Minimum Temperature Trend Forecast

 <img width="629" alt="Screenshot 2024-08-03 151118" src="https://github.com/user-attachments/assets/30493cb7-05f5-406b-ad2c-1830441b2088">


This function plots the latest available NOAA/NWS Minimum Temperature Trend Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/NWS_Forecast_Graphics.py#L9805)

Required Arguments: 

1) contour_step (Integer) - The contour interval. (i.e. a value of 5 means the Temperature gets contoured every 5 degrees Fahrenheit). 

Optional Arguments: 

1) western_bound (Integer or Float) - Western extent of the plot in decimal degrees. 
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

26) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
sample points are displayed on the graphic. Default setting is True. If the user wants 
to hide the sample point values and only have the contour shading, this value will need 
to be changed to False. 

27) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
Default setting is a 10 point fontsize. 

28) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

29) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

31) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

32) data_array (String) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
This setting is only to be changed if the user wants to limit the amount of downloads from the 
NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
if the user wishes to download the data outside of this function. 

33) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

34) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

35) decimate (Integer) - This is the number of which the data is decimated by in order for the spacing of the 
sample points to appear in good order. Example: A value of 300 plots the sample point for one row
of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
Lower values equal more sample points which are less spaced apart. The default value is None. If
the default value is selected, the decimation is scaled automatically, however if the user wishes 
to change the spacing of the sample points, then the user must edit this value. 

36) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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
    
  Return: A list of figures for each forecast day. 
 
 
