# **Observations**

## Gridded Observations Class

This class hosts all the functions that use interpolation methods to make gridded data from observations. 

*Functions*

1) [plot_relative_humidity_observations()](#plot_relative_humidity_observations)

## METAR Observations Class

This class hosts the functions that plot METAR observations and make daily weather summaries for METAR observations

*Functions*

1) [graphical_daily_summary(station_id)](#graphical_daily_summarystation_id)
2) [plot_observations_map()](#plot_observations_map)

### plot_relative_humidity_observations()

This function makes a plot of the latest Gridded Relative Humidity Observations. 

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

26) data (Boolean) - Default = False. When set to False, the data is downloaded inside of the function.
  When making a lot of plots with the same dataset, download the data outside of the function and set
  date=True to pass the dataset into the function. 

27) df (Pandas DataFrame) - Default = None. The Pandas DataFrame of the METAR data. Set df=df when 
  downloading the data outside of the function and passing it in. 

28) mask (Integer or Float) - Default = 300000. This determines how many METARs show up on the graphic. 
  Lower values equal more METAR observations. Default reflects that of CONUS so when looking at a
  smaller area, you most likely would want to set this to a lower value. The value must be a positive
  non-zero number. 

29) time (datetime) - Default = None. This is the time of the METAR dataset. 
  When downloading the data outside of the function and passing in the data
  into the function, set time=time. 

30) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
  If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
  or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
  acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
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

41) interpolation_type (String) - Default='cressman'. This determines the type of interpolation method used. 

  Here are the various interpolation methods:

  1) cressman
  2) barnes
  3) linear
  4) nearest
  5) cubic
  6) rbf
  7) natural neighbor

42) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
  This is a feature of matplotlib, as per their definition, the shrink is:
  "Fraction by which to multiply the size of the colorbar." 
  This should only be changed if the user wishes to change the size of the colorbar. 
  Preset values are called from the settings module for each state and/or gacc_region.

Return: Saves individual images to f:Weather Data/Observations/GRIDDED RELATIVE HUMIDITY/{state}/{reference_system}/{interpolation_type}. 
If the user selects a cwa the path will look like this: f:Weather Data/Observations/METAR MAP/{state}/{reference_system}/{cwa}/{interpolation_type}.

### graphical_daily_summary(station_id)

This function creates a graphical daily weather summary and solar information for the previous day's ASOS observations at any particular ASOS site. 

Required Arguments: 1) station_id (String) - The 4-letter station identifier of the ASOS station

Optional Arguments: None

Returns: A saved figure to the observations folder showing a graphical daily weather summary and solar information for the previous day's ASOS observations. 
     The parameters on this daily weather summary are: 
     
     1) Temperature
     2) Relative Humidity
     3) Wind Speed
     4) Solar Elevation Angle
     5) Solar Radiation

### plot_observations_map()

This function makes a plot of the latest METAR observations. 

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

26) data (Boolean) - Default = False. When set to False, the data is downloaded inside of the function.
  When making a lot of plots with the same dataset, download the data outside of the function and set
  date=True to pass the dataset into the function. 

27) df (Pandas DataFrame) - Default = None. The Pandas DataFrame of the METAR data. Set df=df when 
  downloading the data outside of the function and passing it in. 

28) mask (Integer or Float) - Default = 3. This determines how many METARs show up on the graphic. 
  Lower values equal more METAR observations. Default reflects that of CONUS so when looking at a
  smaller area, you most likely would want to set this to a lower value. The value must be a positive
  non-zero number. 

29) time (datetime) - Default = None. This is the time of the METAR dataset. 
  When downloading the data outside of the function and passing in the data
  into the function, set time=time. 

37) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
  If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
  or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
  acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
  changed to None. 

30) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

31) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

32) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

33) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

34) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

35) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

36) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

37) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA. 
  For a view of the entire state - set cwa=None. 

  NWS CWA Abbreviations:

  1) AER - NWS Anchorage East Domain
  
  2) ALU - NWS Anchorage West Domain
  
  3) AJK - NWS Juneau
  
  4) AFG - NWS Fairbanks        

38) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

39) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

Return: Saves individual images to f:Weather Data/Observations/METAR MAP/{state}/{reference_system}. 
If the user selects a cwa the path will look like this: f:Weather Data/Observations/METAR MAP/{state}/{reference_system}/{cwa}
