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

 **Data Access Module**

[Retrieving the NWS Days 1-3 NDFD Gridded Data](#1-retrieving-the-nws-days-1-3-ndfd-gridded-data)

[Retrieving the NWS Days 4-7 NDFD Gridded Data](#2-retrieving-the-nws-days-4-7-ndfd-gridded-data)


# **Data Access Module**

The `data_access` module hosts functions that retrieve data from the National Weather Service FTP Server and the UCAR THREDDS Server. 

**National Weather Service NDFD Data**
There are two things the user needs to know when using `FireWxPy` to download gridded data from the NWS FTP Server: 1) File Path 
2) Weather Element (i.e. Forecast Parameter)

**File Path List**

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
    
**Weather Element List**

Here is a link to the document that has the proper syntax for each Weather Element of the NWS NDFD gridded data: https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK


# **Data Access Functions**

# 1. Retrieving the NWS Days 1-3 NDFD Gridded Data
  Function: `get_NWS_NDFD_short_term_grid_data(directory_name, parameter)`

This function is used to retrieve the NWS Forecast data for days 1-3, otherwise known as the short-term forecast period. In order for the function to work properly, the user is required to pass in **two** string values. 

1) The first string value `directory_name` is the path in the URL on the NWS FTP server website. Please see above for all the paths in the proper syntax. The user must end the url with a forward slash '/' in order for the function to work properly.
2) The second string value is the weather element (also known as the forecast `parameter`) the user wishes to download. Here is an example: If the user wants to download the maximum temperature grids, the user must pass a string value of `ds.maxt.bin` as that is the filename for the maximum temperature grids.

Here is an example of where all the different file names are. The filenames are the long list of string values that begin with ds. and end with .bin. Therefore, the maximum temperature grid filename is `ds.maxt.bin`. Please see the links under the Weather Element List section for documentation on what weather elements correspond to the different filenames. 
   ![NWS FTP Server](https://github.com/edrewitz/FireWxPy/assets/101157849/fd48f27d-6fc5-42ed-9df5-af432cd737fb)

# 2. Retrieving the NWS Days 4-7 NDFD Gridded Data
   Function: `get_NWS_NDFD_extended_grid_data(directory_name, parameter)`

This function is used to retrieve the NWS Forecast data for days 4-7, otherwise known as the extended forecast period. In order for the function to work properly, the user is required to pass in **two** string values. 

1) The first string value `directory_name` is the path in the URL on the NWS FTP server website. Please see above for all the paths in the proper syntax. The user must end the url with a forward slash '/' in order for the function to work properly.
2) The second string value is the weather element (also known as the forecast `parameter`) the user wishes to download. Here is an example: If the user wants to download the maximum temperature grids, the user must pass a string value of `ds.maxt.bin` as that is the filename for the maximum temperature grids.

Here is an example of where all the different file names are. The filenames are the long list of string values that begin with ds. and end with .bin. Therefore, the maximum temperature grid filename is `ds.maxt.bin`. Please see the links under the Weather Element List section for documentation on what weather elements correspond to the different filenames. 
   ![NWS FTP Server](https://github.com/edrewitz/FireWxPy/assets/101157849/fd48f27d-6fc5-42ed-9df5-af432cd737fb)



   









# Parser Module

The `parser` module hosts functions that parse through the various datasets within the downloaded files and returns organized data arrays to make plotting graphics easier. 

**Classes:**

**save**

The `save` class hosts functions that: 1) extract figures from a figure list and saves them to a specified location, 2) Create animated GIF images from the still images in a specified file location. 

1) Function: `extract_NWS_NDFD_figures(figure_list, file_count, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5)`

This function extracts indivdual figures from a list of figures and saves them with a specified file path. 
        *This function is only to be used for the National Weather Service NDFD graphics.* 

        Inputs: 1) figure_list (List) - List of figures returned by the plotting function. 
                2) file_count (Integer) - Count of files returned by the plotting function. 
                3) file_path_1 (String) - Path to where the first figure is saved. 
                4) file_path_2 (String) - Path to where the second figure is saved. 
                5) file_path_3 (String) - Path to where the third figure is saved. 
                6) file_path_4 (String) - Path to where the fourth figure is saved. 
                7) file_path_5 (String) - Path to where the fifth figure is saved. 

        Return: Each figure in the list is saved as its own file to a specified file path


