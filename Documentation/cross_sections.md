# **Forecast Cross-Sections**

### **Classes**
1) [Time Cross-Sections](#time-cross-sections)
2) [Cross Sections Between Two Points]()


#### Time Cross-Sections
*This section of FireWxPy is inspired by Dr. Brian Tang's [WxChallenge Model Guidance](https://www.atmos.albany.edu/facstaff/tang/forecast/) Time Cross-section graphics.*  

**Here are the different functions in the Time vs. Pressure Cross-Sections Class**
1) [plot_lower_atmosphere_wind(model, station_id, save_name)](#plot_lower_atmosphere_windmodel-station_id-save_name)
2) [plot_lower_atmosphere_vertical_velocity(model, station_id, save_name)](#plot_lower_atmosphere_vertical_velocitymodel-station_id-save_name)
3) [plot_lower_atmosphere_temperature_rh_vertical_velocity_wind(model, station_id, save_name)](#plot_lower_atmosphere_temperature_rh_vertical_velocity_windmodel-station_id-save_name)
4) [plot_lower_atmosphere_temperature_and_wind(model, station_id, save_name)](#plot_lower_atmosphere_temperature_and_windmodel-station_id-save_name)
5) [plot_lower_atmosphere_relative_humidity_and_wind(model, station_id, save_name)](#plot_lower_atmosphere_relative_humidity_and_windmodel-station_id-save_name)
6) [plot_lower_atmosphere_theta_e_and_wind(model, station_id, save_name)](#plot_lower_atmosphere_theta_e_and_windmodel-station_id-save_name)
7) [plot_lower_atmosphere_theta_e_rh_vertical_velocity_wind(model, station_id, save_name)](#plot_lower_atmosphere_theta_e_rh_vertical_velocity_windmodel-station_id-save_name)
8) [plot_favorable_firewx_forecast(model, station_id, save_name)](#plot_favorable_firewx_forecastmodel-station_id-save_name)

##### plot_lower_atmosphere_wind(model, station_id, save_name)
This function plots a time vs. pressure cross-section forecast for a given point. Paramter: Lower Atmosphere Wind. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) station_id (String) - The 4-letter airport station identifier. 
                         If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                        Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 

Optional Arguments:

1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 

2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 

3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
    and passing the data in or if the function needs to download the data. A value of False means the data
    is downloaded inside of the function while a value of True means the user is downloading the data outside
    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
    things, it is recommended to set this value to True and download the data outside of the function and pass
    it in so that the amount of data requests on the host servers can be minimized. 


4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
    in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
    outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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


6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}


##### plot_lower_atmosphere_vertical_velocity(model, station_id, save_name)
This function plots a time vs. pressure cross-section forecast for a given point. Paramter: Vertical Velocity. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) station_id (String) - The 4-letter airport station identifier. 
                         If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                        Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 

Optional Arguments:

1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 

2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 

3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
    and passing the data in or if the function needs to download the data. A value of False means the data
    is downloaded inside of the function while a value of True means the user is downloading the data outside
    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
    things, it is recommended to set this value to True and download the data outside of the function and pass
    it in so that the amount of data requests on the host servers can be minimized. 


4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
    in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
    outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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


6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}

##### plot_lower_atmosphere_temperature_rh_vertical_velocity_wind(model, station_id, save_name)
This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Temperature/RH/Vertical Velocity/Wind. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) station_id (String) - The 4-letter airport station identifier. 
                         If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                        Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 

Optional Arguments:

1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 

2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 

3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
    and passing the data in or if the function needs to download the data. A value of False means the data
    is downloaded inside of the function while a value of True means the user is downloading the data outside
    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
    things, it is recommended to set this value to True and download the data outside of the function and pass
    it in so that the amount of data requests on the host servers can be minimized. 


4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
    in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
    outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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


6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}

##### plot_lower_atmosphere_temperature_and_wind(model, station_id, save_name)
This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Temperature/Wind. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) station_id (String) - The 4-letter airport station identifier. 
                         If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                        Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 

Optional Arguments:

1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 

2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 

