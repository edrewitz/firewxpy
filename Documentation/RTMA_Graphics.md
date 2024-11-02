# **Real Time Mesoscale Analysis Graphics**

### **Functions**

1) [plot_relative_humidity](#plot_relative_humidity)
2) [plot_low_and_high_relative_humidity]
3) [plot_24_hour_relative_humidity_comparison]
4) [plot_temperature]
5) [plot_temperature_advection]
6) [plot_dew_point_advection]
7) [plot_relative_humidity_advection]
8) [plot_frost_freeze]
9) [plot_extreme_heat]
10) [plot_24_hour_temperature_comparison]
11) [plot_dew_point]
12) [plot_24_hour_dew_point_comparison]
13) [plot_total_cloud_cover]
14) [plot_24_hour_total_cloud_cover_comparison]
15) [plot_wind_speed]
16) [plot_24_hour_wind_speed_comparison]
17) [plot_wind_speed_and_direction]
18) [plot_24_hour_wind_speed_and_direction_comparison]
19) [plot_dry_and_windy_areas]
20) [plot_dry_and_gusty_areas]
21) [plot_relative_humidity_with_metar_obs]
22) [plot_low_relative_humidity_with_metar_obs]
23) [plot_wind_speed_with_observed_winds]
24) [plot_wind_gust_with_observed_winds]

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

### plot_low_and_high_relative_humidity()

This function plots the latest available Real Time Mesoscale Analysis (RTMA) Relative Humidity filtered for areas of low RH and high RH. 

Required Arguments: None

Optional Arguments: 

1) low_rh_threshold (Integer) - Default = 15%. The top bound of what is considered low relative humidity. 

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

### plot_24_hour_relative_humidity_comparison()

This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Relative Humidity. 

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

### plot_temperature_advection()

This function plots the latest available Real Time Mesoscale Analysis (RTMA) Temperature Advection. 

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

### plot_dew_point_advection()

This function plots the latest available Real Time Mesoscale Analysis (RTMA) Dew Point Advection. 

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

### plot_relative_humidity_advection()

This function plots the latest available Real Time Mesoscale Analysis (RTMA) Relative Humidity Advection. 

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

### plot_frost_freeze()
