# **Storm Prediction Center Outlook Graphics**

For more information on the methodology behind these Storm Prediction Center products, click [here](https://www.spc.noaa.gov/misc/about.html#FireWx)

### **Functions**
1) [Critical Fire Weather Forecast](#critical-fire-weather-forecast)
2) [Dry Ligtning Forecast](#dry-lightning-forecast)

#### Critical Fire Weather Forecast

This function plots the latest available Storm Prediction Center Critical Fire Weather Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/SPC_Outlook_Graphics.py#L40)

Required Arguments: None

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


26) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

27) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

29) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

30) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

31) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

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
    
Return: A list of figures for each forecast day. 

#### Dry Lightning Forecast

This function plots the latest available Storm Prediction Center Dry Lightning Forecast. [Source Code](https://github.com/edrewitz/FireWxPy/blob/main/src/SPC_Outlook_Graphics.py#L631)

Required Arguments: None

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


26) alpha (Float) - A value between 0 and 1 that determines the transparency of the contour shading. 
A value of 0 is completely transparent while a value of 1 is completely opaque. 
Default setting is 0.5. 

27) directory_name (String) - This is the directory on the NWS FTP Server where the data gets pulled from. 
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

29) file_path (String) - The local file path of the downloaded binary file from the NWS FTP Server (e.g. 'ds.maxt.bin' for the Maximum Temperature Forecast) 
This setting is only to be changed if the user wants to limit the times the file downloads in the script and downloads the 
binary file outside of the functions (which is to be done at the beginning of the script before these plotting functions are called). 
Default setting is None. Please see the documentation for the data_access module if the user wishes to download the data outside of this
function. 

30) count_short (Integer) - This is the number of GRIB timestamps in the short-term forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

31) count_extended (Integer) - This is the number of GRIB timestamps in the extended forecast. This value
is returned by the function that downloads the NWS Forecast data in the FTP_Downloads class of the 
data_access module. This value is to be passed in if and only if the user downloads the data outside 
of this function. Default setting is None. 

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
    
Return: A list of figures for each forecast day. 