3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
    and passing the data in or if the function needs to download the data. A value of False means the data
    is downloaded inside of the function while a value of True means the user is downloading the data outside
    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
    things, it is recommended to set this value to True and download the data outside of the function and pass
    it in so that the amount of data requests on the host servers can be minimized. 


4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
    in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
    outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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


6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}

##### plot_lower_atmosphere_relative_humidity_and_wind(model, station_id, save_name)
This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere RH/Wind. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) station_id (String) - The 4-letter airport station identifier. 
                         If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                        Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 

Optional Arguments:

1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 

2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 

3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
    and passing the data in or if the function needs to download the data. A value of False means the data
    is downloaded inside of the function while a value of True means the user is downloading the data outside
    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
    things, it is recommended to set this value to True and download the data outside of the function and pass
    it in so that the amount of data requests on the host servers can be minimized. 


4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
    in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
    outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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


6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}

##### plot_lower_atmosphere_theta_e_and_wind(model, station_id, save_name)
This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Theta-E/Wind. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) station_id (String) - The 4-letter airport station identifier. 
                         If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                        Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 

Optional Arguments:

1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 

2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 

3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
    and passing the data in or if the function needs to download the data. A value of False means the data
    is downloaded inside of the function while a value of True means the user is downloading the data outside
    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
    things, it is recommended to set this value to True and download the data outside of the function and pass
    it in so that the amount of data requests on the host servers can be minimized. 


4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
    in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
    outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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


6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide state borders. 

7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
    Default setting is False. Users should change this value to False if they wish to hide county borders. 

8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display GACC borders. 

9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display PSA borders.

10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display CWA borders.

11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
    Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}

##### plot_lower_atmosphere_theta_e_rh_vertical_velocity_wind(model, station_id, save_name)
This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Theta-E/RH/Vertical Velocity/Wind. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                     
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) station_id (String) - The 4-letter airport station identifier. 
                       If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                      Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 

Optional Arguments:

1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 

2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 

3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
  and passing the data in or if the function needs to download the data. A value of False means the data
  is downloaded inside of the function while a value of True means the user is downloading the data outside
  of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
  things, it is recommended to set this value to True and download the data outside of the function and pass
  it in so that the amount of data requests on the host servers can be minimized. 


4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
  in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
  outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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


6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
  Default setting is False. Users should change this value to False if they wish to hide state borders. 

7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
  Default setting is False. Users should change this value to False if they wish to hide county borders. 

8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
  Default setting is False. Users should change this value to True if they wish to display GACC borders. 

9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
  Default setting is False. Users should change this value to True if they wish to display PSA borders.

10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
  Default setting is False. Users should change this value to True if they wish to display CWA borders.

11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
  Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
  Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}

##### plot_favorable_firewx_forecast(model, station_id, save_name)
This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Favorable Fire Weather Forecast. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) station_id (String) - The 4-letter airport station identifier. 
                         If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                        Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 

Optional Arguments:

1) low_rh_threshold (Integer) - Default = 15. The threshold for the contour line that defines what extremely low relative humidity is.

2) high_wind_threshold (Integer) - Default = 25. The threshold for the contour line that defines what high winds are.

3) temperature_threshold (Integer) - Default = None. This is to be used if the user wishes to add temperature as a factor to what 
   defines favorable fire weather conditions. When set to None, only RH & Wind Speed/Gust are taken 
   into account. When set to an integer value, the temperature will also be taken into account. 

4) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 

5) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 

6) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
    and passing the data in or if the function needs to download the data. A value of False means the data
    is downloaded inside of the function while a value of True means the user is downloading the data outside
    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
    things, it is recommended to set this value to True and download the data outside of the function and pass
    it in so that the amount of data requests on the host servers can be minimized. 


7) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
    in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
    outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

8) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}

#### Cross Sections Between Two Points

**Here are the different functions in the Time vs. Pressure Cross-Sections Class**

