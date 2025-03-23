# **Forecast Model Graphics**

### **Classes**
1) [dynamics](#dynamics-class)
2) [temperature](#temperature-class)
3) [relative_humidity](#relative-humidity-class)
4) [critical_firewx_conditions](#critical-firewx-conditions-class)
5) [precipitation](#precipitation-class)

#### Dynamics Class

1) [Geopotential Height/Vorticity/Wind](#geopotential-heightvorticitywind)
2) [Geopotential Height](#geopotential-height)
3) [24-Hour Geopotential Height Change](#24-hour-geopotential-height-change)
4) [Geopotential Height/Wind](#geopotential-heightwind)
5) [10-Meter Winds/MSLP](#10-meter-windsmslp)


##### Geopotential Height/Vorticity/Wind

This function plots the Geopotential Height/Vorticity/Wind Forecast for a specific level. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 

1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                     500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 

3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. 

4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
    Default setting is True. Users should change this value to False if they wish to hide rivers.

9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 

Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

##### Geopotential Height

This function plots the Geopotential Height Forecast for a specific level. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 

1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                     500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 

3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. 

4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
    Default setting is True. Users should change this value to False if they wish to hide rivers.

9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

##### 24-Hour Geopotential Height Change

This function plots the 24-Hour Gepotential Height Change Forecast for a specific level. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America
   
2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 

1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                     500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 

3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. 

4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
    Default setting is True. Users should change this value to False if they wish to hide rivers.

9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 

Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level


##### Geopotential Height/Wind

This function plots the Geopotential Height/Wind Forecast for a specific level. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                 To look at any state use the 2-letter abbreviation for the state in either all capitals
                 or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                 CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                 North America use either: NA, na, North America or north america. If the user wishes to use custom
                 boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                 the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                 'oscc' for South Ops. 

Optional Arguments: 

1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                     500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 

3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. 

4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
    Default setting is True. Users should change this value to False if they wish to hide rivers.

9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 

Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

##### 10-Meter Winds/MSLP

This function plots the 10-Meter Wind/MSLP Forecast. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America
   8) RAP - Rapid Refresh Model
   9) RAP 32 - 32km Rapid Refresh Model - Full North America

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 

1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 

2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. 

3) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


4) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


5) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

6) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

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

16) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

17) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

18) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

19) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

20) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

21) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

22) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

23) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

24) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
    To change to a dashed line, users should set state_border_linestyle='--'. 

25) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
    To change to a dashed line, users should set county_border_linestyle='--'. 

26) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
    To change to a dashed line, users should set gacc_border_linestyle='--'. 

27) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

28) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

29) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

30) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'.    

31) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

32) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

33) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

34) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

35) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

36) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

37) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

38) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

39) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

40) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

41) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

42) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

43) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 

Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level


#### Temperature Class

1) [2-Meter Temperature](#2-meter-temperature)
2) [Freezing Level](#freezing-level)
3) [Height Temperature Wind](#height-temperature-wind)


##### 2-Meter Temperature

This function plots the 2-Meter Temperature Forecast. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America
   8) RAP - Rapid Refresh Model
   9) RAP 32 - 32km Rapid Refresh Model - Full North America
   10) GEFS0p25 ENS MEAN - GEFS 0.25x0.25 degree Ensemble Mean

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                 To look at any state use the 2-letter abbreviation for the state in either all capitals
                 or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                 CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                 North America use either: NA, na, North America or north america. If the user wishes to use custom
                 boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                 the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                 'oscc' for South Ops. 

Optional Arguments: 

1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

2) end_of_warm_season_month (Integer) - Default = 10 (October). The numeric value for the month the warm season ends. 

3) start_of_cool_season_month (Integer) - Default = 11 (November). The numeric value for the month the cool season begins. 

4) end_of_cool_season_month (Integer) - Default = 3 (March). The numeric value for the month the cool season ends.

5) temp_scale_warm_start (Integer) - Default = 10. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

6) temp_scale_warm_stop (Integer) - Default = 110. The top bound temperature value in Fahrenheit of the warm season temperature range.

