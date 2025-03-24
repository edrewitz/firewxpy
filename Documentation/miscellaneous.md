# **Table of Contents**
1) [Data Access Module](#data-access-module)
2) [Standard Module](#standard-module)
3) [Dims Module](#dims-module)



## ***Data Access Module***

 **Classes**

 1) [model_data](#model_data)
 2) [RTMA](#rtma)
 3) [NDFD_GRIDS](#ndfd_grids)
 4) [obs](#obs)
 5) [FEMS](#fems)

 ### model_data 

This class hosts the functions that return forecast model data from various different sources.

 *Functions*

 1) [get_nomads_opendap_data()](#get_nomads_opendap_data)
 2) [get_hourly_rap_data_point_forecast()](#get_hourly_rap_data_point_forecast)
 3) [get_hourly_rap_data_area_forecast()](#get_hourly_rap_data_area_forecast)
 4) [get_nomads_opendap_data_point_forecast()](#get_nomads_opendap_data_point_forecast)
 5) [get_nomads_model_data_via_https()](#get_nomads_model_data_via_https)
 6) [msc_datamart_datasets()](#msc_datamart_datasets)

#### get_nomads_opendap_data()

This function retrieves the latest forecast model data from NCEP/NOMADS OPENDAP. 

Required Arguments:

1) model (String) - The forecast model that is being used. 

2) region (String) - The abbreviation for the region used. 

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

Optional Arguments: None

Returns: An xarray.data_array of the forecast model data. 

#### get_hourly_rap_data_point_forecast()

This function downloads and retrieves the latest data for the Rapid Refresh Model from the 
NCEP/NOMADS OPENDAP server. 

Required Arguments:

1) model (String) - The forecast model that is being used. 
   Choices 1) RAP 2) RAP 32 (32km Full North America)

2) station_id (String) - The ID for the ASOS station. If the user wishes to pick a custom point
   that is not an ASOS location, enter 'Custom' or 'custom' for the station_id. 

3) longitude (Integer or Float) - If the user is entering a custom location that is not an ASOS station location,
   enter the longitude value in this place in decimal degrees. If using an ASOS station location, enter None in this
   place. 

4) latitude (Integer or Float) - If the user is entering a custom location that is not an ASOS station location,
   enter the latitude value in this place in decimal degrees. If using an ASOS station location, enter None in this
   place. 

Optional Arguments: None

Returns: An xarray.data_array of the Rapid Refresh Model for the closest grid point to the specified location. 

#### get_hourly_rap_data_area_forecast()

This function retrieves the latest dataset for the hourly RAP model from the NOAA/NCEP/NOMADS server. 

1) model (String) - The forecast model that is being used. 
   Choices 1) RAP 2) RAP 32 (32km Full North America)

2) region (String) - The abbreviation for the region used. 

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

Optional Arguments: 

1) two_point_cross_section (Boolean) - Default = False. When downloading the data and intending to make a cross-section 
   between two points, set two_point_cross_section=True. 

Returns: An xarray.data_array of the forecast model data. 

#### get_nomads_opendap_data_point_forecast()

This function downloads and retrieves the latest data for the forecast model data from the 
NCEP/NOMADS OPENDAP server. 

Required Arguments:

1) model (String) - The forecast model that is being used. 

2) station_id (String) - The ID for the ASOS station. If the user wishes to pick a custom point
   that is not an ASOS location, enter 'Custom' or 'custom' for the station_id. 

3) longitude (Integer or Float) - If the user is entering a custom location that is not an ASOS station location,
   enter the longitude value in this place in decimal degrees. If using an ASOS station location, enter None in this
   place. 

4) latitude (Integer or Float) - If the user is entering a custom location that is not an ASOS station location,
   enter the latitude value in this place in decimal degrees. If using an ASOS station location, enter None in this
   place. 

Optional Arguments: None

Returns: An xarray.data_array of the forecast model data for the closest grid point to the specified location. 

#### get_nomads_model_data_via_https()

This function grabs the latest model data from the NOAA/NCEP/NOMADS HTTPS Server and returns it to the user. 

Required Arguments: 

1) model (String) - This is the model the user must select. 
                       
   Here are the choices: 
   1) GEFS0p25 ENS MEAN - GEFS 0.25x0.25 degree ensemble mean
   2) GEFS0p25 CHEM - GEFS 0.25x0.25 coarse and fine particulates
   3) GEFS0p50 CHEM - GEFS 0.5x0.5 coarse and fine particulates
   4) UKMET - UKMET model

