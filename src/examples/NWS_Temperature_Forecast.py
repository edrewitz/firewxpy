'''
This is a sample program of how to create all the fire weather graphics surrounding maximum and minimum temperature from the National Weather Service NDFD gridded forecast data. 
This is the program the user will write using the FireWxPy package in Python. 
You can already see how the functions of FireWxPy significantly simplify the amount of coding the meteorologist will need to do in order to re-create these graphics. 
All of the data downloading, data parsing, calculations, bringing in the Predictive Services Areas boundaries etc. are done in the background and thus should significantly reduce the amount of coding on the part of the user. 
I will walk you through step by step of what this code does. 

Once the user "plays around" with the coordinates and figure sizes and color bar sizes and finds the settings they like, they can just automate this script via the Windows Task Scheduler or a Cron Job depending on the operating system the user has on their computer. 

Copyright (C) Meteorologist Eric J. Drewitz 
                      USDA/USFS
                         2023
'''

'''
Here, we need to import the required packages in order for the script to run. Due to the large amount of functions active in the background (i.e. data download, data parsing etc.) we only need to import these two packages and not need to worry about the rest. 
The needed packages are: 1) FireWxPy_Plots and 2) matplotlib.pyplot (commonly used as plt in code, hence the import matplotlib.pyplot as plt). 

'''

import FireWxPy_Plots as fpplots
import matplotlib.pyplot as plt

'''
The user also needs to define the directory name of where the data will be pulled from on the NOAA/NWS FTP Server. 
Not to worry, if you either have a typo or an invalid directory name, you will be prompted with an error message that has the list of all the proper directories in the proper syntax. 
I will also post them here to make sure you know what to put in. 
The directory names are broken down by region and they are as follows: 

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

In this example we will use the Pacific Southwest directory since I am stationed at the Southern California Geographic Area Coordination Center, meaning Southern California is the area I am forecasting for. 
If you are concerned about another area, using the list above change the directory_name to the directory you are interested in. 

'''

directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/'

'''
*** The main part of the code the user needs to edit and "play around with" is this section of code, the coordinates of the bounds of the plot, the first and second standard parallels, the figure size and the size of the color bar on the side of the image which is referred to as the color_table_shrink. 
We will explain step by step here. *** 


'''

'''
The first section is the boundaries of the plot which are to be entered as latitude/longitude coordinates in DECIMAL DEGREES (NOT DEGREES, MINUTES, SECONDS!). 

Negative longitude values correspond to longitude values in the WESTERN HEMISPHERE. Positive latitude values correspond to latitude values in the NORTHERN HEMISPHERE. Likewise, positive longitude is EASTERN HEMISPHERE and negative latitude is SOUTHERN HEMISPHERE. 

Choose latitude/longitude boundaries that cover the area you are interested in. In this example, we will focus in on Southern California as shown by the coordinates selected below. 

'''

western_bound = -122
eastern_bound = -114
southern_bound = 32
northern_bound = 39
central_latitude = 35
central_longitude = -118

'''
Since we are using Lambert Conformal projections, we need to define our first and second standard parallels. 

Standard parallel 1 and standard parallel 2 are used with conic projections to define the latitude lines where the scale is 1.0. When defining a Lambert conformal conic projection with one standard parallel, the first standard parallel defines the origin of the y-coordinates.

For more information on standard parallels, visit: https://wiki.gis.com/wiki/index.php/Standard_parallel#:~:text=Standard%20parallels%20are%20parallel%20lines,is%20only%20one%20standard%20parallel.

'''

first_standard_parallel = 30
second_standard_parallel = 60

'''
In this section, we determine the size of our figure. 
This is something users will need to "play around with" a little bit. 
Depending on how many GRIB files are availiable, there are likely to be different numbers of subplots in each figure. 
The number of GRIB files downloaded is dependent on which time the script runs and how many GRIB files are valid at the time the script runs. 

fig_x_length_1 corresponds to how big the figure size will be in the x-direction if there is only 1 subplot. 
fig_y_length_1 corresponds to how big the figure size will be in the y-direction if there is only 1 subplot.

fig_x_length_2 corresponds to how big the figure size will be in the x-direction if there are 2 subplots.
fig_y_length_2 corresponds to how big the figure size will be in the y-direction if there are 2 subplots.

fig_x_length_3 corresponds to how big the figure size will be in the x-direction if there are 3 subplots.
fig_y_length_3 corresponds to how big the figure size will be in the y-direction if there are 3 subplots.

fig_x_length_4 corresponds to how big the figure size will be in the x-direction if there are 4 subplots.
fig_y_length_4 corresponds to how big the figure size will be in the y-direction if there are 4 subplots.

fig_x_length_5 corresponds to how big the figure size will be in the x-direction if there are 5 subplots.
fig_y_length_5 corresponds to how big the figure size will be in the y-direction if there are 5 subplots.

'''