2) Function: `extract_SPC_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6)'

   This function extracts indivdual figures from a list of figures and saves them with a specified file path. 
        *This function is only to be used for the SPC Critical Fire Weather Outlook and/or Dry Lightning Outlook Graphics.* 

        Inputs: 1) figure_list (List) - List of figures returned by the plotting function. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.

        Return: Each figure in the list is saved as its own file to a specified file path

3) Function: `make_SPC_Outlook_GIF(GIF_Image_file_path, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, file_path_8, fps)`

   This function makes an animated GIF images of the SPC Outlooks and saves the GIF to a specified location.
       *This function is only to be used for the SPC Critical Fire Weather Outlook and/or Dry Lightning Outlook Graphics.*  

        Inputs: 1) GIF_Image_file_path (String) - The path to where the GIF image saves to plus the filename of the GIF image. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.
                8) file_path_7 (String) - Path to where the seventh figure is saved.
                9) file_path_8 (String) - Path to where the eigth figure is saved.
                10) fps (Integer) - The rate in frames per second the GIF loops. 

        Return: An animated GIF of the latest SPC Critical Fire Weather and/or Dry Lightning Outlook

4) Function: `extract_RTMA_figures_6hr_timelapse(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)`
  
      This function extracts indivdual figures from a list of figures and saves them with a specified file path. 
        *This function is only to be used for the Real Time Mesoscale Analysis Graphics.* 

        This function extracts indivdual figures from a list of figures and saves them with a specified file path. 
        *This function is only to be used for the Real Time Mesoscale Analysis Graphics.* 

        Inputs: 1) figure_list (List) - List of figures returned by the plotting function. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.
                8) file_path_7 (String) - Path to where the seventh figure is saved.

        Return: Each figure in the list is saved as its own file to a specified file path

5) Function: `make_RTMA_6hr_timelapse_GIF(GIF_Image_file_path, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, fps)`

      This function makes an animated GIF images of the SPC Outlooks and saves the GIF to a specified location.
        *This function is only to be used for the Real Time Mesoscale Analysis Graphics.*

        Inputs: 1) GIF_Image_file_path (String) - The path to where the GIF image saves to plus the filename of the GIF image. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.
                8) file_path_7 (String) - Path to where the seventh figure is saved.
                9) fps (Integer) - The rate in frames per second the GIF loops. 

        Return: An animated 6hr timelapse GIF image of the RTMA plots

# Real_Time_Mesoscale_Analysis_Graphics_CONUS Module

The Real_Time_Mesoscale_Analysis_Graphics_CONUS` module hosts a variety of different functions for the user to plot various types of real-time analysis for the Continental US aka "The Lower-48."

**Classes:**

1) `Counties_Perspective`: Uses state and county boundaries as the geographical reference system.
2) `Predictive_Services_Areas_Perspective`: Uses Geographic Area Coordination Center (GACC) and Predictive Services Areas (PSAs) as the geographical reference system.

**Counties_Perspective**

1) Function: `plot_generic_real_time_mesoanalysis_no_METARs(parameter, plot_title, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, state_border_color, state_border_line_thickness, county_border_color, county_border_line_thickness, signature_x_position, signature_y_position, title_font_size, signature_font_size, colorbar_label_font_size, colorbar_pad, show_rivers, state_border_linewidth, county_border_linewidth)`

            This function does the following:
                                            1) Downloads the data that corresponds to the parameter the user requests. 
                                            2) Converts the units of the data (if needed).
                                            3) Plots the data that corresponds to the parameter the user requests. 

            

            Inputs:
                1) parameter (String) - The parameter the user chooses to plot. For the full parameter list, visit: https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/NDFD/NWS/CONUS/CONDUIT/Best.html

                2) plot_title (String) - The title of the entire figure. 

                3) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                4) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                5) color_table (String) - The color table used for the scale of the data being plotted. See either the FireWxPy and/or matplotlib colortable documentation for colortable options. 

                6) color_table_title (String) - The title along the colorbar on the edge of the figure. 

                7) color_table_start (Integer) - The bottom bound of the color scale reference used to plot the data. 

                8) color_table_stop (Integer) - The top bound of the color scale reference used to plot the data.

                9) color_table_step (Integer) - The increment of the color scale (i.e. every 1 degree vs. every 5 degrees). 

                10) color_table_shrink (Integer or Float) - The size of the color bar with respect to the size of the figure. Generally this ranges between 0 and 1. Values closer to 0 correspond to shrinking the size of the color bar while larger values correspond to increasing the size of the color bar. 

                11) state_border_color (String) - Color of the state border. 

                12) state_border_line_thickness (Integer or Float) - Thickness of the state border lines. 

                13) county_border_color (String) - Color of the county border. 

                14) county_border_line_thickness (Integer or Float) - Thickness of the county border lines.

                15) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                16) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                17) title_font_size (Integer) - The fontsize of the title of the figure. 

                18) signature_font_size (Integer) - The fontsize of the signature of the figure. 

                19) colorbar_label_font_size (Integer) - The fontsize of the title of the colorbar of the figure. 

                20) colorbar_pad (Float) - This determines how close the position of the colorbar is to the edge of the subplot of the figure. 
                                           Default setting is 0.05.
                                           Lower numbers mean the colorbar is closer to the edge of the subplot while larger numbers allows for more space between the edge of the subplot and the colorbar.
                                           Example: If colorbar_pad = 0.00, then the colorbar is right up against the edge of the subplot. 

                21) show_rivers (Boolean) - If set to True, rivers will display on the map. If set to False, rivers 
                                            will not display on the map. 


            Returns:
                    1) A figure of the plotted 2.5km x 2.5km Real Time Mesoscale Analysis for the parameter the user wishes to plot. 
