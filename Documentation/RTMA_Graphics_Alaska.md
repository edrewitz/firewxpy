# **Real Time Mesoscale Analysis Graphics Alaska**

### **Functions**

1) [plot_relative_humidity()](#plot_relative_humidity)
2) [plot_low_and_high_relative_humidity()](#plot_low_and_high_relative_humidity)
3) [plot_24_hour_relative_humidity_comparison()](#plot_low_and_high_relative_humidity)
4) [plot_temperature()](#plot_temperature)
5) [plot_temperature_advection()](#plot_temperature_advection)
6) [plot_dew_point_advection](#plot_dew_point_advection)
7) [plot_relative_humidity_advection()](#plot_relative_humidity_advection)
8) [plot_frost_freeze()](#plot_frost_freeze)
9) [plot_extreme_heat()](#plot_extreme_heat)
10) [plot_24_hour_temperature_comparison()](#plot_24_hour_temperature_comparison)
11) [plot_dew_point()](#plot_dew_point)
12) [plot_24_hour_dew_point_comparison()](#plot_24_hour_dew_point_comparison)
13) [plot_total_cloud_cover()](#plot_total_cloud_cover)
14) [plot_24_hour_total_cloud_cover_comparison()](#plot_24_hour_total_cloud_cover_comparison)
15) [plot_wind_speed()](#plot_wind_speed)
16) [plot_24_hour_wind_speed_comparison()](#plot_24_hour_wind_speed_comparison)
17) [plot_wind_speed_and_direction()](#plot_wind_speed_and_direction)
18) [plot_24_hour_wind_speed_and_direction_comparison()](#plot_24_hour_wind_speed_and_direction_comparison)
19) [plot_hot_dry_and_windy_areas()](#plot_dry_and_windy_areas)
20) [plot_hot_dry_and_gusty_areas()](#plot_dry_and_gusty_areas)

### plot_relative_humidity()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Relative Humidity. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            36) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            37) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            38) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            39) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_low_and_high_relative_humidity()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Relative Humidity filtered for areas of low RH and high RH. 
    
        Required Arguments: None

        Optional Arguments: 1) low_rh_threshold (Integer) - Default = 25%. The top bound of what is considered low relative humidity. 

                            2) high_rh_threshold (Integer) - Default = 80%. The bottom bound of what is considered high relative humidity.         

                            3) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
                               This is a feature of matplotlib, as per their definition, the shrink is:
                               "Fraction by which to multiply the size of the colorbar." 
                               This should only be changed if the user wishes to change the size of the colorbar. 
                               Preset values are called from the settings module for each state and/or gacc_region.
                                
                            4) title_fontsize (Integer) - Fontsize of the plot title. 
                                Default setting is 12 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region. 
    
                            5) subplot_title_fontsize (Integer) - Fontsize of the subplot title. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.  
    
                            6) signature_fontsize (Integer) - The fontsize of the signature. 
                                Default setting is 10 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            7) colorbar_fontsize (Integer) - The fontsize of the colorbar label. 
                                Default setting is 8 point font for a custom plot. Default fontsizes
                                are called from the settings module for each state and/or gacc_region.
    
                            8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
                                Default setting is True. Users should change this value to False if they wish to hide rivers.

                            9) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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

                            36) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            37) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            38) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            39) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            40) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            41) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_24_hour_relative_humidity_comparison()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Relative Humidity. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) data_24 (Array) - Default = None. A data array (for 24hrs prior to the latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data_24=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data_24=None to data_24=data for example.  

                            36) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            37) time_24 (Array) - Default = None. A time array (for the dataset that is 24-hours prior to current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,

                            38) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            39) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            40) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            41) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_temperature()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Temperature. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            36) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            37) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            38) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            40) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_temperature_advection()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Temperature Advection. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            36) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            37) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            38) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            39) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_dew_point_advection()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Dew Point Advection. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            36) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            37) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            38) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            39) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_relative_humidity_advection()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Relative Humidity Advection. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            36) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            37) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            38) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            39) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_frost_freeze()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Frost/Freeze Areas (RTMA Temperature <= 32F). 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            36) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            37) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            38) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            39) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_extreme_heat()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Extreme Heat. 
    
        Required Arguments: None

        Optional Arguments: 1) temperature_threshold (Integer) - Default = 70F. The threshold at which the user defines extreme heat. 
                               Extreme Heat = RTMA Temperature >= temperature_threshold.
        
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

                            35) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            36) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            37) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            38) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            39) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            40) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_24_hour_temperature_comparison()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Temperature. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) data_24 (Array) - Default = None. A data array (for 24hrs prior to the latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data_24=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data_24=None to data_24=data for example.  

                            36) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            37) time_24 (Array) - Default = None. A time array (for the dataset that is 24-hours prior to current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,

                            38) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            39) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            40) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            41) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_dew_point()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Dew Point. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            36) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            37) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            38) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            39) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.
        