fig_x_length_1 = 10 
fig_y_length_1 = 10 
fig_x_length_2 = 9
fig_y_length_2 = 5
fig_x_length_3 = 15
fig_y_length_3 = 6
fig_x_length_4 = 12 
fig_y_length_4 = 10
fig_x_length_5 = 25
fig_y_length_5 = 5

'''
In this section called color_table_shrink we will be editing how big the colorbar will be on the size of the image. 
Depending on how many subplots there are or the size of the image, the size of the colorbar can come out sloppy. 
The good thing about FireWxPy is the plotting functions allow for the user to customize the size of the color bar so it fits best in the graphics they want to produce. 

color_table_shrink cannot be lower than 0. It is recommended to not set the color_table_shrink above 1. 
The closer to 0, the smaller the color bar and the closer to 1, the larger the colorbar. 
Depending on the figure size, number of subplots and how much area you are looking at on the map can all affect how the color bar appears. 
If the color bar is longer than the vertical length of the image, it is recommended to decrease the color_bar_shrink so that your end product appears to be nice and neat. 

'''

color_table_shrink = 0.7

'''
In this final section we use the FireWxPy plotting functions in FireWxPy_Plots that we imported at the beginning to create our graphics. 
It is recommended to use try and except blocks when automating your graphics. 
You can see the graphic we want to produce is in the try block and the graphic that is returned if there is no data is in the except block. 
This is how we prevent the program from crashing. 

The try block essentially tells the computer "try to do this" so in this case, try to create our relative humidity forecast graphics. 
Sometimes, there are issues with dataflow which are no fault of the user and that is why the except block is important, so in these events we can display a "no data" graphic for the time at which the script ran. This is also critically important for instances where there is data for some of the plots we want to create in this script but data is missing from other plots we would like to create in this script. 
These try and except blocks make the creation of these images independent from one another so if one fails, the script still runs rather than crashes and we can at least download and visualize the data that is currently available rather than have no data to help us with our forecast. 

This example, we save the completed images to one of two folders inside of a folder titled "Weather Data" if the script is plotting the data with respect to county and state borders, we save the images inside of a folder titled "National Weather Service Forecast Counties Perspective" inside of our Weather Data folder. 
Likewise, the images that are plotting the data with Predictive Services Areas (PSAs) as the reference point, the images save to a different folder titled "National Weather Service Forecast Predictive Services Areas Perspective" inside of our Weather Data folder. 


I hope these instructions helped you understand what this script does so you can use FireWxPy to help create your own weather graphics. 

'''

try:
    fig_NWS_Short_Term_Forecast_Frost_And_Freeze_Counties = fpplots.National_Weather_Service_Forecast_Counties_Perspective.CONUS.plot_frost_freeze_short_term_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Short_Term_Forecast_Frost_And_Freeze_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Short Term Forecast Frost and Freeze Areas")

except Exception as a:
    fig_NWS_Short_Term_Forecast_Frost_And_Freeze_Counties = fpplots.standard.no_data_graphic()
    fig_NWS_Short_Term_Forecast_Frost_And_Freeze_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Short Term Forecast Frost and Freeze Areas")


try:
    fig_NWS_Extended_Forecast_Frost_And_Freeze_Counties = fpplots.National_Weather_Service_Forecast_Counties_Perspective.CONUS.plot_frost_freeze_extended_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Extended_Forecast_Frost_And_Freeze_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Extended Forecast Frost and Freeze Areas")

except Exception as b:
    fig_NWS_Extended_Forecast_Frost_And_Freeze_Counties = fpplots.standard.no_data_graphic()
    fig_NWS_Extended_Forecast_Frost_And_Freeze_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Extended Forecast Frost and Freeze Areas")


try:
    fig_NWS_Short_Term_Forecast_Extreme_Heat_Counties = fpplots.National_Weather_Service_Forecast_Counties_Perspective.CONUS.plot_extreme_heat_short_term_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Short_Term_Forecast_Extreme_Heat_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Short Term Forecast Extreme Heat")

