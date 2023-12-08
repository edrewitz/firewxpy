# Welcome To FireWxPy

Thank you for choosing to use FireWxPy in your weather operations and/or research. The purpose of this package is to help fellow meteorologists create realtime data visualizations of weather data with an emphasis on fire weather. The goal of this project is to make creating these graphics with the least amount of work required for the user. These graphics are designed to be part of a script that is being automatically run via either a Cron Job or via the Windows Task Scheduler. These plots display National Weather Service forecast data as well as 2.5km x 2.5km Real Time Mesoscale Analysis data from the UCAR THREDDS server: https://www.unidata.ucar.edu/software/tds/

# The Role of the User

FireWxPy does at least 95% of the work for the user to create data visualizations of various types of weather analysis and forecast data. However, there is still plenty of customization for the users. 

Here is what the user will still be responsible for:

1. Importing the needed Python modules
2. Choosing the bounds for the plot in latitude/longitude coordinates. 
3. There is a function where the user can customize the title, colorscale, colorbar, figure size and weather parameter of a plot. 
4. There are also plenty of preset plots that the user will be able to call functions from the `FireWxPy_Plots` module.

# FireWxPy Modules

# Data Access Module

The `data_access` module hosts functions that retrieve data from the National Weather Service FTP Server and the UCAR THREDDS Server. 

**National Weather Service NDFD Data**
There are two things the user needs to know when using `FireWxPy` to download gridded data from the NWS FTP Server: 1) File Path 
2) Weather Element (i.e. Forecast Parameter)

**File Path List**
Here is the complete list of all the file paths for each region of the NWS NDFD gridded data:

CONUS aka "Lower-48"
r"""/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/"""



    
    
**Weather Element List**

Here is a link to the document that has the proper syntax for each Weather Element of the NWS NDFD gridded data: https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK

**Data Access Functions**

1. `get_NWS_NDFD_grid_data(directory_name, parameter)`









# Parser Module

The `parser` module hosts functions that parse through the various datasets within the downloaded files and returns organized data arrays to make plotting graphics easier. 








# FireWxPy_Plots Module

The `FireWxPy_Plots` module hosts a variety of different functions for the user to plot various types of real-time analysis and forecast weather data. 