7) temp_scale_cool_start (Integer) - Default = -20. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

8) temp_scale_cool_stop (Integer) - Default = 80. The top bound temperature value in Fahrenheit of the cool season temperature range. 

9) temp_scale_step (Integer) - Default = 1. The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                               (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

10) temperature_contour_value (Integer) - Default = 32. This draws a contour line seperating two groups of temperature values. 
                                          Default is the boundary between below and above freezing temperatures.

11) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 

12) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

13) ds_list (List) - Default = None. This is the list of datasets the user passes in if the user downloads the data outside of the function
                    and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                    needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

14) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


15) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


16) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

17) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

18) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
    Default setting is True. Users should change this value to False if they wish to hide rivers.

19) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                       

20) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

21) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

22) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

23) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

24) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

25) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

26) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

27) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

28) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

29) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

30) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

31) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

32) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

33) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

34) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

35) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
    To change to a dashed line, users should set state_border_linestyle='--'. 

36) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
    To change to a dashed line, users should set county_border_linestyle='--'. 

37) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
    To change to a dashed line, users should set gacc_border_linestyle='--'. 

38) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

39) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

40) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

41) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'.    

42) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

43) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

44) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

45) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

46) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

47) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

48) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

49) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

50) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

51) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

52) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

53) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

54) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 

Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

#### Freezing Level 

This function plots the Freezing Level Forecast. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America
   8) RAP - Rapid Refresh Model
   9) RAP 32 - 32km Rapid Refresh Model - Full North America

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 

1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 

2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

3) ds_list (List) - Default = None. This is the list of datasets the user passes in if the user downloads the data outside of the function
                    and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                    needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

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

17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 

Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/FREEZING LEVEL

#### Height Temperature Wind

This function plots the Geopotential Height/Temperature/Wind Forecast for a specific level. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America
   8) RAP - Rapid Refresh Model
   9) RAP 32 - 32km Rapid Refresh Model - Full North America

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 

1) level (Integer) - Default = 850. This is the level in millibars or hectopascals at which the user wishes to examine. 
                     850 means 850mb or 850hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 

3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. 

4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
    Default setting is True. Users should change this value to False if they wish to hide rivers.

9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

#### Relative Humidity Class

1) [2-Meter Relative Humidity](#2-meter-relative-humidity)
2) [Height RH Wind](#height-rh-wind)

##### 2-Meter Relative Humidity

This function plots the 2-Meter Relative Humidity Forecast. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America
   8) RAP - Rapid Refresh Model
   9) RAP 32 - 32km Rapid Refresh Model - Full North America
   10) GEFS0p25 ENS MEAN - GEFS 0.25x0.25 degree Ensemble Mean

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 

1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 

2) low_rh_threshold (Integer) - Default = 15. The threshold for the contour line that defines what extremely low relative humidity is. 

3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

4) ds_list (List) - Default = None. This is the list of datasets the user passes in if the user downloads the data outside of the function
                    and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                    needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

5) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


6) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


7) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

8) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

9) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
    Default setting is True. Users should change this value to False if they wish to hide rivers.

10) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                       

11) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

12) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

13) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

14) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

15) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

16) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

17) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

18) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

19) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

20) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

21) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

22) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

23) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

24) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

25) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

26) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
    To change to a dashed line, users should set state_border_linestyle='--'. 

27) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
    To change to a dashed line, users should set county_border_linestyle='--'. 

28) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
    To change to a dashed line, users should set gacc_border_linestyle='--'. 

29) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

30) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

31) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

32) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'.    

33) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

34) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

35) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

36) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

37) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

38) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

39) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

40) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

41) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

42) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

43) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

44) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

45) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 

Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

##### Height RH Wind

This function plots the Geopotential Height/Relative Humidity/Wind Forecast for a specific level. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America
   8) RAP - Rapid Refresh Model
   9) RAP 32 - 32km Rapid Refresh Model - Full North America

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 

1) level (Integer) - Default = 700. This is the level in millibars or hectopascals at which the user wishes to examine. 
                     700 means 700mb or 700hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 

