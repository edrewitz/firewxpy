# **Soundings**

### **Functions**
1) [plot_observed_sounding(station_id)](#plot_observed_soundingstation_id)
2) [plot_observed_sounding_custom_date_time(station_id, year, month, day, hour)](#plot_observed_sounding_custom_date_timestation_id-year-month-day-hour)
3) [plot_forecast_soundings(model, station_id)](#plot_forecast_soundingsmodel-station_id)

### plot_observed_sounding(station_id)

This function downloads the latest avaliable sounding data from the University of Wyoming and plots the upper-air profiles. 

Required Arguments: 

1) station_id (String) - The 3 or 4 letter station identifier for the upper-air site. 

Example: San Diego, CA will be entered as plot_observed_sounding('nkx')

Optional Arguments: None

Returns: Saves the upper-air profiles graphic to the Soundings folder. 

### plot_observed_sounding_custom_date_time(station_id, year, month, day, hour)

This function downloads the latest avaliable sounding data from the University of Wyoming and plots the upper-air profiles. 

Required Arguments: 

1) station_id (String) - The 3 or 4 letter station identifier for the upper-air site. 
Example: San Diego, CA will be entered as plot_observed_sounding('nkx')

2) year (Integer) - The four digit year (i.e. 2024)

3) month (Integer) - The one or two digit month. 

4) day (Integer) - The nth day of the month. 

5) hour (Integer) - The hour of the sounding in UTC. 

Optional Arguments: None

Returns: Saves the upper-air profiles graphic to the Soundings folder. 

### plot_forecast_soundings(model, station_id)

This function plots the vertical profile forecasts for a given point and shows the transport wind and precipitation forecast in the vicinity of the point. 

Required Arguments:

1) model (String) - This is the model the user must select. 
                       
     Here are the choices: 
     1) GFS0p25 - GFS 0.25x0.25 degree
     2) GFS0p25_1h - GFS 0.25x0.25 degree with 1 hour intervals
     3) GFS0p50 - GFS 0.5x0.5 degree
     4) GFS1p00 - GFS 1.0x1.0 degree
     5) NAM - North American Model
     6) NAM 1hr - North American Model with 1 hour intervals 
     7) RAP - RAP for the CONUS
     8) RAP 32 - 32km North American RAP

2) station_id (String) - The 4-letter airport station identifier. 
                         If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

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

    Returns: A set of forecast vertical profile graphics saved to f:Weather Data/Forecast Model Data/{model}/Soundings/{latitude}{lat_symbol}/{longitude}{lon_symbol}/{reference_system}