except Exception as c:
    fig_NWS_Short_Term_Forecast_Extreme_Heat_Counties = fpplots.standard.no_data_graphic()
    fig_NWS_Short_Term_Forecast_Extreme_Heat_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Short Term Forecast Extreme Heat")


try:
    fig_NWS_Extended_Forecast_Extreme_Heat_Counties = fpplots.National_Weather_Service_Forecast_Counties_Perspective.CONUS.plot_extreme_heat_extended_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Extended_Forecast_Extreme_Heat_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Extended Forecast Extreme Heat")

except Exception as d:
    fig_NWS_Extended_Forecast_Extreme_Heat_Counties = fpplots.standard.no_data_graphic()
    fig_NWS_Extended_Forecast_Extreme_Heat_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Extended Forecast Extreme Heat")


try:
    fig_NWS_Short_Term_Forecast_Maximum_Temperature_And_Trend_Counties = fpplots.National_Weather_Service_Forecast_Counties_Perspective.CONUS.plot_maximum_temperature_short_term_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Short_Term_Forecast_Maximum_Temperature_And_Trend_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Short Term Forecast Maximum Temperature and Trend")

except Exception as e:
    fig_NWS_Short_Term_Forecast_Maximum_Temperature_And_Trend_Counties = fpplots.standard.no_data_graphic()
    fig_NWS_Short_Term_Forecast_Maximum_Temperature_And_Trend_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Short Term Forecast Maximum Temperature and Trend")


try:
    fig_NWS_Extended_Forecast_Maximum_Temperature_And_Trend_Counties = fpplots.National_Weather_Service_Forecast_Counties_Perspective.CONUS.plot_maximum_temperature_extended_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Extended_Forecast_Maximum_Temperature_And_Trend_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Extended Forecast Maximum Temperature and Trend")

except Exception as f:
    fig_NWS_Extended_Forecast_Maximum_Temperature_And_Trend_Counties = fpplots.standard.no_data_graphic()
    fig_NWS_Extended_Forecast_Maximum_Temperature_And_Trend_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Extended Forecast Maximum Temperature and Trend")


try:
    fig_NWS_Short_Term_Forecast_Minimum_Temperature_And_Trend_Counties = fpplots.National_Weather_Service_Forecast_Counties_Perspective.CONUS.plot_minimum_temperature_short_term_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Short_Term_Forecast_Minimum_Temperature_And_Trend_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Short Term Forecast Minimum Temperature and Trend")

except Exception as g:
    fig_NWS_Short_Term_Forecast_Minimum_Temperature_And_Trend_Counties = fpplots.standard.no_data_graphic()
    fig_NWS_Short_Term_Forecast_Minimum_Temperature_And_Trend_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Short Term Forecast Minimum Temperature and Trend")


try:
    fig_NWS_Extended_Forecast_Minimum_Temperature_And_Trend_Counties = fpplots.National_Weather_Service_Forecast_Counties_Perspective.CONUS.plot_minimum_temperature_extended_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Extended_Forecast_Minimum_Temperature_And_Trend_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Extended Forecast Minimum Temperature and Trend")

except Exception as g:
    fig_NWS_Extended_Forecast_Minimum_Temperature_And_Trend_Counties = fpplots.standard.no_data_graphic()
    fig_NWS_Extended_Forecast_Minimum_Temperature_And_Trend_Counties = plt.savefig(f"Weather Data/National Weather Service Forecast Counties Perspective/National Weather Service Extended Forecast Minimum Temperature and Trend")


try:
    fig_NWS_Short_Term_Forecast_Frost_And_Freeze_PSAs = fpplots.National_Weather_Service_Forecast_Predictive_Services_Areas_Perspective.CONUS.plot_frost_freeze_short_term_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Short_Term_Forecast_Frost_And_Freeze_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Short Term Forecast Frost and Freeze Areas")

except Exception as i:
    fig_NWS_Short_Term_Forecast_Frost_And_Freeze_PSAs = fpplots.standard.no_data_graphic()
    fig_NWS_Short_Term_Forecast_Frost_And_Freeze_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Short Term Forecast Frost and Freeze Areas")


try:
    fig_NWS_Extended_Forecast_Frost_And_Freeze_PSAs = fpplots.National_Weather_Service_Forecast_Predictive_Services_Areas_Perspective.CONUS.plot_frost_freeze_extended_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Extended_Forecast_Frost_And_Freeze_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Extended Forecast Frost and Freeze Areas")

