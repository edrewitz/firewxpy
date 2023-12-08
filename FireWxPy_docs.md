# **Welcome To FireWxPy**

Thank you for choosing to use FireWxPy in your weather operations and/or research. The purpose of this package is to help fellow meteorologists create realtime data visualizations of weather data with an emphasis on fire weather. The goal of this project is to make creating these graphics with the least amount of work required for the user. These graphics are designed to be part of a script that is being automatically run via either a Cron Job or via the Windows Task Scheduler. These plots display National Weather Service forecast data as well as 2.5km x 2.5km Real Time Mesoscale Analysis data from the UCAR THREDDS server: https://www.unidata.ucar.edu/software/tds/

# **The Role of the User**

FireWxPy does at least 95% of the work for the user to create data visualizations of various types of weather analysis and forecast data. However, there is still plenty of customization for the users. 

Here is what the user will still be responsible for:

1. Importing the needed Python modules
2. Choosing the bounds for the plot in latitude/longitude coordinates. 
3. There is a function where the user can customize the title, colorscale, colorbar, figure size and weather parameter of a plot. 
4. There are also plenty of preset plots that the user will be able to call functions from the `FireWxPy_Plots` module.

# **Table of Contents**

# Data Access Module

[Retrieving the NWS Days 1-3 NDFD Gridded Data](#1-retrieving-the-nws-days-1-3-ndfd-gridded-data)

[Retrieving the NWS Days 4-7 NDFD Gridded Data](#2-retrieving-the-nws-days-4-7-ndfd-gridded-data)


# **Data Access Module**

The `data_access` module hosts functions that retrieve data from the National Weather Service FTP Server and the UCAR THREDDS Server. 

# National Weather Service NDFD Data
There are two things the user needs to know when using `FireWxPy` to download gridded data from the NWS FTP Server: 1) File Path 
2) Weather Element (i.e. Forecast Parameter)

# File Path List

Here is the complete list of all the file paths for each region of the NWS NDFD gridded data:

CONUS aka "Lower-48"
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/
```

Alaska
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/
```

Central Great Lakes
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/
```

Central Mississippi Valley
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/
```

Central Plains 
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/
```

Central Rockies
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/
```

Eastern Great Lakes
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/
```

Guam
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/
```

Hawaii
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/
```

Mid-Atlantic
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/
```

Northeast
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/
```

Northern Hemisphere
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/
```

North Pacific Ocean
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/
```

Northern Plains
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/
```

Northern Rockies
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/
```

Oceanic
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/
```

Pacific Northwest 
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/
```

Pacific Southwest
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
```

Puerto Rico
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/
```

Southeast
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/
```

Southern Mississippi Valley 
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/
```

Southern Plains
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/
```

Southern Rockies
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/
```

Upper Mississippi Valley 
```
/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/
```
    
# Weather Element List

Here is a link to the document that has the proper syntax for each Weather Element of the NWS NDFD gridded data: https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK


# **Data Access Functions**

# 1. Retrieving the NWS Days 1-3 NDFD Gridded Data
  Function: `get_NWS_NDFD_short_term_grid_data(directory_name, parameter)`

The `get_NWS_NDFD_short_term_grid_data(directory_name, parameter)` is used to retrieve the NWS Forecast data for days 1-3, otherwise known as the short-term forecast period. In order for the function to work properly, the user is required to pass in **two** string values. 

1) The first string value `directory_name` is the path in the URL on the NWS FTP server website. Please see above for all the paths in the proper syntax. The user must end the url with a forward slash '/' in order for the function to work properly.
2) The second string value is the weather element (also known as the forecast `parameter`) the user wishes to download. Here is an example: If the user wants to download the maximum temperature grids, the user must pass a string value of `ds.maxt.bin` as that is the filename for the maximum temperature grids.

Here is an example of where all the different file names are. The filenames are the long list of string values that begin with ds. and end with .bin. Therefore, the maximum temperature grid filename is `ds.maxt.bin`. Please see the links under the Weather Element List section for documentation on what weather elements correspond to the different filenames. 
   ![NWS FTP Server](https://github.com/edrewitz/FireWxPy/assets/101157849/fd48f27d-6fc5-42ed-9df5-af432cd737fb)

# 2. Retrieving the NWS Days 4-7 NDFD Gridded Data
   Function: `get_NWS_NDFD_extended_grid_data(directory_name, parameter)`

The `get_NWS_NDFD_extended_grid_data(directory_name, parameter)` is used to retrieve the NWS Forecast data for days 4-7, otherwise known as the extended forecast period. In order for the function to work properly, the user is required to pass in **two** string values. 

1) The first string value `directory_name` is the path in the URL on the NWS FTP server website. Please see above for all the paths in the proper syntax. The user must end the url with a forward slash '/' in order for the function to work properly.
2) The second string value is the weather element (also known as the forecast `parameter`) the user wishes to download. Here is an example: If the user wants to download the maximum temperature grids, the user must pass a string value of `ds.maxt.bin` as that is the filename for the maximum temperature grids.

Here is an example of where all the different file names are. The filenames are the long list of string values that begin with ds. and end with .bin. Therefore, the maximum temperature grid filename is `ds.maxt.bin`. Please see the links under the Weather Element List section for documentation on what weather elements correspond to the different filenames. 
   ![NWS FTP Server](https://github.com/edrewitz/FireWxPy/assets/101157849/fd48f27d-6fc5-42ed-9df5-af432cd737fb)



   









# Parser Module

The `parser` module hosts functions that parse through the various datasets within the downloaded files and returns organized data arrays to make plotting graphics easier. 








# FireWxPy_Plots Module

The `FireWxPy_Plots` module hosts a variety of different functions for the user to plot various types of real-time analysis and forecast weather data. 