2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                     To look at any state use the 2-letter abbreviation for the state in either all capitals
                     or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                     CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                     North America use either: NA, na, North America or north america. If the user wishes to use custom
                     boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                     the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                     'oscc' for South Ops. 

3) typeOfLevel (String) - This determines which parameters are available for the GEFS 0.25x0.25 Ensemble Mean. The choices are as
                          follows: 

                          1) surface
                          2) meanSea
                          3) depthBelowLandLayer
                          4) heightAboveGround
                          5) atmosphereSingleLayer
                          6) cloudCeiling
                          7) heightAboveGroundLayer
                          8) pressureFromGroundLayer

                          For both the UKMET and GEFS CHEM you can enter a value of None here. 

4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                             

7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                             custom boundaries. This should be set to None if the user wishes to use a pre-defined region.

Optional Arguments: 

1) get_u_and_v_wind_components (Boolean) - Default = False. When having the typeOfLevel set to 'heightAboveGround' there is an issue
                                           with retrieving the u and v wind components. You will see an error message. Fortunately, 
                                           in FireWxPy we fix that for you so you can disregard the errors. When setting this value to True
                                           you will also return lists of the u and v datasets. 

2) add_wind_gusts (Boolean) - Default = True. When having get_u_and_v_wind_components=True, you can opt to add an additional list to be 
                              returned which will have the wind gust dataset. 

Returns: Depending on the values you enter above determines how many lists of datasets are returned. 
         If the user does not use 'GEFS0p25 ENS MEAN' for the model of choice, a single list of the datasets are returned. 
         If the user uses 'GEFS0p25 ENS MEAN' and does not have typeOfLevel set to 'heightAboveGround', a single list of the datasets are returned. 
         If the user uses 'GEFS0p25 ENS MEAN' and does have typeOfLevel set to 'heightAboveGround' while get_u_and_v_wind_components=False, a single list of the datasets are returned. 
         If the user uses 'GEFS0p25 ENS MEAN' and does have typeOfLevel set to 'heightAboveGround' while get_u_and_v_wind_components=True and get_u_and_v_wind_components=False,
         a list of the 'heightAboveGround' datasets, u-wind datasets and v-wind datasets will be returned. 
         If the user uses 'GEFS0p25 ENS MEAN' and does have typeOfLevel set to 'heightAboveGround' while get_u_and_v_wind_components=True and get_u_and_v_wind_components=True,
         a list of the 'heightAboveGround' datasets, u-wind datasets, v-wind datasets and gust datasets will be returned.

#### msc_datamart_datasets()

This function retrieves the latest data from the Canadian RDPA

Required Arguments:

1) product (String) - The type of product: 1) 'RDPA 6hr' 2) 'RDPA 24hr'

Optional Arguments: None

Returns: An xarray.data_array of the latest RDPA data. 

### RTMA

This class hosts the active functions that download the 2.5km x 2.5km Real Time Mesoscale Analysis (RTMA) Data. 

This class hosts the functions the users will import and call if the users wish to download the data outside of the 
plotting function and pass the data into the plotting function.

This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

*Functions*

1) [get_rtma_datasets()](#get_rtma_datasets)

#### get_rtma_datasets()

This function retrieves the latest RTMA Dataset and the RTMA Dataset for 24-Hours prior to the current dataset for the user. 

Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

Required Arguments:

1) region (String) - The abbreviation for the region (state, GACC Region, CONUS, etc.)

2) Current Time in UTC

Returns: 

1) The latest 2.5km x 2.5km RTMA Dataset

2) 1) The 2.5km x 2.5km RTMA Dataset from 24-Hours prior to the current dataset

3) The time corresponding to the dataset

4) The time corresponding to the dataset from 24-Hours prior to the current dataset

### NDFD_GRIDS

This class hosts the active function that downloads the NOAA/NWS/NDFD Gridded Data. 

This class hosts the function the users will import and call if the users wish to download the data outside of the 
plotting function and pass the data into the plotting function.

This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

*Functions*

1) [get_ndfd_grids_xarray()](#get_ndfd_grids_xarray)

#### get_ndfd_grids_xarray()

This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

Required Arguments: 

1) directory_name (String) - The name of the directory (see FireWxPy documentation for directory paths)

2) parameter (String) - The parameter that the user wishes to download. (i.e. ds.maxt.bin for max temperature)

3) state (String) - The state or region being used. 

Returns: An xarray.data_array of the latest NWS/SPC Forecast data

*Directory List*

