# **Table of Contents**
1) [Data Access Module](#data-access-module)
2) [Standard Module](#standard-module)
3) [Dims Module](#dims-module)



## ***Data Access Module***

 **Classes**
1) [RTMA_CONUS](#rtma_conus-class)
2) [NDFD_CONUS_Hawaii](#ndfd_conus_hawaii-class)
3) RTMA_Alaska
4) NDFD_Alaska
5) RTMA_Hawaii

### RTMA_CONUS Class

This class hosts the active functions that download the 2.5km x 2.5km Real Time Mesoscale Analysis (RTMA) Data. 

This class hosts the functions the users will import and call if the users wish to download the data outside of the 
plotting function and pass the data into the plotting function.

This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

***Functions***

1) [get_RTMA_dataset(current_time)](#get_rtma_datasetcurrent_time)
2) [get_RTMA_24_hour_comparison_datasets(current_time)](#get_rtma_24_hour_comparison_datasetscurrent_time)
3) [RTMA_Relative_Humidity_Synced_With_METAR(current_time, mask)](#rtma_relative_humidity_synced_with_metarcurrent_time-mask)
4) [RTMA_Synced_With_METAR(parameter, current_time, mask)](#get_current_rtma_datacurrent_time-parameter)
5) [get_current_rtma_data(current_time, parameter)](#get_current_rtma_datacurrent_time-parameter)

#### get_RTMA_dataset(current_time)

This function retrieves the latest RTMA Dataset for the user. 

Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

Required Argument: 1) Current Time in UTC (please see the [standard module](#standard-module) for more information on how to get the current time. 

Returns: 

1) The latest 2.5km x 2.5km RTMA Dataset

2) The time corresponding to the dataset


#### get_RTMA_24_hour_comparison_datasets(current_time)

This function retrieves the latest RTMA Dataset and the RTMA Dataset for 24-Hours prior to the current dataset for the user. 

Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

Required Argument: 1) Current Time in UTC (please see the [standard module](#standard-module) for more information on how to get the current time. 

Returns: 

1) The latest 2.5km x 2.5km RTMA Dataset

2) The 2.5km x 2.5km RTMA Dataset from 24-Hours prior to the current dataset

3) The time corresponding to the dataset

4) The time corresponding to the dataset from 24-Hours prior to the current dataset 


#### RTMA_Relative_Humidity_Synced_With_METAR(current_time, mask)

This function retrieves the latest RTMA Relative Humidity Dataset and METAR Dataset for the user. 

Data Source: UCAR/THREDDS (https://thredds.ucar.edu/)

Required Argument: 

1) Current Time in UTC (please see the [standard module](#standard-module) for more information on how to get the current time. 

2) (Mask) Minimum radius allowed between points. If units are not provided, meters is assumed (please see the [dims module](#dims-module) for more information on how to get the mask. 

Returns: A list of all the aformentioned data:

RTMA RH Data = data[0]

The time corresponding to the dataset = data[1]

Surface METAR Data = data[2]

METAR u-component of wind (kt) = data[3]

METAR v-component of wind (kt) = data[4]

METAR RH Data = data[5]

Mask (Minimum radius allowed between points) = data[6]

Time of METAR Observations = data[7]

Projection for the data = data[8]  

#### RTMA_Synced_With_METAR(parameter, current_time, mask)

This function is the recommended method to download the Real Time Mesoscale Analysis dataset with the METAR dataset as this function syncs the time of the
latest available Real Time Mesoscale Analysis dataset with the latest available complete METAR dataset. 

Inputs: 

1) parameter (String) - The weather parameter the user wishes to download. 
To find the full list of parameters, visit: https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/RTMA/CONUS_2p5km/Best.html

2) current_time (Datetime) - Current date and time in UTC (please see the [standard module](#standard-module) for more information on how to get the current time.  
3) mask (Integer) - Distance in meters to mask METAR stations apart from eachother so stations don't clutter the plot. The higher the value, the less stations are displayed
                     (please see the [dims module](#dims-module) for more information on how to get the mask  

Returns: 

1) rtma_data - The latest avaiable Real Time Mesoscale Analysis dataset
2) rtma_time - The time of the latest avaiable Real Time Mesoscale Analysis dataset
3) sfc_data - The entire METAR dataset. 
4) sfc_data_u_kt - The u-component (west-east) of the wind velocity in knots. 
5) sfc_data_v_kt - The v-component (north-south) of the wind velocity in knots. 
6) sfc_data_rh - The relative humidity in the METAR dataset. 
7) sfc_data_mask - Distance in meters to mask METAR stations apart from eachother so stations don't clutter the plot. The higher the value, the less stations are displayed.
8) metar_time_revised - The corrected time (if needed) for the latest complete METAR dataset. 
9) plot_projection - The coordinate reference system of the data being plotted. This is usually PlateCarree.