### plot_24_hour_dew_point_comparison()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Dew Point. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) data_24 (Array) - Default = None. A data array (for 24hrs prior to the latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data_24=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data_24=None to data_24=data for example.  

                            36) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            37) time_24 (Array) - Default = None. A time array (for the dataset that is 24-hours prior to current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,

                            38) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            39) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            40) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            41) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_total_cloud_cover()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Total Cloud Cover. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            36) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            37) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            38) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            39) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.
        
### plot_24_hour_total_cloud_cover_comparison()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Total Cloud Cover. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) data_24 (Array) - Default = None. A data array (for 24hrs prior to the latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data_24=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data_24=None to data_24=data for example.  

                            36) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            37) time_24 (Array) - Default = None. A time array (for the dataset that is 24-hours prior to current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,

                            38) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            39) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            40) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            41) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_wind_speed()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) Wind Speed. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            36) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            37) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            38) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            39) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_24_hour_wind_speed_comparison()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Wind Speed. 
    
        Required Arguments: None

        Optional Arguments: 1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
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

                            46) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            47) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            48) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            49) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_wind_speed_and_direction()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) for Wind Speed & Direction. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            36) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            37) barbs_or_quivers (String) - Default = 'barbs'. Sets the plot to either be wind barbs or vectors. Proper syntax for wind barbs: 'barbs', 'b', 'Barbs',
                                'BARBS', 'B'. Proper syntax for quivers (vectors): 'quivers', 'q', 'Quivers', 'QUIVERS', 'Q'

                            38) barb_quiver_alpha (Float) - Default = 1. Number between 0 and 1 for the transparency of the barb or quiver. 0 is completely transparent while 1 is completely opaque. 

                            39) barb_quiver_fontsize (Integer) - Default = 6. Fontsize of the barb or quiver. 

                            40) barb_linewidth (Float) - Default = 0.5. The width or thickness of the wind barb. 

                            41) quiver_linewidth (Float) - Default = 0.5. The width or thickness of the quiver. 

                            42) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            43) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            44) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_24_hour_wind_speed_and_direction_comparison()

        This function plots the latest available Real Time Mesoscale Analysis (RTMA) 24-Hour Comparison for Wind Speed & Direction. 
    
        Required Arguments: None

        Optional Arguments: 1) color_table_shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
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

                            26) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            27) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            28) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            29) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            30) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            31) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            32) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            33) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            34) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            35) data_24 (Array) - Default = None. A data array (for 24hrs prior to the latest available time) if the user downloads the data array outside of the function using the data_access module. 
                                If data_24=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data_24=None to data_24=data for example.  

                            36) time (Array) - Default = None. A time array (for the dataset of the current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            37) time_24 (Array) - Default = None. A time array (for the dataset that is 24-hours prior to current time) if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,

                            38) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            39) barbs_or_quivers (String) - Default = 'barbs'. Sets the plot to either be wind barbs or vectors. Proper syntax for wind barbs: 'barbs', 'b', 'Barbs',
                                'BARBS', 'B'. Proper syntax for quivers (vectors): 'quivers', 'q', 'Quivers', 'QUIVERS', 'Q'

                            40) barb_quiver_alpha (Float) - Default = 1. Number between 0 and 1 for the transparency of the barb or quiver. 0 is completely transparent while 1 is completely opaque. 

                            41) barb_quiver_fontsize (Integer) - Default = 6. Fontsize of the barb or quiver. 

                            42) barb_linewidth (Float) - Default = 0.5. The width or thickness of the wind barb. 

                            43) quiver_linewidth (Float) - Default = 0.5. The width or thickness of the quiver. 

                            44) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            45) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            46) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_hot_dry_and_windy_areas()

        This function plots the latest available RTMA Hot, Dry and Windy Areas with their components.

        Areas where the relative humidity <= low_minimum_rh_threshold AND wind gust >= wind_speed_threshold AND temperature >= pre_greenup_temperature_threshold/post_greenup_temperature_threshold are shaded in red. 
    
        Required Arguments: None

        Optional Arguments: 1) pre_greenup_temperature_threshold (Integer) - Default = 65F. Threshold for "hot" temperature based on the NWS Alaska Region RFW
                               criteria for pre-greenup. Any values greater than or equal to this threshold are considered "hot". 
        
                            2) post_greenup_temperature_threshold (Integer) - Default = 75F. Threshold for "hot" temperature based on the NWS Alaska Region RFW
                               criteria for post-greenup. Any values greater than or equal to this threshold are considered "hot".   
        
                            3) low_rh_threshold (Integer) - Default = 25%. The top bound of what is considered low relative humidity. 

                            4) high_wind_threshold (Integer) - Default = 15 MPH. The bottom bound of what is considered high sustained winds.         

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
                                                   
    
                            12) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            13) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            14) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            15) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            16) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            17) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            18) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            19) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            20) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            21) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            22) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            23) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            24) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            25) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            26) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            27) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            28) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            29) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            30) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            31) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            32) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            33) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            34) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            35) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            36) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            37) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            38) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            39) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            40) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            41) sample_point_type (String) - Default='barbs'. The type of sample point. The options are either wind barbs or the raw numbers for the wind speeds. Wind barbs
                                are the default since barbs incorporates wind direction.

                            42) barb_quiver_linewidth (Float) - Default = 0.5. The width or thickness of the wind barb or quiver. 

                            43) barb_fontsize (Integer) - Default = 6. Fontsize of the barb. 

                            44) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            45) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            46) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

