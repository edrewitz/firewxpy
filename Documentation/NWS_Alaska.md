# **National Weather Service Forecast Graphics Alaska**

### **Classes**
1) [Relative Humidity](#relative-humidity-class) (`nws_relative_humidity_forecast_alaska`)
2) [Temperature](#temperature-class) (`nws_temperature_forecast_alaska`)
3) [Hot Dry and Windy](hot-dry-and-windy-class) (nws_hot_dry_and_windy_alaska)

#### Relative Humidity Class

The `nws_relative_humidity_forecast_alaska` class hosts 7 functions that plot the NWS Relative Humidity Forecasts for Alaska:

1) [Poor Overnight Recovery Forecast](#poor-overnight-recovery-forecast) 

2) [Excellent Overnight Recovery Forecast](#excellent-overnight-recovery-forecast)

3) [Maximum Relative Humidity Forecast](#maximum-relative-humidity-forecast)

4) [Maximum Relative Humidity Trend Forecast](#maximum-relative-humidity-trend-forecast)

5) [Low Minimum Relative Humidity Forecast](#low-minimum-relative-humidity-forecast)

6) [Minimum Relative Humidity Forecast](#minimum-relative-humidity-forecast)

7) [Minimum Relative Humidity Trend Forecast](#minimum-relative-humidity-trend-forecast)

  ##### Poor Overnight Recovery Forecast

This function plots the latest available NOAA/NWS Minimum RH Forecast. 

Required Arguments: None

Optional Arguments: 

1) poor_overnight_recovery_rh_threshold (Integer) -  Default = 50%. The relative humidity threshold for 
   a poor overnight relative humidity recovery. This is the upper bound of values shaded. 
   (i.e. a value of 50 means all values less than 50% get shaded).

2) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
   This is a feature of matplotlib, as per their definition, the shrink is:
   "Fraction by which to multiply the size of the colorbar." 
   This should only be changed if the user wishes to change the size of the colorbar. 
   Preset values are called from the settings module for each state and/or gacc_region.
    
3) title_fontsize (Integer) - Fontsize of the plot title. 
    Default setting is 12 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region. 

4) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.  

5) signature_fontsize (Integer) - The fontsize of the signature. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

6) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
    Default setting is 8 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

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

28) psa_color (String) - Default = 'black'. Color of the PSA borders.

29) gacc_color (String) - Default = 'black'. Color of the GACC borders.

30) cwa_color (String) - Default = 'black'. Color of the CWA borders.

31) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

32) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

33) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

34) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

35) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 


36) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

37) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

38) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

39) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

40) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

41) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

42) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

43) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                   AER or aer: WFO Anchorage Eastern Domain
                   ALU or alu: WFO Anchorage Western Domain
                   AJK or ajk: WFO Juneau
                   AFG or afg: WFO Fairbanks
                   
44) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

45) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

  ##### Excellent Overnight Recovery Forecast

This function plots the latest available NOAA/NWS Minimum RH Forecast. 

Required Arguments: None

Optional Arguments: 

1) excellent_overnight_recovery_rh_threshold (Integer) -  Default = 80%. The relative humidity threshold for 
   a poor overnight relative humidity recovery. This is the upper bound of values shaded. 
   (i.e. a value of 80 means all values greater than 80% get shaded).

2) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
   This is a feature of matplotlib, as per their definition, the shrink is:
   "Fraction by which to multiply the size of the colorbar." 
   This should only be changed if the user wishes to change the size of the colorbar. 
   Preset values are called from the settings module for each state and/or gacc_region.
    
3) title_fontsize (Integer) - Fontsize of the plot title. 
    Default setting is 12 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region. 

4) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.  

5) signature_fontsize (Integer) - The fontsize of the signature. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

6) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
    Default setting is 8 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

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

28) psa_color (String) - Default = 'black'. Color of the PSA borders.

29) gacc_color (String) - Default = 'black'. Color of the GACC borders.

30) cwa_color (String) - Default = 'black'. Color of the CWA borders.

31) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

32) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

33) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

34) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

35) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 


36) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

37) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

38) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

39) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

40) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

41) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

42) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

43) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                   AER or aer: WFO Anchorage Eastern Domain
                   ALU or alu: WFO Anchorage Western Domain
                   AJK or ajk: WFO Juneau
                   AFG or afg: WFO Fairbanks
                   
44) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

45) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images.   

  ##### Maximum Relative Humidity Forecast

This function plots the latest available NOAA/NWS Maximum RH Forecast. 

Required Arguments: None

Optional Arguments: 

1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
   This is a feature of matplotlib, as per their definition, the shrink is:
   "Fraction by which to multiply the size of the colorbar." 
   This should only be changed if the user wishes to change the size of the colorbar. 
   Preset values are called from the settings module for each state and/or gacc_region.
    
2) title_fontsize (Integer) - Fontsize of the plot title. 
    Default setting is 12 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region. 

3) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.  

4) signature_fontsize (Integer) - The fontsize of the signature. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

5) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
    Default setting is 8 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

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

27) psa_color (String) - Default = 'black'. Color of the PSA borders.

28) gacc_color (String) - Default = 'black'. Color of the GACC borders.

29) cwa_color (String) - Default = 'black'. Color of the CWA borders.

30) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

31) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

32) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

33) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

34) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 


35) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

36) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

37) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

38) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

39) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

40) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

41) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

42) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                   AER or aer: WFO Anchorage Eastern Domain
                   ALU or alu: WFO Anchorage Western Domain
                   AJK or ajk: WFO Juneau
                   AFG or afg: WFO Fairbanks
                   
43) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

44) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images.   

  ##### Maximum Relative Humidity Trend Forecast

This function plots the latest available NOAA/NWS Maximum RH Forecast. 

Required Arguments: None

Optional Arguments: 

1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
   This is a feature of matplotlib, as per their definition, the shrink is:
   "Fraction by which to multiply the size of the colorbar." 
   This should only be changed if the user wishes to change the size of the colorbar. 
   Preset values are called from the settings module for each state and/or gacc_region.
    
2) title_fontsize (Integer) - Fontsize of the plot title. 
    Default setting is 12 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region. 

3) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.  

4) signature_fontsize (Integer) - The fontsize of the signature. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

5) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
    Default setting is 8 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

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

27) psa_color (String) - Default = 'black'. Color of the PSA borders.

28) gacc_color (String) - Default = 'black'. Color of the GACC borders.

29) cwa_color (String) - Default = 'black'. Color of the CWA borders.

30) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

31) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

32) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

33) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

34) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 


35) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

36) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

37) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

38) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

39) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

40) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

41) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

42) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                   AER or aer: WFO Anchorage Eastern Domain
                   ALU or alu: WFO Anchorage Western Domain
                   AJK or ajk: WFO Juneau
                   AFG or afg: WFO Fairbanks
                   
43) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

44) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

  ##### Low Minimum Relative Humidity Forecast

This function plots the latest available NOAA/NWS Minimum RH Forecast. 

Required Arguments: None

Optional Arguments: 

1) low_minimum_rh_threshold (Integer) -  Default = 25%. The relative humidity threshold for 
   a low minimum relative humidity. This is the upper bound of values shaded. 
   (i.e. a value of 25 means all values less than 25% get shaded).

2) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
   This is a feature of matplotlib, as per their definition, the shrink is:
   "Fraction by which to multiply the size of the colorbar." 
   This should only be changed if the user wishes to change the size of the colorbar. 
   Preset values are called from the settings module for each state and/or gacc_region.
    
3) title_fontsize (Integer) - Fontsize of the plot title. 
    Default setting is 12 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region. 

4) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.  

5) signature_fontsize (Integer) - The fontsize of the signature. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

6) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
    Default setting is 8 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

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

28) psa_color (String) - Default = 'black'. Color of the PSA borders.

29) gacc_color (String) - Default = 'black'. Color of the GACC borders.

30) cwa_color (String) - Default = 'black'. Color of the CWA borders.

31) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

32) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

33) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

34) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

35) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 


36) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

37) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

38) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

39) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

40) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

41) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

42) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

43) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                   AER or aer: WFO Anchorage Eastern Domain
                   ALU or alu: WFO Anchorage Western Domain
                   AJK or ajk: WFO Juneau
                   AFG or afg: WFO Fairbanks
                   
44) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

45) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

  ##### Minimum Relative Humidity Forecast

This function plots the latest available NOAA/NWS Minimum RH Forecast. 

Required Arguments: None

Optional Arguments: 

1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
   This is a feature of matplotlib, as per their definition, the shrink is:
   "Fraction by which to multiply the size of the colorbar." 
   This should only be changed if the user wishes to change the size of the colorbar. 
   Preset values are called from the settings module for each state and/or gacc_region.
    
2) title_fontsize (Integer) - Fontsize of the plot title. 
    Default setting is 12 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region. 

3) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.  

4) signature_fontsize (Integer) - The fontsize of the signature. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

5) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
    Default setting is 8 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

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

27) psa_color (String) - Default = 'black'. Color of the PSA borders.

28) gacc_color (String) - Default = 'black'. Color of the GACC borders.

29) cwa_color (String) - Default = 'black'. Color of the CWA borders.

30) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

31) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

32) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

33) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

34) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 


35) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

36) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

37) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

38) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

39) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

40) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

41) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

42) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                   AER or aer: WFO Anchorage Eastern Domain
                   ALU or alu: WFO Anchorage Western Domain
                   AJK or ajk: WFO Juneau
                   AFG or afg: WFO Fairbanks
                   
43) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

44) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images.   

  ##### Minimum Relative Humidity Trend Forecast

This function plots the latest available NOAA/NWS Minimum RH Forecast. 

Required Arguments: None

Optional Arguments: 

1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
   This is a feature of matplotlib, as per their definition, the shrink is:
   "Fraction by which to multiply the size of the colorbar." 
   This should only be changed if the user wishes to change the size of the colorbar. 
   Preset values are called from the settings module for each state and/or gacc_region.
    
2) title_fontsize (Integer) - Fontsize of the plot title. 
    Default setting is 12 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region. 

3) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.  

4) signature_fontsize (Integer) - The fontsize of the signature. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

5) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
    Default setting is 8 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

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

27) psa_color (String) - Default = 'black'. Color of the PSA borders.

28) gacc_color (String) - Default = 'black'. Color of the GACC borders.

29) cwa_color (String) - Default = 'black'. Color of the CWA borders.

30) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

31) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

32) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

33) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

34) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 


35) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

36) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

37) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

38) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

39) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

40) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

41) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

42) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                   AER or aer: WFO Anchorage Eastern Domain
                   ALU or alu: WFO Anchorage Western Domain
                   AJK or ajk: WFO Juneau
                   AFG or afg: WFO Fairbanks
                   
43) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

44) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images.   

  #### Temperature Class

The `nws_temperature_forecast_alaska` class hosts 7 functions that plot the NWS Temperature Forecasts for Alaska:

1) [Extreme Heat Forecast](#extreme-heat-forecast)

2) [Extremely Warm Low Temperature Forecast](#extremely-warm-low-temperature-forecast)

3) [Frost/Freeze Forecast](#frostfreeze-forecast) 

4) [Maximum Temperature Forecast](#maximum-temperature-forecast)

5) [Minimum Temperature Forecast](#minimum-temperature-forecast)

6) [Maximum Temperature Trend Forecast](#maximum-temperature-trend-forecast)

7) [Minimum Temperature Trend Forecast](#minimum-temperature-trend-forecast)

 ##### Extreme Heat Forecast

This function plots the latest available NOAA/NWS Extreme Heat Forecast. 

Required Arguments: None

Optional Arguments: 

1) start_of_warm_season_month (Integer) - Default = 5 (May). The numeric value for the month the warm season begins. 

2) end_of_warm_season_month (Integer) - Default = 9 (September). The numeric value for the month the warm season ends. 

3) start_of_cool_season_month (Integer) - Default = 10 (October). The numeric value for the month the cool season begins. 

4) end_of_cool_season_month (Integer) - Default = 4 (April). The numeric value for the month the cool season ends.

5) temp_scale_warm_start (Integer) - Default = 70. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

