# **Table of Contents
1) [Data Access Module]
2) [Standard Module]
3) [Dims Module]



## ***Data Access Module***

## **Classes**
1) [RTMA_CONUS]
2) [NDFD_CONUS]

### RTMA_CONUS Class

This class hosts the active functions that download the 2.5km x 2.5km Real Time Mesoscale Analysis (RTMA) Data. 

This class hosts the functions the users will import and call if the users wish to download the data outside of the 
plotting function and pass the data into the plotting function.

This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

***Functions***

1) [get_RTMA_dataset(current_time)]
2) [get_RTMA_24_hour_comparison_datasets(current_time)]
3) [RTMA_Relative_Humidity_Synced_With_METAR(current_time, mask)]
4) [RTMA_Synced_With_METAR(parameter, current_time, mask)]
5) [get_current_rtma_data(current_time, parameter)]

#### get_RTMA_dataset(current_time)

This function retrieves the latest RTMA Dataset for the user. 

Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

Required Argument: 1) Current Time in UTC (please see the [standard module]() for more information on how to get the current time. 

Returns: 

1) The latest 2.5km x 2.5km RTMA Dataset

2) The time corresponding to the dataset


#### get_RTMA_24_hour_comparison_datasets(current_time)

This function retrieves the latest RTMA Dataset and the RTMA Dataset for 24-Hours prior to the current dataset for the user. 

Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

Required Argument: 1) Current Time in UTC (please see the [standard module]() for more information on how to get the current time. 

Returns: 

1) The latest 2.5km x 2.5km RTMA Dataset

2) The 2.5km x 2.5km RTMA Dataset from 24-Hours prior to the current dataset

3) The time corresponding to the dataset

4) The time corresponding to the dataset from 24-Hours prior to the current dataset 


#### RTMA_Relative_Humidity_Synced_With_METAR(current_time, mask)

This function retrieves the latest RTMA Relative Humidity Dataset and METAR Dataset for the user. 

Data Source: UCAR/THREDDS (https://thredds.ucar.edu/)

Required Argument: 

1) Current Time in UTC (please see the [standard module]() for more information on how to get the current time. 

2) (Mask) Minimum radius allowed between points. If units are not provided, meters is assumed (please see the [dims module]() for more information on how to get the mask. 

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

2) current_time (Datetime) - Current date and time in UTC (please see the [standard module]() for more information on how to get the current time.  
3) mask (Integer) - Distance in meters to mask METAR stations apart from eachother so stations don't clutter the plot. The higher the value, the less stations are displayed
                     (please see the [dims module]() for more information on how to get the mask  

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

1) current_time (Datetime) - Current time in UTC (please see the [standard module]() for more information on how to get the current time.  
2) parameter (String) - The weather parameter the user wishes to download. 
To find the full list of parameters, visit: https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/RTMA/CONUS_2p5km/Best.html

Returns: 

1) If there are zero errors, the latest dataset and the time of the dataset for the requested parameter will be returned. 
2) If there is an error, an error message is returned. 

### NDFD_CONUS Class

This class hosts the active function that downloads the NOAA/NWS/NDFD Gridded Data. 

This class hosts the function the users will import and call if the users wish to download the data outside of the 
plotting function and pass the data into the plotting function.

This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

***Functions***

1) 