### plot_hot_dry_and_gusty_areas()

        This function plots the latest available RTMA Hot, Dry and Gusty Areas with their components.

        Areas where the relative humidity <= low_minimum_rh_threshold AND wind gust >= wind_speed_threshold AND temperature >= pre_greenup_temperature_threshold/post_greenup_temperature_threshold are shaded in red. 
    
        Required Arguments: None

        Optional Arguments: 1) pre_greenup_temperature_threshold (Integer) - Default = 65F. Threshold for "hot" temperature based on the NWS Alaska Region RFW
                               criteria for pre-greenup. Any values greater than or equal to this threshold are considered "hot". 
        
                            2) post_greenup_temperature_threshold (Integer) - Default = 75F. Threshold for "hot" temperature based on the NWS Alaska Region RFW
                               criteria for post-greenup. Any values greater than or equal to this threshold are considered "hot".   
        
                            3) low_rh_threshold (Integer) - Default = 25%. The top bound of what is considered low relative humidity. 

                            4) high_wind_threshold (Integer) - Default = 15 MPH. The bottom bound of what is considered high wind gusts.         

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
                                                   
    
                            12) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide state borders. 

                            13) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                                Default setting is False. Users should change this value to False if they wish to hide county borders. 

                            14) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display GACC borders. 

                            15) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display PSA borders.

                            16) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display CWA borders.

                            17) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

                            18) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

                            19) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

                            20) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

                            21) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

                            22) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

                            23) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                                To change to a dashed line, users should set state_border_linestyle='--'. 

                            24) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                                To change to a dashed line, users should set county_border_linestyle='--'. 

                            25) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                                To change to a dashed line, users should set gacc_border_linestyle='--'. 

                            26) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            27) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            28) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            29) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                                To change to a dashed line, users should set psa_border_linestyle='--'. 

                            30) psa_color (String) - Default = 'black'. Color of the PSA borders.

                            31) gacc_color (String) - Default = 'black'. Color of the GACC borders.

                            32) cwa_color (String) - Default = 'black'. Color of the CWA borders.

                            33) fwz_color (String) - Default = 'black'. Color of the FWZ borders.

                            34) pz_color (String) - Default = 'black'. Color of the Public Zone borders.

                            35) show_sample_points (Boolean) - When this setting is set to True, the numeric values of
                                sample points are displayed on the graphic. Default setting is True. If the user wants 
                                to hide the sample point values and only have the contour shading, this value will need 
                                to be changed to False. 

                            36) sample_point_fontsize (Integer) - The fontsize of the sample point numbers. 
                                Default setting is a 10 point fontsize. 

                            37) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
                                A value of 0 is completely transparent while a value of 1 is completely opaque. 
                                Default setting is 0.5. 

                            38) data (Array) - Default = None. A data array if the user downloads the data array outside of the function using the data_access module. 
                                If data=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change data=None to data=data for example. 

                            39) time (Array) - Default = None. A time array if the user downloads the data array outside of the function using the data_access module. 
                                If time=None, the function will download the data inside of the function. If the user is generating several RTMA images in an automated script,
                                it is recommended to download the data outside of the function and change time=None to time=time for example. 

                            40) colorbar_pad (Float) - Default = 0.02. How close or far on the figure the colorbar is to the edge of the map. The lower the number, the closer and
                                the higher the number the farther away. See matplotlib documentation for more information. 

                            41) sample_point_type (String) - Default='barbs'. The type of sample point. The options are either wind barbs or the raw numbers for the wind speeds. Wind barbs
                                are the default since barbs incorporates wind direction.

                            42) barb_quiver_linewidth (Float) - Default = 0.5. The width or thickness of the wind barb or quiver. 

                            43) barb_fontsize (Integer) - Default = 6. Fontsize of the barb. 

                            44) aspect (Integer) - Default = 30. Ratio of the long dimension to the short dimension of the colorbar. See matplotlib docs for more information. 

                            45) tick (Integer) - Default = 9. Fontsize of colorbar ticks. 

                            46) cwa (String) - Default = None. This is the 3 letter identifier for the NWS Alaska Region CWA. 
                                               AER or aer: WFO Anchorage Eastern Domain
                                               ALU or alu: WFO Anchorage Western Domain
                                               AJK or ajk: WFO Juneau
                                               AFG or afg: WFO Fairbanks
    
        Return: Saves individual images to the RTMA subfolder.