3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. 

4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
    Default setting is True. Users should change this value to False if they wish to hide rivers.

9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level



#### Critical FireWx Conditions Class

[Favorable FireWx Conditions](#favorable-firewx-conditions)


##### Favorable FireWx Conditions

This function plots the Favorable Fire Weather Forecast. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America
   8) RAP - Rapid Refresh Model
   9) RAP 32 - 32km Rapid Refresh Model - Full North America
   10) GEFS0p25 ENS MEAN - GEFS 0.25x0.25 degree Ensemble Mean

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 

1) low_rh_threshold (Integer) - Default = 15. The threshold for the contour line that defines what extremely low relative humidity is.

2) high_wind_threshold (Integer) - Default = 25. The threshold for the contour line that defines what high winds are.

3) use_wind_gust (Boolean) - Default = False. When set to False, the red shading is determined by the intersection of either the 
                            RH & Sustained Wind Speed or RH & Temperature & Sustained Wind Speed. When set to True, the red shading
                            is determined by the intersection of RH & Wind Gust or RH & Temperature & Wind Gust. 

4) temperature_threshold (Integer) - Default = None. This is to be used if the user wishes to add temperature as a factor to what 
                                     defines favorable fire weather conditions. When set to None, only RH & Wind Speed/Gust are taken 
                                     into account. When set to an integer value, the temperature will also be taken into account. 

5) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 

 

3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

4) ds_list (List) - Default = None. This is the list of datasets the user passes in if the user downloads the data outside of the function
                    and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                    needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

5) u (List) - Default = None. This is the list of u-wind datasets the user passes in if the user downloads the data outside of the function
                    and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                    needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

6) v (List) - Default = None. This is the list of v-wind datasets the user passes in if the user downloads the data outside of the function
                    and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                    needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

7) gusts (List) - Default = None. This is the list of wind gust datasets the user passes in if the user downloads the data outside of the function
                    and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                    needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

8) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


9) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


10) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

11) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

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

21) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

22) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

23) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

24) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

25) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

26) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

27) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

28) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

36) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

37) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

38) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

39) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

40) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

41) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

42) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

43) decimate (Integer) - Default = 20. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

44) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

45) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

46) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

47) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

48) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 

Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level



#### Precipitation Class 

1) [Precipitation Rate](#precipitation-rate)

##### Precipitation Rate

This function plots the Precipitation Rate Forecast. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p50 - GFS 0.5x0.5 degree
   3) GFS1p00 - GFS 1.0x1.0 degree
   4) GEFS0p50 - GEFS 0.5x0.5 degree
   5) CMCENS - Canadian Ensemble
   6) NAM - North American Model
   7) NA NAM - 32km North American Model - Full North America
   8) RAP - Rapid Refresh Model
   9) RAP 32 - 32km Rapid Refresh Model - Full North America

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 

1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                    and passing the data in or if the function needs to download the data. A value of False means the data
                    is downloaded inside of the function while a value of True means the user is downloading the data outside
                    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                    things, it is recommended to set this value to True and download the data outside of the function and pass
                    it in so that the amount of data requests on the host servers can be minimized. 


2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 
                

3) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


4) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


5) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

6) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

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

16) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

17) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

18) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

19) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

20) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

21) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

22) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

23) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

24) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
    To change to a dashed line, users should set state_border_linestyle='--'. 

25) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
    To change to a dashed line, users should set county_border_linestyle='--'. 

26) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
    To change to a dashed line, users should set gacc_border_linestyle='--'. 

27) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

28) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

29) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'. 

30) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
    To change to a dashed line, users should set psa_border_linestyle='--'.    

31) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

32) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

33) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

34) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

35) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

36) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

37) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                  This is a feature of matplotlib, as per their definition, the shrink is:
                                  "Fraction by which to multiply the size of the colorbar." 
                                  This should only be changed if the user wishes to make a custom plot. 
                                  Preset values are called from the settings module for each region. 

38) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                         Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                         when making a custom plot. 

39) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

40) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

41) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

42) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

43) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 

Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