6) temp_scale_warm_stop (Integer) - Default = 90. The top bound temperature value in Fahrenheit of the warm season temperature range.

7) temp_scale_cool_start (Integer) - Default = 70. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

8) temp_scale_cool_stop (Integer) - Default = 90. The top bound temperature value in Fahrenheit of the cool season temperature range. 

9) temp_scale_step (Integer) - Default = 1. The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                             (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

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

44) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
  This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
  binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
  Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
  function. 

45) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
  This setting is only to be changed if the user wants to limit the amount of downloads from the 
  NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
  if the user wishes to download the data outside of this function. 

46) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
  This setting is only to be changed if the user wants to limit the amount of downloads from the 
  NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
  if the user wishes to download the data outside of this function. 

47) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
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

51) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

52) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images.  

 ##### Extremely Warm Low Temperature Forecast

This function plots the latest available NOAA/NWS Extremely Warm Low Temperature Forecast. 

Required Arguments: None

Optional Arguments: 

1) start_of_warm_season_month (Integer) - Default = 5 (May). The numeric value for the month the warm season begins. 

2) end_of_warm_season_month (Integer) - Default = 9 (September). The numeric value for the month the warm season ends. 

3) start_of_cool_season_month (Integer) - Default = 10 (October). The numeric value for the month the cool season begins. 

4) end_of_cool_season_month (Integer) - Default = 4 (April). The numeric value for the month the cool season ends.

5) temp_scale_warm_start (Integer) - Default = 60. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

6) temp_scale_warm_stop (Integer) - Default = 70. The top bound temperature value in Fahrenheit of the warm season temperature range.

7) temp_scale_cool_start (Integer) - Default = 60. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

8) temp_scale_cool_stop (Integer) - Default = 80. The top bound temperature value in Fahrenheit of the cool season temperature range. 

9) temp_scale_step (Integer) - Default = 1. The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                               (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

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

44) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

45) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

46) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

47) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
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

51) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

52) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images.   

 ##### Frost/Freeze Forecast

This function plots the latest available NOAA/NWS Frost/Freeze Forecast. 

Required Arguments: None

Optional Arguments: 

1) temperature_bottom_bound (Integer) - Default = -10. 
 The temperature value in Fahrenheit for the bottom bound of the temperature scale. 
 This value must be less than 32.  

2) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
 This is a feature of matplotlib, as per their definition, the shrink is:
 "Fraction by which to multiply the size of the colorbar." 
 This should only be changed if the user wishes to change the size of the colorbar. 
 Preset values are called from the settings module for each state and/or gacc_region.
  
3) title_fontsize (Integer) - Fontsize of the plot title. 
  Default setting is 12 point font for a custom plot. Default fontsizes
  are called from the settings module for each state and/or gacc_region. 

4) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
  Default setting is 10 point font for a custom plot. Default fontsizes
  are called from the settings module for each state and/or gacc_region.  

5) signature_fontsize (Integer) - The fontsize of the signature. 
  Default setting is 10 point font for a custom plot. Default fontsizes
  are called from the settings module for each state and/or gacc_region.

6) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
  Default setting is 8 point font for a custom plot. Default fontsizes
  are called from the settings module for each state and/or gacc_region.

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

28) psa_color (String) - Default = 'black'. Color of the PSA borders.

29) gacc_color (String) - Default = 'black'. Color of the GACC borders.

30) cwa_color (String) - Default = 'black'. Color of the CWA borders.

31) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

32) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

33) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
  sample points are displayed on the graphic. Default setting is True. If the user wants 
  to hide the sample point values and only have the contour shading, this value will need 
  to be changed to False. 

34) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
  Default setting is a 10 point fontsize. 

35) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
  A value of 0 is completely transparent while a value of 1 is completely opaque. 
  Default setting is 0.5. 


36) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
  This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
  binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
  Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
  function. 

37) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
  This setting is only to be changed if the user wants to limit the amount of downloads from the 
  NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
  if the user wishes to download the data outside of this function. 

38) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
  This setting is only to be changed if the user wants to limit the amount of downloads from the 
  NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
  if the user wishes to download the data outside of this function. 

39) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
  This setting is only to be changed if the user wants to limit the amount of downloads from the 
  NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
  if the user wishes to download the data outside of this function. 

40) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
  is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
  data_access module. This value is to be passed in if and only if the user downloads the data outside 
  of this function. Default setting is None. 

41) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
  is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
  data_access module. This value is to be passed in if and only if the user downloads the data outside 
  of this function. Default setting is None. 

42) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
  sample points to appear in good order. Example: A value of 300 plots the sample point for one row
  of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
  Lower values equal more sample points which are less spaced apart. The default value is None. If
  the default value is selected, the decimation is scaled automatically, however if the user wishes 
  to change the spacing of the sample points, then the user must edit this value. 

43) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                 AER or aer: WFO Anchorage Eastern Domain
                 ALU or alu: WFO Anchorage Western Domain
                 AJK or ajk: WFO Juneau
                 AFG or afg: WFO Fairbanks
                 
44) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

45) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

 ##### Maximum Temperature Forecast

This function plots the latest available NOAA/NWS Maximum Temperature Forecast. 

Required Arguments: None

Optional Arguments: 

1) start_of_warm_season_month (Integer) - Default = 5 (May). The numeric value for the month the warm season begins. 

2) end_of_warm_season_month (Integer) - Default = 9 (September). The numeric value for the month the warm season ends. 

3) start_of_cool_season_month (Integer) - Default = 10 (October). The numeric value for the month the cool season begins. 

4) end_of_cool_season_month (Integer) - Default = 4 (April). The numeric value for the month the cool season ends.

5) temp_scale_warm_start (Integer) - Default = 60. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

6) temp_scale_warm_stop (Integer) - Default = 70. The top bound temperature value in Fahrenheit of the warm season temperature range.

7) temp_scale_cool_start (Integer) - Default = 60. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

8) temp_scale_cool_stop (Integer) - Default = 80. The top bound temperature value in Fahrenheit of the cool season temperature range. 

9) temp_scale_step (Integer) - Default = 1. The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                               (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

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

44) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

45) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

46) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

47) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
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

51) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

52) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images.   

 ##### Minimum Temperature Forecast

This function plots the latest available NOAA/NWS Minimum Temperature Forecast. 

Required Arguments: None

Optional Arguments: 

1) start_of_warm_season_month (Integer) - Default = 5 (May). The numeric value for the month the warm season begins. 

2) end_of_warm_season_month (Integer) - Default = 9 (September). The numeric value for the month the warm season ends. 

3) start_of_cool_season_month (Integer) - Default = 10 (October). The numeric value for the month the cool season begins. 

4) end_of_cool_season_month (Integer) - Default = 4 (April). The numeric value for the month the cool season ends.

5) temp_scale_warm_start (Integer) - Default = 10. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

6) temp_scale_warm_stop (Integer) - Default = 60. The top bound temperature value in Fahrenheit of the warm season temperature range.

7) temp_scale_cool_start (Integer) - Default = -30. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

8) temp_scale_cool_stop (Integer) - Default = 40. The top bound temperature value in Fahrenheit of the cool season temperature range. 

9) temp_scale_step (Integer) - Default = 1. The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                               (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

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

44) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

45) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

46) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

47) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
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

51) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

52) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images.   

 ##### Maximum Temperature Trend Forecast

This function plots the latest available NOAA/NWS Minimum Temperature Trend Forecast. 

Required Arguments: None

Optional Arguments: 

1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
   This is a feature of matplotlib, as per their definition, the shrink is:
   "Fraction by which to multiply the size of the colorbar." 
   This should only be changed if the user wishes to change the size of the colorbar. 
   Preset values are called from the settings module for each state and/or gacc_region.
    
2) title_fontsize (Integer) - Fontsize of the plot title. 
    Default setting is 12 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region. 

3) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.  

4) signature_fontsize (Integer) - The fontsize of the signature. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

5) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
    Default setting is 8 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

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

27) psa_color (String) - Default = 'black'. Color of the PSA borders.

28) gacc_color (String) - Default = 'black'. Color of the GACC borders.

29) cwa_color (String) - Default = 'black'. Color of the CWA borders.

30) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

31) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

32) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

33) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

34) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 


35) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

36) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

37) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

38) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

39) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

40) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

41) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

42) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                   AER or aer: WFO Anchorage Eastern Domain
                   ALU or alu: WFO Anchorage Western Domain
                   AJK or ajk: WFO Juneau
                   AFG or afg: WFO Fairbanks
                   
43) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

44) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

 ##### Minimum Temperature Trend Forecast

This function plots the latest available NOAA/NWS Minimum Temperature Trend Forecast. 

Required Arguments: None

Optional Arguments: 

1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
   This is a feature of matplotlib, as per their definition, the shrink is:
   "Fraction by which to multiply the size of the colorbar." 
   This should only be changed if the user wishes to change the size of the colorbar. 
   Preset values are called from the settings module for each state and/or gacc_region.
    
2) title_fontsize (Integer) - Fontsize of the plot title. 
    Default setting is 12 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region. 

3) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.  

4) signature_fontsize (Integer) - The fontsize of the signature. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

5) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
    Default setting is 8 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

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

27) psa_color (String) - Default = 'black'. Color of the PSA borders.

28) gacc_color (String) - Default = 'black'. Color of the GACC borders.

29) cwa_color (String) - Default = 'black'. Color of the CWA borders.

30) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

31) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

32) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

33) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

34) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 


35) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

36) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

37) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

38) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

39) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

40) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

41) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

42) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                   AER or aer: WFO Anchorage Eastern Domain
                   ALU or alu: WFO Anchorage Western Domain
                   AJK or ajk: WFO Juneau
                   AFG or afg: WFO Fairbanks
                   
43) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

44) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 

#### Hot Dry And Windy Class

The `nws_hot_dry_and_windy_alaska` class hosts 2 functions that plot the NWS Forecasts for Hot Dry and Windy as well as Hot Dry and Gusty conditons for Alaska. 

1) [Hot Dry And Windy Forecast](#hot-dry-and-windy-forecast)

2) [Hot Dry And Gusty Forecast](#hot-dry-and-gusty-forecast)

##### Hot Dry And Windy Forecast

This function plots the latest available NOAA/NWS Dry and Windy Forecast.

Areas where the relative humidity <= low_minimum_rh_threshold AND wind speed >= wind_speed_threshold AND temperature >= pre_greenup_temperature_threshold/post_greenup_temperature_threshold are shaded in red. 

Required Arguments: None

Optional Arguments: 

1) pre_greenup_temperature_threshold (Integer) - Default = 65F. Threshold for "hot" temperature based on the NWS Alaska Region RFW
   criteria for pre-greenup. Any values greater than or equal to this threshold are considered "hot". 

2) post_greenup_temperature_threshold (Integer) - Default = 75F. Threshold for "hot" temperature based on the NWS Alaska Region RFW
   criteria for post-greenup. Any values greater than or equal to this threshold are considered "hot".         

3) low_minimum_rh_threshold (Integer) - Default = 15%. Threshold for low relative humidity. Any values less or equal to this threshold are considered "dry."

4) wind_speed_threshold (Integer) - Default = 25 MPH. Threshold for high winds (sustained winds). Any values greater than or equal to this threshold are considered "windy."  

5) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
   This is a feature of matplotlib, as per their definition, the shrink is:
   "Fraction by which to multiply the size of the colorbar." 
   This should only be changed if the user wishes to change the size of the colorbar. 
   Preset values are called from the settings module for each state and/or gacc_region.
    
6) title_fontsize (Integer) - Fontsize of the plot title. 
    Default setting is 12 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region. 

7) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.  

8) signature_fontsize (Integer) - The fontsize of the signature. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

9) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
    Default setting is 8 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

10) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
    Default setting is True. Users should change this value to False if they wish to hide rivers.

11) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                       

13) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

14) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

15) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

16) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

17) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

18) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

19) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

20) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

21) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

22) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

23) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

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

31) psa_color (String) - Default = 'black'. Color of the PSA borders.

32) gacc_color (String) - Default = 'black'. Color of the GACC borders.

33) cwa_color (String) - Default = 'black'. Color of the CWA borders.

34) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

35) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

36) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

37) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

38) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 


39) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

40) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

41) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

42) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

43) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

44) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

45) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

46) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                   AER or aer: WFO Anchorage Eastern Domain
                   ALU or alu: WFO Anchorage Western Domain
                   AJK or ajk: WFO Juneau
                   AFG or afg: WFO Fairbanks
                   
47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 
        
##### Hot Dry And Gusty Forecast

This function plots the latest available NOAA/NWS Dry and Windy Forecast.

Areas where the relative humidity <= low_minimum_rh_threshold AND wind gust >= wind_speed_threshold AND temperature >= pre_greenup_temperature_threshold/post_greenup_temperature_threshold are shaded in red. 

Required Arguments: None

Optional Arguments: 

1) pre_greenup_temperature_threshold (Integer) - Default = 65F. Threshold for "hot" temperature based on the NWS Alaska Region RFW
   criteria for pre-greenup. Any values greater than or equal to this threshold are considered "hot". 

2) post_greenup_temperature_threshold (Integer) - Default = 75F. Threshold for "hot" temperature based on the NWS Alaska Region RFW
   criteria for post-greenup. Any values greater than or equal to this threshold are considered "hot".         

3) low_minimum_rh_threshold (Integer) - Default = 15%. Threshold for low relative humidity. Any values less or equal to this threshold are considered "dry."

4) wind_speed_threshold (Integer) - Default = 25 MPH. Threshold for high winds (wind gust). Any values greater than or equal to this threshold are considered "gusty."  

5) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
   This is a feature of matplotlib, as per their definition, the shrink is:
   "Fraction by which to multiply the size of the colorbar." 
   This should only be changed if the user wishes to change the size of the colorbar. 
   Preset values are called from the settings module for each state and/or gacc_region.
    
6) title_fontsize (Integer) - Fontsize of the plot title. 
    Default setting is 12 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region. 

7) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.  

8) signature_fontsize (Integer) - The fontsize of the signature. 
    Default setting is 10 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

9) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
    Default setting is 8 point font for a custom plot. Default fontsizes
    are called from the settings module for each state and/or gacc_region.

10) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
    Default setting is True. Users should change this value to False if they wish to hide rivers.

11) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                       

13) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

14) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

15) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

16) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

17) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

18) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

19) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

20) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

21) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

22) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

23) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

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

31) psa_color (String) - Default = 'black'. Color of the PSA borders.

32) gacc_color (String) - Default = 'black'. Color of the GACC borders.

33) cwa_color (String) - Default = 'black'. Color of the CWA borders.

34) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

35) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

36) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
    sample points are displayed on the graphic. Default setting is True. If the user wants 
    to hide the sample point values and only have the contour shading, this value will need 
    to be changed to False. 

37) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
    Default setting is a 10 point fontsize. 

38) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
    A value of 0 is completely transparent while a value of 1 is completely opaque. 
    Default setting is 0.5. 


39) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
    This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
    binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
    Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
    function. 

40) ds_short (Data Array) - The xarray data array of the downloaded short term grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

41) ds_extended (Data Array) - The xarray data array of the downloaded extended grids dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

42) ds (Data Array) - The xarray data array of the downloaded dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

43) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

44) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
    is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
    data_access module. This value is to be passed in if and only if the user downloads the data outside 
    of this function. Default setting is None. 

45) decimate (String [Default]/Integer [Custom]) - Default = 'default'. This is the number of which the data is decimated by in order for the spacing of the 
    sample points to appear in good order. Example: A value of 300 plots the sample point for one row
    of data every 300 lines of data. Higher values equal less sample points that are more spaced apart. 
    Lower values equal more sample points which are less spaced apart. The default value is None. If
    the default value is selected, the decimation is scaled automatically, however if the user wishes 
    to change the spacing of the sample points, then the user must edit this value. 

46) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                   AER or aer: WFO Anchorage Eastern Domain
                   ALU or alu: WFO Anchorage Western Domain
                   AJK or ajk: WFO Juneau
                   AFG or afg: WFO Fairbanks
                   
47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

Return: Saves individual images to a folder and creates a GIF from those images. 










