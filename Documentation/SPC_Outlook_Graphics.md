# **Storm Prediction Center Outlook Graphics**

For more information on the methodology behind these Storm Prediction Center products, click [here](https://www.spc.noaa.gov/misc/about.html#FireWx)

### **Functions**
1) [plot_critical_fire_weather_risk_outlook()](#plot_critical_fire_weather_risk_outlook)
2) [plot_dry_lightning_outlook()](#plot_dry_lightning_outlook)
3) [plot_convective_outlook()](#plot_convective_outlook)

#### plot_critical_fire_weather_risk_outlook()

This function plots the latest available NOAA/NWS SPC Critical Fire Weather Risk Outlook. 

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

29) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
    Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
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

37) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

38) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

Return: Saves individual images to f:Weather Data/SPC Outlooks/Critical Fire Weather Risk Outlook/{reference_system}. 

#### plot_dry_lightning_outlook()

This function plots the latest available NOAA/NWS SPC Dry Lightning Outlook. 

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

29) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
    Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
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

37) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

38) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

Return: Saves individual images to f:Weather Data/SPC Outlooks/Dry Lightning Outlook/{reference_system}. 

#### plot_convective_outlook

This function plots the latest available NOAA/NWS SPC Convective Outlook. 

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

27) ds (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
    This setting is only to be changed if the user wants to limit the amount of downloads from the 
    NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
    if the user wishes to download the data outside of this function. 

28) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
    If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
    Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
    acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
    changed to None. 

29) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

30) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

31) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

32) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

33) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

34) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

35) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.     

36) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

37) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

Return: Saves individual images to f:Weather Data/SPC Outlooks/Convective Outlook/{reference_system}. 