except Exception as j:
    fig_NWS_Extended_Forecast_Frost_And_Freeze_PSAs = fpplots.standard.no_data_graphic()
    fig_NWS_Extended_Forecast_Frost_And_Freeze_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Extended Forecast Frost and Freeze Areas")


try:
    fig_NWS_Short_Term_Forecast_Extreme_Heat_PSAs = fpplots.National_Weather_Service_Forecast_Predictive_Services_Areas_Perspective.CONUS.plot_extreme_heat_short_term_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Short_Term_Forecast_Extreme_Heat_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Short Term Forecast Extreme Heat")

except Exception as k:
    fig_NWS_Short_Term_Forecast_Extreme_Heat_PSAs = fpplots.standard.no_data_graphic()
    fig_NWS_Short_Term_Forecast_Extreme_Heat_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Short Term Forecast Extreme Heat")


try:
    fig_NWS_Extended_Forecast_Extreme_Heat_PSAs = fpplots.National_Weather_Service_Forecast_Predictive_Services_Areas_Perspective.CONUS.plot_extreme_heat_extended_forecast(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Extended_Forecast_Extreme_Heat_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Extended Forecast Extreme Heat")

except Exception as l:
    fig_NWS_Extended_Forecast_Extreme_Heat_PSAs = fpplots.standard.no_data_graphic()
    fig_NWS_Extended_Forecast_Extreme_Heat_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Extended Forecast Extreme Heat")


try:
    fig_NWS_Short_Term_Forecast_Maximum_Temperature_And_Trend_PSAs = fpplots.National_Weather_Service_Forecast_Predictive_Services_Areas_Perspective.CONUS.plot_maximum_temperature_short_term_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Short_Term_Forecast_Maximum_Temperature_And_Trend_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Short Term Forecast Maximum Temperature and Trend")

except Exception as m:
    fig_NWS_Short_Term_Forecast_Maximum_Temperature_And_Trend_PSAs = fpplots.standard.no_data_graphic()
    fig_NWS_Short_Term_Forecast_Maximum_Temperature_And_Trend_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Short Term Forecast Maximum Temperature and Trend")


try:
    fig_NWS_Extended_Forecast_Maximum_Temperature_And_Trend_PSAs = fpplots.National_Weather_Service_Forecast_Predictive_Services_Areas_Perspective.CONUS.plot_maximum_temperature_extended_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Extended_Forecast_Maximum_Temperature_And_Trend_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Extended Forecast Maximum Temperature and Trend")

except Exception as n:
    fig_NWS_Extended_Forecast_Maximum_Temperature_And_Trend_PSAs = fpplots.standard.no_data_graphic()
    fig_NWS_Extended_Forecast_Maximum_Temperature_And_Trend_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Extended Forecast Maximum Temperature and Trend")


try:
    fig_NWS_Short_Term_Forecast_Minimum_Temperature_And_Trend_PSAs = fpplots.National_Weather_Service_Forecast_Predictive_Services_Areas_Perspective.CONUS.plot_minimum_temperature_short_term_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Short_Term_Forecast_Minimum_Temperature_And_Trend_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Short Term Forecast Minimum Temperature and Trend")

except Exception as o:
    fig_NWS_Short_Term_Forecast_Minimum_Temperature_And_Trend_PSAs = fpplots.standard.no_data_graphic()
    fig_NWS_Short_Term_Forecast_Minimum_Temperature_And_Trend_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Short Term Forecast Minimum Temperature and Trend")


try:
    fig_NWS_Extended_Forecast_Minimum_Temperature_And_Trend_PSAs = fpplots.National_Weather_Service_Forecast_Predictive_Services_Areas_Perspective.CONUS.plot_minimum_temperature_extended_forecast_and_trends(directory_name, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length_1, fig_y_length_1, fig_x_length_2, fig_y_length_2, fig_x_length_3, fig_y_length_3, fig_x_length_4, fig_y_length_4, fig_x_length_5, fig_y_length_5, color_table_shrink)
    fig_NWS_Extended_Forecast_Minimum_Temperature_And_Trend_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Extended Forecast Minimum Temperature and Trend")

except Exception as p:
    fig_NWS_Extended_Forecast_Minimum_Temperature_And_Trend_PSAs = fpplots.standard.no_data_graphic()
    fig_NWS_Extended_Forecast_Minimum_Temperature_And_Trend_PSAs = plt.savefig(f"Weather Data/National Weather Service Forecast Predictive Services Areas Perspective/National Weather Service Extended Forecast Minimum Temperature and Trend")