#### get_current_rtma_data(current_time, parameter)

This function retrieves the latest available 2.5km x 2.5km Real Time Mesoscale Analysis for any available parameter. 

Inputs:

1) current_time (Datetime) - Current time in UTC (please see the [standard module](#standard-module) for more information on how to get the current time.  
2) parameter (String) - The weather parameter the user wishes to download. 
To find the full list of parameters, visit: https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/RTMA/CONUS_2p5km/Best.html

Returns: 

1) If there are zero errors, the latest dataset and the time of the dataset for the requested parameter will be returned. 
2) If there is an error, an error message is returned. 

### NDFD_CONUS_Hawaii Class

This class hosts the active function that downloads the NOAA/NWS/NDFD Gridded Data for CONUS and Hawaii. 

This class hosts the function the users will import and call if the users wish to download the data outside of the 
plotting function and pass the data into the plotting function.

This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

***Functions***

1) [download_NDFD_grids(directory_name, parameter)](#download_ndfd_gridsdirectory_name-parameter)
2) [download_short_term_NDFD_grids(directory_name, parameter)](#download_short_term_ndfd_gridsdirectory_name-parameter)
3) [download_extended_NDFD_grids(directory_name, parameter)](#download_extended_ndfd_gridsdirectory_name-parameter)
4) [get_NWS_NDFD_7_Day_grid_data(directory_name, parameter)](#get_nws_ndfd_7_day_grid_datadirectory_name-parameter)

#### Directory Paths

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



#### download_NDFD_grids(directory_name, parameter)

This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

Scripts that download files from the CONUS directory are recommended to be run between the 48th and 15th 
minute to avoid the script idiling. The reason is because the files in the CONUS directory update between the 15th
and 48th minute of the hour (and downloading them during that time makes them extremely hard to work with!!). Due
to this, if there is an issue with the data, the program will automatically idle until the 48th minute and resume and try again to download the latest data. 

Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

Required Arguments: 

1) The name of the directory (see FireWxPy documentation for [directory paths](#directory-paths))

2) The parameter that the user wishes to download. (i.e. ds.maxt.bin for max temperature)

Returns: 

1) The files holding the forecast data in a GRIB2 format. 

2) An xarray data-array of the same forecast data. 

3) The count of the number of files in the short-term forecast period. 

4) The count of the number of files in the extended forecast period. 


#### download_short_term_NDFD_grids(directory_name, parameter)

This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

Scripts that download files from the CONUS directory are recommended to be run between the 48th and 15th 
minute to avoid the script idiling. The reason is because the files in the CONUS directory update between the 15th
and 48th minute of the hour (and downloading them during that time makes them extremely hard to work with!!). Due
to this, if there is an issue with the data, the program will automatically idle until the 48th minute and resume and try again to download the latest data. 

Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

Required Arguments: 

1) The name of the directory (see FireWxPy documentation for [directory paths](#directory-paths))

2) The parameter that the user wishes to download. (i.e. ds.maxt.bin for max temperature)

Returns: 

1) The files holding the forecast data in a GRIB2 format. 

2) An xarray data-array of the same forecast data. 

3) The count of the number of files in the short-term forecast period. 

4) The count of the number of files in the extended forecast period. 

#### download_extended_NDFD_grids(directory_name, parameter)

This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

Scripts that download files from the CONUS directory are recommended to be run between the 48th and 15th 
minute to avoid the script idiling. The reason is because the files in the CONUS directory update between the 15th
and 48th minute of the hour (and downloading them during that time makes them extremely hard to work with!!). Due
to this, if there is an issue with the data, the program will automatically idle until the 48th minute and resume and try again to download the latest data. 

Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

Required Arguments: 