ALASKA: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/

CONUS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/

CENTRAL GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/

CENTRAL MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/

CENTRAL PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/

CENTRAL ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/

EASTERN GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/

GUAM: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/

HAWAII: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/

MID-ATLANTIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/

NORTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/

NORTHERN HEMISPHERE: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/

NORTH PACIFIC OCEAN: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/

NORTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/

NORTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/

OCEANIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/

PACIFIC NORTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/

PACIFIC SOUTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/

PUERTO RICO: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/

SOUTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/

SOUTHERN MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/

SOUTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/

SOUTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/

UPPER MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/

### obs

This class hosts functions to access observational data

*Functions*

1) [previous_day_weather_summary()](#previous_day_weather_summary)
2) [get_metar_data()](#get_metar_data)

#### previous_day_weather_summary()

This function retrieves the 24 hour observations for the previous day and returns the extreme maximum and minimum values as well as the times associated with those values.

Inputs:
       1) station_id (String) - The 4 letter station identifier for the observational site. 

Returns:
        1) Maximum Temperature (°F)
        2) The time the maximum temperature occurred
        3) Minimum Temperature (°F)
        4) The time the minimum temperature occurred
        5) Minimum Relative Humidity (%)
        6) The time the minimum relative humidity occurred
        7) Maximum Relative Humidity (%)
        8) The time the maximum relative humidity occurred
        9) Maximum Wind Speed (MPH)
        10) The time the maximum wind speed occurred
        11) Maximum Wind Gust (MPH)
        12) The time the maximum wind gust occurred 

#### get_metar_data()

This function downloads and returns the latest METAR data. 

Inputs: None 

Returns: 

1) df (Pandas DataFrame) - DataFrame of the latest METAR data

2) time (datetime) - The time of the latest METAR dataset

### FEMS

This class hosts functions to retrieve the latest fuels data from FEMS

*Functions*

1) [get_single_station_data()](#get_single_station_data)

#### get_single_station_data()

This function retrieves the dataframe for a single RAWS station in FEMS

Required Arguments:

1) station_id (Integer) - The WIMS or RAWS ID of the station. 

2) number_of_days (Integer or String) - How many days the user wants the summary for (90 for 90 days).
   If the user wants to use a custom date range enter 'Custom' or 'custom' in this field. 

Optional Arguments:

1) start_date (String) - Default = None. The start date if the user wants to define a custom period. Enter as a string
   in the following format 'YYYY-mm-dd'

2) end_date (String) - Default = None. The end date if the user wants to define a custom period. Enter as a string
   in the following format 'YYYY-mm-dd'

3) fuel_model (String) - Default = 'Y'. The fuel model being used. 
   Fuel Models List:

   Y - Timber
   X - Brush
   W - Grass/Shrub
   V - Grass
   Z - Slash

4) to_csv (Boolean) - Default = True. This will save the data into a CSV file and build a directory to hold the CSV files. 

Returns: A Pandas DataFrame of the NFDRS data from FEMS.            


## ***Standard Module***

***Functions***

1) [plot_creation_time()](#plot_creation_time)

#### plot_creation_time()

This function uses the datetime module to find the time at which the script ran. 

This can be used in many ways:

1) Timestamp for graphic in both local time and UTC
2) When downloading data with functions in the data_access module, this function is called to find 
the time which is passed into the data downloading functions in order for the latest data to be
downloaded. 

There are no variables to pass into this function. 

Returns: 

1) Current Local Time
2) Current UTC Time

## ***Dims Module***

***Functions***

1) [get_metar_mask(state, gacc_region, rtma_ws=False)](#get_metar_maskstate-gacc_region-rtma_wsfalse)

#### get_metar_mask(state, gacc_region, rtma_ws=False)

This function returns the METAR mask for a given state or GACC region. 

Required Arguments:

1) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
                            If the user wishes to make a graphic for the entire CONUS, there are 4 acceptable abbreviations: 'US' or 'us'
                            or 'USA' or 'usa'. Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
                            acceptable. Default setting is 'us'. If the user wishes to make a plot based on gacc_region, this value must be 
                            changed to None. 


2) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
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

  Optional Arguments:
  
  1) rtma_ws (Boolean) - Default = False. When set to False, the mask value returned is for when the user wants to create full station plots.
     When rtma_ws=True, the mask returned is for when the user is only plotting wind barbs of observed winds from the METAR observations rather than the full station plot.

Returns: The value of the mask applied to the METAR observations. This way station plots aren't cluttered over each other. 







