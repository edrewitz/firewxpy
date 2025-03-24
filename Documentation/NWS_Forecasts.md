# **National Weather Service Forecast Graphics**

**Relative Humidity Class**

*Functions*

1) [plot_poor_overnight_recovery_relative_humidity_forecast()](#plot_poor_overnight_recovery_relative_humidity_forecast)
2) [plot_excellent_overnight_recovery_relative_humidity_forecast()](#plot_excellent_overnight_recovery_relative_humidity_forecast)
3) [plot_low_minimum_relative_humidity_forecast()](#plot_low_minimum_relative_humidity_forecast)
4) [plot_minimum_relative_humidity_forecast()](#plot_minimum_relative_humidity_forecast)
5) [plot_maximum_relative_humidity_forecast()](#plot_maximum_relative_humidity_forecast)
6) [plot_maximum_relative_humidity_forecast_trend()](#plot_maximum_relative_humidity_forecast_trend)
7) [plot_minimum_relative_humidity_forecast_trend()](#plot_minimum_relative_humidity_forecast_trend)

**Temperature Class**

*Functions*

1) [plot_frost_freeze_forecast()](#plot_frost_freeze_forecast)
2) [plot_extremely_warm_low_temperature_forecast()](#plot_extremely_warm_low_temperature_forecast)
3) [plot_extreme_heat_forecast()](#plot_extreme_heat_forecast)
4) [plot_maximum_temperature_forecast()](#plot_maximum_temperature_forecast)
5) [plot_minimum_temperature_forecast()](#plot_minimum_temperature_forecast)
6) [plot_minimum_temperature_forecast_trend()](#plot_minimum_temperature_forecast_trend)
7) [plot_maximum_temperature_forecast_trend()](#plot_maximum_temperature_forecast_trend)

**Critical Fire Weather Class**

*Functions*

[plot_critical_firewx_forecast()](#plot_critical_firewx_forecast)

### plot_poor_overnight_recovery_relative_humidity_forecast()

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


### plot_excellent_overnight_recovery_relative_humidity_forecast()

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

### plot_low_minimum_relative_humidity_forecast()

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

### plot_minimum_relative_humidity_forecast()

This function plots the latest available NOAA/NWS Minimum RH Forecast. 

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

### plot_maximum_relative_humidity_forecast()

This function plots the latest available NOAA/NWS Maximum RH Forecast. 

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

### plot_maximum_relative_humidity_forecast_trend()

This function plots the latest available NOAA/NWS Maximum Relative Humidity Forecast Trend. 

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

41) show_contours (Boolean) - Default = True. If set to False, contours will be hidden. 

Return: Saves individual images to f:Weather Data/NWS Forecasts/Maximum Relative Humidity Trend/{reference_system}. 
If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Maximum Relative Humidity Trend/{reference_system}/{cwa}

### plot_minimum_relative_humidity_forecast_trend()

This function plots the latest available NOAA/NWS Minimum Relative Humidity Forecast Trend. 

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

41) show_contours (Boolean) - Default = True. If set to False, contours will be hidden. 

Return: Saves individual images to f:Weather Data/NWS Forecasts/Minimum Relative Humidity Trend/{reference_system}. 
If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Minimum Relative Humidity Trend/{reference_system}/{cwa}

### plot_frost_freeze_forecast()

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

### plot_extremely_warm_low_temperature_forecast()

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

### plot_extreme_heat_forecast()

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

### plot_maximum_temperature_forecast()

This function plots the latest available NOAA/NWS Maximum Temperature Forecast. 

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

Return: Saves individual images to f:Weather Data/NWS Forecasts/Max T Forecast/{reference_system}. 
If the user selects a cwa the path will look like this: f:Weather Data/NWS Forecasts/Max T Forecast/{reference_system}/{cwa}

### plot_minimum_temperature_forecast()

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

### plot_minimum_temperature_forecast_trend()

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

### plot_maximum_temperature_forecast_trend()

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

### plot_critical_firewx_forecast()

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
