# **Forecast Model Graphics**

### **Classes**
1) [dynamics]()
2) [temperature]()
3) [relative_humidity]()
4) [critical_firewx_conditions]()

#### Dynamics Class

1) [Geopotential Height/Vorticity/Wind]()
2) [Geopotential Height]()
3) [24-Hour Geopotential Height Change]()
4) [Geopotential Height/Wind]()
5) [10-Meter Winds/MSLP]()


##### Geopotential Height/Vorticity/Wind

This function plots the Geopotential Height/Vorticity/Wind Forecast for a specific level. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p25_1h - GFS 0.25x0.25 degree with 1 hour intervals
   3) GFS0p50 - GFS 0.5x0.5 degree
   4) GFS1p00 - GFS 1.0x1.0 degree
   5) GEFS0p50_all - All ensemble members of the GEFS 0.5x0.5 degree
   6) CMCENS - Canadian Ensemble
   7) NAM - North American Model
   8) NAM 1hr - North American Model with 1 hour intervals 

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
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


##### Geopotential Height

This function plots the Geopotential Height Forecast for a specific level. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p25_1h - GFS 0.25x0.25 degree with 1 hour intervals
   3) GFS0p50 - GFS 0.5x0.5 degree
   4) GFS1p00 - GFS 1.0x1.0 degree
   5) GEFS0p50_all - All ensemble members of the GEFS 0.5x0.5 degree
   6) CMCENS - Canadian Ensemble
   7) NAM - North American Model
   8) NAM 1hr - North American Model with 1 hour intervals 

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
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


##### 24-Hour Geopotential Height Change

This function plots the 24-Hour Gepotential Height Change Forecast for a specific level. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p25_1h - GFS 0.25x0.25 degree with 1 hour intervals
   3) GFS0p50 - GFS 0.5x0.5 degree
   4) GFS1p00 - GFS 1.0x1.0 degree
   5) GEFS0p50_all - All ensemble members of the GEFS 0.5x0.5 degree
   6) CMCENS - Canadian Ensemble
   7) NAM - North American Model
   8) NAM 1hr - North American Model with 1 hour intervals 

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
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


##### Geopotential Height/Wind

This function plots the Geopotential Height/Wind Forecast for a specific level. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p25_1h - GFS 0.25x0.25 degree with 1 hour intervals
   3) GFS0p50 - GFS 0.5x0.5 degree
   4) GFS1p00 - GFS 1.0x1.0 degree
   5) GEFS0p50_all - All ensemble members of the GEFS 0.5x0.5 degree
   6) CMCENS - Canadian Ensemble
   7) NAM - North American Model
   8) NAM 1hr - North American Model with 1 hour intervals 

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

Optional Arguments: 1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
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


##### 10-Meter Winds/MSLP

This function plots the 10-Meter Wind/MSLP Forecast. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GFS0p25 - GFS 0.25x0.25 degree
   2) GFS0p25_1h - GFS 0.25x0.25 degree with 1 hour intervals
   3) GFS0p50 - GFS 0.5x0.5 degree
   4) GFS1p00 - GFS 1.0x1.0 degree
   5) GEFS0p50_all - All ensemble members of the GEFS 0.5x0.5 degree
   6) CMCENS - Canadian Ensemble
   7) NAM - North American Model
   8) NAM 1hr - North American Model with 1 hour intervals 

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                   To look at any state use the 2-letter abbreviation for the state in either all capitals
                   or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                   CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                   North America use either: NA, na, North America or north america. If the user wishes to use custom
                   boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                   the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                   'oscc' for South Ops. 

Optional Arguments: 1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
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

8) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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