1) The name of the directory (see FireWxPy documentation for [directory paths](#directory-paths))

2) The parameter that the user wishes to download. (i.e. ds.maxt.bin for max temperature)

Returns: 

1) The files holding the forecast data in a GRIB2 format. 

2) An xarray data-array of the same forecast data. 

3) The count of the number of files in the short-term forecast period. 

4) The count of the number of files in the extended forecast period.


#### get_NWS_NDFD_7_Day_grid_data(directory_name, parameter)

This function connects to the National Weather Service FTP Server and returns the forecast data for the parameter of interest in a GRIB2 file.
This function is specifically for downloading the entire National Weather Service Forecast (Days 1-7) Forecast grids. 

Inputs:
1) directory_name (String) - The directory name is the complete filepath on the National Weather Service FTP server. 
The directory determines the domain the forecast data is valid for. See [directory paths](#directory-paths) for more information on each proper path. 

2) parameter (String) - The parameter corresponds to the weather element the user is interested in (i.e. temperature, relative humidity, wind speed etc.)
Here is a link to the spreadsheet that contains all of the proper syntax for each parameter:
https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK

Returns: This function returns the National Weather Service NDFD gridded forecast data in a GRIB2 file for the entire forecast period (Days 1-7). 
This function may also return an error message for either: 

1) A bad file path (invalid directory_name)
2) An invalid parameter (if the spelling of the parameter syntax is incorrect)

### RTMA_Alaska Class

This class hosts the active functions that download the 2.5km x 2.5km Real Time Mesoscale Analysis (RTMA) Data for Alaska. 

This class hosts the functions the users will import and call if the users wish to download the data outside of the 
plotting function and pass the data into the plotting function.

This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

#### get_RTMA_dataset(current_time)

This function retrieves the latest RTMA Dataset for the user. 

Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

Required Argument: 1) Current Time in UTC

Returns: 

1) The latest 2.5km x 2.5km RTMA Dataset

2) The time corresponding to the dataset

#### get_RTMA_24_hour_comparison_datasets(current_time)

This function retrieves the latest RTMA Dataset and the RTMA Dataset for 24-Hours prior to the current dataset for the user for Alaska. 

Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

Required Argument: 1) Current Time in UTC

Returns: 

1) The latest 2.5km x 2.5km RTMA Dataset

2) 1) The 2.5km x 2.5km RTMA Dataset from 24-Hours prior to the current dataset

3) The time corresponding to the dataset

4) The time corresponding to the dataset from 24-Hours prior to the current dataset

### NDFD_Alaska Class

#### get_short_and_extended_grids(parameter)

This function connects to the National Weather Service FTP Server and returns the forecast data for the parameter of interest in a GRIB2 file.
This function is specifically for downloading the entire National Weather Service Forecast (Days 1-7) Forecast grids. 

Inputs:

1) parameter (String) - The parameter corresponds to the weather element the user is interested in (i.e. temperature, relative humidity, wind speed etc.)
                        Here is a link to the spreadsheet that contains all of the proper syntax for each parameter:
                        https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK

Returns: This function returns the National Weather Service NDFD gridded forecast data in a GRIB2 file for the entire forecast period (Days 1-7). 
     This function may also return an error message for either: 1) A bad file path (invalid directory_name) or 2) An invalid parameter (if the spelling of the parameter syntax is incorrect)


### RTMA_Hawaii Class

This class hosts the active functions that download the 2.5km x 2.5km Real Time Mesoscale Analysis (RTMA) Data for Hawaii. 

This class hosts the functions the users will import and call if the users wish to download the data outside of the 
plotting function and pass the data into the plotting function.

This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

#### get_RTMA_dataset(current_time)

This function retrieves the latest RTMA Dataset for the user. 

Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

Required Argument: 1) Current Time in UTC

Returns: 

1) The latest 2.5km x 2.5km RTMA Dataset

2) The time corresponding to the dataset

#### get_RTMA_24_hour_comparison_datasets(current_time)

This function retrieves the latest RTMA Dataset and the RTMA Dataset for 24-Hours prior to the current dataset for the user. 

Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

Required Argument: 1) Current Time in UTC

Returns: 

1) The latest 2.5km x 2.5km RTMA Dataset

2) 1) The 2.5km x 2.5km RTMA Dataset from 24-Hours prior to the current dataset

3) The time corresponding to the dataset

4) The time corresponding to the dataset from 24-Hours prior to the current dataset 


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