1) [plot_lower_atmosphere_wind(model, region, starting_point, ending_point)](#plot_lower_atmosphere_windmodel-region-starting_point-ending_point)
2) [plot_lower_atmosphere_vertical_velocity(model, region, starting_point, ending_point)](#plot_lower_atmosphere_vertical_velocitymodel-region-starting_point-ending_point)
3) [plot_lower_atmosphere_temperature_rh_vertical_velocity_wind(model, region, starting_point, ending_point)](#plot_lower_atmosphere_temperature_rh_vertical_velocity_windmodel-region-starting_point-ending_point)
4) [plot_lower_atmosphere_temperature_and_wind(model, region, starting_point, ending_point)](#plot_lower_atmosphere_temperature_and_windmodel-region-starting_point-ending_point)
5) [plot_lower_atmosphere_relative_humidity_and_wind(model, region, starting_point, ending_point)](#plot_lower_atmosphere_relative_humidity_and_windmodel-region-starting_point-ending_point)
6) [plot_lower_atmosphere_theta_e_and_wind(model, region, starting_point, ending_point)](#plot_lower_atmosphere_theta_e_and_windmodel-region-starting_point-ending_point)
7) [plot_lower_atmosphere_theta_e_rh_vertical_velocity_wind(model, region, starting_point, ending_point)](#plot_lower_atmosphere_theta_e_rh_vertical_velocity_windmodel-region-starting_point-ending_point)
8) [plot_favorable_firewx_forecast(model, region, starting_point, ending_point)](#plot_favorable_firewx_forecastmodel-region-starting_point-ending_point)

##### plot_lower_atmosphere_wind(model, region, starting_point, ending_point)

This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Wind. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

4) ending_point (Tuple) - (lat,lon) in decimal degrees.

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

7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/


##### plot_lower_atmosphere_vertical_velocity(model, region, starting_point, ending_point)

This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Vertical Velocity. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

4) ending_point (Tuple) - (lat,lon) in decimal degrees.

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

7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/

##### plot_lower_atmosphere_temperature_rh_vertical_velocity_wind(model, region, starting_point, ending_point)

This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Temperature/RH/Vertical Velocity/Wind Barbs. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

4) ending_point (Tuple) - (lat,lon) in decimal degrees.

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

7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/

##### plot_lower_atmosphere_temperature_and_wind(model, region, starting_point, ending_point)

This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Temperature & Wind Barbs. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

4) ending_point (Tuple) - (lat,lon) in decimal degrees.

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

7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/

##### plot_lower_atmosphere_relative_humidity_and_wind(model, region, starting_point, ending_point)

This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere RH & Wind Barbs. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

4) ending_point (Tuple) - (lat,lon) in decimal degrees.

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

7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/

##### plot_lower_atmosphere_theta_e_and_wind(model, region, starting_point, ending_point)

This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Theta-E & Wind Barbs. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

4) ending_point (Tuple) - (lat,lon) in decimal degrees.

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

7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/

##### plot_lower_atmosphere_theta_e_rh_vertical_velocity_wind(model, region, starting_point, ending_point)

This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Theta-E & RH & Wind Barbs. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

4) ending_point (Tuple) - (lat,lon) in decimal degrees.

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

7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

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

Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/

##### plot_favorable_firewx_forecast(model, region, starting_point, ending_point)

This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Favorable Fire Weather Forecast. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
       Here are the choices: 
       1) GFS0p25 - GFS 0.25x0.25 degree
       2) NAM - North American Model
       3) RAP - RAP for the CONUS
       4) RAP 32 - 32km North American RAP

2) station_id (String) - The 4-letter airport station identifier. 
                         If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                        Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 

Optional Arguments:

1) low_rh_threshold (Integer) - Default = 15. The threshold for the contour line that defines what extremely low relative humidity is.

2) high_wind_threshold (Integer) - Default = 25. The threshold for the contour line that defines what high winds are.

3) temperature_threshold (Integer) - Default = None. This is to be used if the user wishes to add temperature as a factor to what 
   defines favorable fire weather conditions. When set to None, only RH & Wind Speed/Gust are taken 
   into account. When set to an integer value, the temperature will also be taken into account. 

4) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 

5) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 

6) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
    and passing the data in or if the function needs to download the data. A value of False means the data
    is downloaded inside of the function while a value of True means the user is downloading the data outside
    of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
    things, it is recommended to set this value to True and download the data outside of the function and pass
    it in so that the amount of data requests on the host servers can be minimized. 


7) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
    in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
    outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

8) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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

Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}









