# **Real Time Mesoscale Analysis Graphics**

### **Functions**

1) [plot_relative_humidity()](#plot_relative_humidity)
2) [plot_temperature()](#plot_temperature)
3) [plot_dew_point()](#plot_dew_point)
4) [plot_total_cloud_cover()](#plot_total_cloud_cover)
5) [plot_wind_speed()](#plot_wind_speed)
6) [plot_critical_firewx()](#plot_critical_firewx)
7) [plot_24_hour_relative_humidity_comparison()](#plot_24_hour_relative_humidity_comparison)
8) [plot_24_hour_temperature_comparison()](#plot_24_hour_temperature_comparison)
9) [plot_24_hour_dew_point_comparison()](#plot_24_hour_dew_point_comparison)
10) [plot_24_hour_wind_speed_comparison()](#plot_24_hour_wind_speed_comparison)
11) [plot_24_hour_total_cloud_cover_comparison()](#plot_24_hour_total_cloud_cover_comparison)

### plot_relative_humidity()

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

### plot_temperature()

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

### plot_dew_point()

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

### plot_total_cloud_cover()

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

### plot_wind_speed()

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

### plot_critical_firewx()

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

43) use_wind_gust (Boolean) - Default = False. If set to True, the critical fire weather forecast will use wind gust rather than sustained wind speed. If set to False, sustained
    wind speed will be used. 

44) add_temperature_parameter (Boolean) - Default = False. If set to True, temperature will also be a factor in determining the criteria for critical fire weather risk. 

45) low_rh_threshold (Integer) - Default = 15%. The threshold for what defines low relative humidity. 

46) high_wind_threshold (Integer) - Default = 25 MPH. The threshold for what defines high sustained winds and/or gusts. 

47) high_temperature_threshold (Integer) - Default = 75°F. The threshold for what defines the "hot" in "hot, dry and windy."
    
Return: Saves individual images to f:Weather Data/RTMA/RTMA Critical Fire Weather/{reference_system}. 
If the user selects a cwa the path will look like this: f:Weather Data/RTMA/RTMA Critical Fire Weather/{reference_system}/{cwa}

### plot_24_hour_relative_humidity_comparison()

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

### plot_24_hour_temperature_comparison()

This function plots the latest available 24-Hour RTMA Temperature Comparison. 

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

Return: Saves individual images to f:Weather Data/RTMA/24 HOUR RTMA TEMPERATURE COMPARISON {With or Without Contours}/{reference_system}. 
If the user selects a cwa the path will look like this: f:Weather Data/RTMA/24 HOUR RTMA TEMPERATURE COMPARISON {With or Without Contours}/{reference_system}/{cwa}

### plot_24_hour_dew_point_comparison()

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

### plot_24_hour_wind_speed_comparison()

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

### plot_24_hour_total_cloud_cover_comparison()

This function plots the latest available 24-Hour RTMA Total Cloud Cover Comparison. 

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

Return: Saves individual images to f:Weather Data/RTMA/24 HOUR RTMA TOTAL CLOUD COVER COMPARISON {With or Without Contours}/{reference_system}. 
If the user selects a cwa the path will look like this: f:Weather Data/RTMA/24 HOUR RTMA TOTAL CLOUD COVER COMPARISON COMPARISON {With or Without Contours}/{reference_system}/{cwa}






















