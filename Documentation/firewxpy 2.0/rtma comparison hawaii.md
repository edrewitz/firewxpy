# Real Time Mesoscale Analysis Comparison Hawaii

These functions plot the Real Time Mesoscale Analysis Comparison for Hawaii.

- FireWxPy >= 2.0 Brings much new customization to each set of graphics where everything is customizable.
- FireWxPy >= 2.0 Uses the WxData and Shapeography packages as a back-end for automating these graphics.
- FireWxPy >= 2.0 Works for users on VPN/PROXY connections as a result of the WxData and Shapeography packages.

Functions
---------

1) [`plot_temperature`]()
2) [`plot_dew_point`]()
3) [`plot_dew_point_depression`]()
4) [`plot_relative_humidity`]()
5) [`plot_wind_speed`]()
6) [`plot_wind_gust`]()
7) [`plot_temperature_and_wind`]()
8) [`plot_temperature_and_gust`]()
9) [`plot_relative_humidity_and_wind`]()
10) [`plot_relative_humidity_and_gust`]()
11) [`plot_dew_point_depression_and_wind`]()
12) [`plot_dew_point_depression_and_gust`]()
13) [`plot_dew_point_and_wind`]()
14) [`plot_dew_point_and_gust`]()

Arguments and Settings
----------------------

- region (String) - Default='hi'. The region of the plot. Use the 2-letter state abbreviation or 4-letter GACC abbreviation.
        If the user wants a completely custom region where they define their own lat/lon bounds, set region='custom'. 
        
- hours (Integer) - Default=24. The amount of hours between the current and comparison. Defaults to a 24 hour
        comparison. 
        
- show_states (Boolean) - Default=True. When set to True, U.S. state borders are shown. 
    
- state_border_color (String) - Default='black'. The color of the U.S. state borders.
    
- state_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the U.S. state borders.
    
- state_border_zorder (Integer) - Default=3. The z-order of the state borders. For state borders to be displayed
        the following condition must be met: state_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
        
- show_counties (Boolean) - Default=True. When set to True, U.S. county borders are shown. 
    
- county_border_color (String) - Default='black'. The color of the U.S. county borders.
    
- county_border_linewidth (Float or Integer) - Default=0.25. The linewidth of the U.S. county borders.
    
- county_border_zorder (Integer) - Default=3. The z-order of the county borders. For county borders to be displayed
        the following condition must be met: county_border_zorder > contourf_zorder. To bring forward, increase the zorder
        to send back decrease the zorder. 
    
- show_gacc_boundaries (Boolean) - Default=False. When set to True, Geographic Area Coordination Center borders are shown. 
    
- gacc_border_color (String) - Default='black'. The color of the Geographic Area Coordination Center borders.
    
- gacc_border_linewidth (Float or Integer) - Default=0.5. The linewidth of the Geographic Area Coordination Center borders.
    
- gacc_border_zorder (Integer) - Default=3. The z-order of the Geographic Area Coordination Center borders. 
       For Geographic Area Coordination Center borders to be displayed the following condition must be met: gacc_border_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
       
- show_predictive_services_areas (Boolean) - Default=False. When set to True, Predictive Services Areas borders are shown. 
    
- predictive_services_areas_color (String) - Default='black'. The color of the Predictive Services Areas borders.
    
- predictive_services_areas_linewidth (Float or Integer) - Default=0.25. The linewidth of the Predictive Services Areas borders.
    
- predictive_services_areas_zorder (Integer) - Default=3. The z-order of the Predictive Services Areas borders. 
       For Predictive Services Areas borders to be displayed the following condition must be met: predictive_services_areas_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
- show_nws_public_zones (Boolean) - Default=False. When set to True, NWS Public Zone borders are shown. 
    
- nws_public_zones_color (String) - Default='black'. The color of the NWS Public Zone borders.
    
- nws_public_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Public Zone borders.
    
- nws_public_zones_zorder (Integer) - Default=3. The z-order of the NWS Public Zone borders. 
       For NWS Public Zone borders to be displayed the following condition must be met: nws_public_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder. 
    
- show_nws_fire_weather_zones (Boolean) - Default=False. When set to True, NWS Fire Weather Zone borders are shown. 
    
- nws_fire_weather_zones_color (String) - Default='black'. The color of the NWS Fire Weather Zone borders.
    
- nws_fire_weather_zones_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS Fire Weather Zone borders.
    
- nws_fire_weather_zones_zorder (Integer) - Default=3. The z-order of the NWS Fire Weather Zone borders. 
       For NWS Fire Weather Zone borders to be displayed the following condition must be met: nws_fire_weather_zones_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
- show_nws_cwa (Boolean) - Default=False. When set to True, NWS CWA borders are shown.
    
- nws_cwa_color (String) - Default='black'. The color of the NWS CWA borders.
    
- nws_cwa_linewidth (Float or Integer) - Default=0.25. The linewidth of the NWS CWA borders.
    
- nws_cwa_zorder (Integer) - Default=3. The z-order of the NWS CWA borders. 
       For NWS CWA borders to be displayed the following condition must be met: nws_cwa_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.
    
- show_calfire_boundaries (Boolean) - Default=False. When set to True, CalFire borders are shown.
    
- calfire_boundary_color (String) - Default='black'. The color of the CalFire borders.
    
- calfire_boundary_linewidth (Float or Integer) - Default=0.25. The linewidth of the CalFire borders.
    
- calfire_boundary_zorder (Integer) - Default=3. The z-order of the CalFire borders. 
       For CalFire borders to be displayed the following condition must be met: calfire_boundary_zorder > contourf_zorder. 
       To bring forward, increase the zorder. To send back decrease the zorder.

- custom_shapefile_url (String or None) - Default=None. If the user wishes to set up an automation importing geometry from a shapefile that
        is not in the base version of FireWxPy, this is how to do that. The user will pass the download URL as a string by setting
        custom_shapefile_url='https"//shapefile_download_url.file_extension'. 
        
- custom_shapefile_file_extension (String) - Default='.zip'. This is the file extension of the zipped shapefile folder on the web
        server. 
        
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
- custom_shapefile_color (String) - Default='black'. The color of the borders in the custom shapefile.
    
- custom_shapefile_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders in the custom shapefile.
    
- custom_shapefile_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- custom_geojson_url (String) - Default=None. If the user wishes to set up an automation with a publicly available
        geojson on the web, pass in the full download URL into this argument.
    
- custom_geojson_filename (String) - Default=None. The filename of the custom geojson file. 
    
- custom_geojson_folder_name (String) Default='Custom GeoJSON'. The folder where the custom geojson will be saved in.
    
- custom_geojson_color (String) - Default='black'. The edge color of the geometries in the custom geojson file.
    
- custom_geojson_linewidth (Integer or Float) - Default=0.5. The linewidth of the borders in the custom geojson. 
    
- custom_geojson_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- custom_shapefile_local_path (String) - Default=None. The path to a shapefile locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
- custom_shapefile_local_color (String) - Default='black'. The edge color of the geometries in the shapefile.
    
- custom_shapefile_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
- custom_shapefile_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- custom_geojson_local_path (String) - Default=None. The path to a geojson locally hosted on the PC. This is useful
        for those who want to use proprietary (data is private and not publicly available) shapefiles locally on their PC. Users
        can link the full path to the shapefile and overlay the geometries from that shapefile. 
        
- custom_geojson_local_color (String) - Default='black'. The edge color of the geometries in the geojson.
    
- custom_geojson_local_linewidth (Float or Integer) - Default=0.5. The linewidth of the borders. 
    
- custom_geojson_local_zorder (Integer) - Default=3. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- convert_custom_shapefile_crs (Boolean)- Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom shapefile. 
        
- convert_local_custom_shapefile_crs (Boolean) - Default=False. Set to True if the user needs to change their coordinate reference system
        of the geometries in the custom geojson.
        
- refresh_cartographic_files (Boolean) - Default=True. Users that have automated pipelines set up for shapefiles. Having this set to
        True allows the client to delete and re-download the shapefiles with each run of the script. This is useful for shapefiles
        that have frequent geometry updates.
        
- reference_system (String) - Default='States & Counties'. The name of the borders overlaid onto the map.
    
- show_rivers (Boolean) - Default=False. Set to True to display rivers. 
    
- rivers_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- rivers_color (String) - Default='lightcyan'. The color of the river. 
    
- figure_x_length (Integer) - Default=12. The length of the figure in the x-direction.
    
- figure_y_length (Integer) - Default=12. The length of the figure in the y-direction.
    
- coastline_linewidth (Float or Integer) - Default=0.75. The linewidth of the coastline.
    
- land_color (String) - Default='beige'. The color of the land on a map.
    
- ocean_color (String) - Default='lightcyan'. The color of the ocean on a map.
    
- lakes_color (String) - Default='lightcyan'. The color of lakes on a map. 

- costline_zorder (Integer) - Default=9. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- ocean_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
- lakes_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
    
- land_zorder (Integer) - Default=1. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- decimate (Integer) - Default=150. This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. When set to 50, every 50 values will be queried. Use
        larger numbers for larger areas and smaller values for smaller areas. The default of 50 represents the setting for
        CONUS. 
        
- start (Integer) - The start of the filled contour range.
    
- stop (Integer) - The end of the filled contour range. 
    
- step (Integer) - Default=1. The interval of the filled contours.
    
- facecolor (String) - Default='aliceblue'. The background color of the graphic. 
    
- primary_title_text (String) - Default='RTMA 2-METER TEMPERATURE [°F] & 10-METER WIND [MPH]'. The primary title
        of the graphic. 
        
- primary_title_textbox_color (String) - Default='wheat'. The color of the textbox of the primary title.
    
- primary_title_textbox_style (String) - Default='round'. The style of the textbox of the primary title.
    
- primary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
- secondary_title_textbox_color (Float or Integer) Default='wheat'. The color of the textbox of the secondary title.
        
- secondary_title_textbox_style (String) - Default='round'. The style of the textbox of the secondary title.
    
- secondary_title_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
- primary_title_fontsize (Integer) - Default=12. Fontsize of the primary title text.
    
- secondary_title_fontsize (Integer) Default=10. Fontsize of the secondary title text.
    
- local_time (Boolean) - Default=True. Set to False for UTC time.
    
- signature_textbox_color (String) - Default='wheat'. The color of the textbox of the graphic's signature.
    
- signature_textbox_style (String) - Default='round'. The style of the textbox of the graphic's signature.
    
- signature_textbox_alpha (Float or Integer) - Default=1. A value between 0.5 and 1 representing transparency.

- signature_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- signature_fontsize (Integer) - Default=8. Fontsize of the graphic's signature text.
    
- signature_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the signature text box.
    
- signature_textbox_y_position (Float) - Default=-0.175. The y-position with respect to the plot axis of the signature text box.
    
- signature_text_new_lines (Boolean) - Default=False. When set to True, each section in the signature is on a new line.
        It is recommended to set this to True on plots that are longer from North to South than West to East. 
        
- reference_system_textbox_color (String) - Default='wheat'. The color of the textbox of the reference system.
    
- reference_system_textbox_style (String) - Default='round'. The style of the textbox of the reference system.
    
- reference_system_textbox_alpha (Float or Integer) - Default=1. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
- reference_system_textbox_zorder (Integer) - Default=10. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- reference_system_fontsize (Integer) - Default=6. Fontsize of the reference system label text.
    
- reference_system_textbox_x_position (Float) - Default=0.01. The x-position with respect to the plot axis of the reference system text box.
    
- reference_system_textbox_y_position (Float) - Default=0. The y-position with respect to the plot axis of the reference system text box.

- colorbar_shrink (Float or Integer) - Default=1. Fraction by which to multiply the size of the colorbar.
    
- colorbar_pad (Float) - Default=0.01. Fraction of original Axes between colorbar and new image Axes.
    
- tick_label_fontsize (Integer) - Default=9. The fontsize of the colorbar tick labels.
    
- colorbar_location (String) - Default='bottom'. The side of the plot axis where the colorbar will be displayed.
    
- colorbar_interval (Integer) - Default=10. The interval of tick marks on the colorbar.
    
- colorbar_aspect (Integer) - Default=50. Ratio of long to short dimensions.
    
- colormap (String) - Default='custom'. The Matplotlib colormap for filled contours being used OR set to 'custom' to create your own 
        custom colormapping. See the optional colors argument documentation (109) for more information on how to pass
        in a custom array of colors. 
        
- contourf_alpha (Float or Integer) - Default=0.5. A value between 0 and 1 representing transparency.
        0 = completely transparent, 1 = completely opaque
        
- contourf_zorder (Integer) - Default=2. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- colors (String List) - Example (Temperature Custom Colormap): colors=['purple',
                                                                        'darkblue',
                                                                        'dodgerblue',
                                                                        'white',
                                                                        'crimson',
                                                                        'darkred',
                                                                        'violet']
                                        
            The array of colors being used when colormap='custom'. 
            
- ds1 (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds1=ds1. This is the current time dataset. 
        
- ds2 (xarray.array or None) - Default=None. If the user is downloading, processing and plotting the data within the function,
        keep this set as None. If the user wishes to create a medley of plots it is recommended to download the data outside of this
        function and pass in the data by setting ds2=ds2. This is the comparison dataset.  
            
- western_bound (Float or Integer) - Default=-125. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
- eastern_bound (Float or Integer) - Default=-65. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
- southern_bound (Float or Integer) - Default=20. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
- northern_bound (Float or Integer) - Default=50. When region is set to 'custom' the user defines the bounds of the plot in 
        latitude and longitude coordinates.
        
- pixel_query_value_fontsize (Integer) - Default=4. The fontsize of the pixel query values.
    
- pixel_query_value_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- pixel_query_value_foreground (String) - Default='white'. The color of the foreground on the station plot (pixel query value).
    
- pixel_query_value_fontcolor (String) - Default='black'. The font color of the pixel query values.
    
- pixel_query_stroke_linewidth (Float or Integer) - Default=1. The linewidth of the pixel query values text outline.
    
- path (String) - Default='FireWxPy Graphics/RTMA/Temperature'. The directory where the graphic will save.
    
- filename (String) - Default='RTMA Temperature and Wind.png'. The filename of the image.
    
- proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }

- clear_recycle_bin (Boolean) - Default=False, When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
        
- clear_data (Boolean) - Default=True. When set to True, the data will be cleared with each run of the script.
        Set to False when downloading the data outside of the function and passing the data in. 
        
- chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB data to a file.
    
- notifications (String) - Default='off'. Notifications throughout the process. 

- custom_data_directory (String or None) - Default=None. The directory path where the data will be saved to. 

- mapcrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the map.
    
- datacrs (Cartopy.crs) - Default=ccrs.PlateCarree(). The coordinate reference system of the data.

- temperature_var_key (String) - Default='2m_temperature'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
- wind_speed_var_key (String) - Default='10m_wind_speed'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
- u_var_key (String) - Default='10m_u_wind_component'. The variable key name of the u-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
- v_var_key (String) - Default='10m_v_wind_component'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
- wind_direction_var_key (String) - Default='10m_wind_direction'. The variable key name of the v-wind parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
- time_coord_key (String) - Default='time'. The time coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
- longitude_key (String) - Default='longitude'. The longitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
    
- latitude_key (String) - Default='latitude'. The latitude coordinate key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
- dwpt_var_key (String) - Default='2m_dew_point'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        This is for
        
- dd_var_key (String) - Default='2m_dew_point_depression'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
- rh_var_key (String) - Default='2m_relative_humidity'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
- wind_gust_var_key (String) - Default='10m_wind_gust'. The variable key name of the parameter being plotted.
        You can ignore this if you are either 1) downloading, processing and plotting the data within the function or 2) Using
        WxData to download and process the data in your script before you pass the data into this function.
        
- onvert_wind_speed (Boolean) - Default=True. Convert wind speed from m/s to either mph or kts.
    
- convert_to (String) - Default='mph'. Set to 'kts' for knots.
    
- pixel_query_type (String) - Default='barbs'. Display either wind barbs or numerical values.
    
- barb_length (Float or Integer) - Default=2. Length of wind barb.
    
- barb_width (Float or Integer) - Default=0.25. Width of wind barb. 
    
- barb_color (String) - Default='black'. Color of wind barb. 
    
- barb_zorder (Integer) - Default=7. The z-order of the borders on the image. Lower numbers send this to the back
        higher numbers bring this forward.
        
- temp_value_loc (String) - Default='NW'. The location of temperature on the station plot in the form of compass directions.
    
- speed_value_loc (String) - Default='NE'. The location of wind speed on the station plot in the form of compass directions.

- gust_value_loc (String) - Default='NE'. The location of wind gust on the station plot in the form of compass directions.

- dwpt_value_loc (String) - Default='NW'. The location of dew point on the station plot in the form of compass directions.

- rh_value_loc (String) - Default='NW'. The location of relative humidity on the station plot in the form of compass directions.

- dd_value_loc (String) - Default='NW'. The location of dew point depression on the station plot in the form of compass directions.

- dwpt_value_loc (String) - Default='NW'. The location of dew point on the station plot in the form of compass directions.

***For Temperature & Wind/Gust, Dew Point & Wind/Gust & Dew Point Depression & Wind/Gust***

- convert_temp_to (String) - Convert the temperature-based parameter from kelvin to either fahrenheit or celsius.

- convert_speed_to (String) - Convert the wind speed/gust from m/s to either mph or kts.

## Functions

### plot_temperature()

***def plot_temperature(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER TEMPERATURE COMPARISON [Δ°F]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='custom',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['purple',
                             'darkblue',
                             'dodgerblue',
                             'white',
                             'crimson',
                             'darkred',
                             'violet'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Temperature',
                     filename='RTMA Comparison Temperature.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     convert_temperature=True,
                     convert_from='kelvin',
                     convert_to='fahrenheit',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     var_key='2m_temperature',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude'):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for temperature.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'Custom' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Temperature Analysis specified to the user's needs saved to {path}    

### plot_dew_point()

***def plot_dew_point(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER DEW POINT COMPARISON [Δ°F]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='terrain_r',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['saddlebrown',
                             'peru',
                             'darkorange',
                             'gold',
                             'white',
                             'lime',
                             'forestgreen',
                             'mediumspringgreen',
                             'aqua'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Dew Point',
                     filename='RTMA Comparison Dew Point.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     convert_temperature=True,
                     convert_from='kelvin',
                     convert_to='fahrenheit',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     var_key='2m_dew_point',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude'):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for dew point.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'terrain_r' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Dew Point Analysis specified to the user's needs saved to {path} 

### plot_dew_point_depression()

***def plot_dew_point_depression(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER DEW POINT DEPRESSION COMPARISON [Δ°F]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='terrain',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['aqua',
                             'mediumspringgreen',
                             'forestgreen',
                             'lime',
                             'white',
                             'gold',
                             'darkorange',
                             'peru',
                             'saddlebrown'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Dew Point Depression',
                     filename='RTMA Comparison Dew Point Depression.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     convert_temperature=True,
                     convert_to='fahrenheit',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     temperature_var_key='2m_temperature',
                     dew_point_var_key='2m_dew_point',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude'):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for dew point depression.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'terrain' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Dew Point Depression Analysis specified to the user's needs saved to {path}  

### plot_relative_humidity()

***def plot_relative_humidity(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 2-METER RELATIVE HUMIDITY COMPARISON [Δ%]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='terrain_r',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['saddlebrown',
                             'peru',
                             'darkorange',
                             'gold',
                             'white',
                             'lime',
                             'forestgreen',
                             'mediumspringgreen',
                             'aqua'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Relative Humidity',
                     filename='RTMA Comparison Relative Humidity.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     convert_temperature=True,
                     convert_to='fahrenheit',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     var_key='2m_relative_humidity',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude'):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for relative humidity.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'terrain_r' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Relative Humidity Analysis specified to the user's needs saved to {path}    

### plot_wind_speed()

***def plot_wind_speed(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-25,
                     stop=25,
                     step=5,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 10-METER WIND SPEED COMPARISON [ΔMPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='custom',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['purple',
                             'blue',
                             'lime',
                             'white',
                             'gold',
                             'red',
                             'violet'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Wind Speed',
                     filename='RTMA Comparison Wind Speed.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     var_key='10m_wind_speed',
                     u_var_key='10m_u_wind_component',
                     v_var_key='10m_v_wind_component',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_to='mph',
                     pixel_query_type='barbs',
                     current_barb_length=4,
                     current_barb_width=0.5,
                     current_barb_color='gray',
                     current_barb_zorder=7,
                     comparison_barb_length=4,
                     comparison_barb_width=0.5,
                     comparison_barb_color='indigo',
                     comparison_barb_zorder=7,
                     barb_legend_fontsize=7,
                     barb_legend_x_position=0.825,
                     barb_legend_y_position=0,
                     barb_legend_zorder=10):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for sustained wind speed.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'Custom' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Wind Speed Analysis specified to the user's needs saved to {path} 

### plot_wind_gust()

***def plot_wind_gust(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-25,
                     stop=25,
                     step=5,
                     facecolor='aliceblue',
                     primary_title_text='RTMA 10-METER WIND GUST COMPARISON [ΔMPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='custom',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['purple',
                             'blue',
                             'lime',
                             'white',
                             'gold',
                             'red',
                             'violet'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Wind Gust',
                     filename='RTMA Comparison Wind Gust.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     var_key='10m_wind_gust',
                     wind_direction_var_key='10m_wind_direction',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_to='mph',
                     pixel_query_type='barbs',
                     current_barb_length=4,
                     current_barb_width=0.5,
                     current_barb_color='gray',
                     current_barb_zorder=7,
                     comparison_barb_length=4,
                     comparison_barb_width=0.5,
                     comparison_barb_color='indigo',
                     comparison_barb_zorder=7,
                     barb_legend_fontsize=7,
                     barb_legend_x_position=0.825,
                     barb_legend_y_position=0,
                     barb_legend_zorder=10):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for wind gust.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'custom' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.

    Returns
    -------
    
    An image of the RTMA Wind Gust Analysis specified to the user's needs saved to {path}    

### plot_temperature_and_wind()

***def plot_temperature_and_wind(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA COMPARISON 2-METER TEMPERATURE [Δ°F] & 10-METER WIND [ΔMPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='custom',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['purple',
                             'darkblue',
                             'dodgerblue',
                             'white',
                             'crimson',
                             'darkred',
                             'violet'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     temperature_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Temperature',
                     filename='RTMA Comparison Temperature and Wind.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     temperature_var_key='2m_temperature',
                     wind_speed_var_key='10m_wind_speed',
                     u_var_key='10m_u_wind_component',
                     v_var_key='10m_v_wind_component',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_speed_to='mph',
                     convert_temperature=True,
                     convert_temp_to='fahrenheit',
                     temp_value_loc='NW',
                     speed_value_loc='NE',
                     current_barb_length=4,
                     current_barb_width=0.5,
                     current_barb_color='gray',
                     current_barb_zorder=7,
                     comparison_barb_length=4,
                     comparison_barb_width=0.5,
                     comparison_barb_color='indigo',
                     comparison_barb_zorder=7,
                     barb_legend_fontsize=7,
                     barb_legend_x_position=0.825,
                     barb_legend_y_position=0,
                     barb_legend_zorder=10):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for temperature + wind.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'custom' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Temperature + Wind Analysis specified to the user's needs saved to {path} 

### plot_temperature_and_gust()

***def plot_temperature_and_gust(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA COMPARISON 2-METER TEMPERATURE [Δ°F] & 10-METER GUST [ΔMPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='custom',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['purple',
                             'darkblue',
                             'dodgerblue',
                             'white',
                             'crimson',
                             'darkred',
                             'violet'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     temperature_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Temperature',
                     filename='RTMA Comparison Temperature and Gust.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     temperature_var_key='2m_temperature',
                     wind_gust_var_key='10m_wind_gust',
                     wind_direction_var_key='10m_wind_direction',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_speed_to='mph',
                     convert_temperature=True,
                     convert_temp_to='fahrenheit',
                     temp_value_loc='NW',
                     gust_value_loc='NE',
                     current_barb_length=4,
                     current_barb_width=0.5,
                     current_barb_color='gray',
                     current_barb_zorder=7,
                     comparison_barb_length=4,
                     comparison_barb_width=0.5,
                     comparison_barb_color='indigo',
                     comparison_barb_zorder=7,
                     barb_legend_fontsize=7,
                     barb_legend_x_position=0.825,
                     barb_legend_y_position=0,
                     barb_legend_zorder=10):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for temperature + gust.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'custom' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Temperature + Gust Analysis specified to the user's needs saved to {path} 

### plot_relative_humidity_and_wind()

***def plot_relative_humidity_and_wind(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA COMPARISON 2-METER RELATIVE HUMIDITY [Δ%] & 10-METER WIND [ΔMPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='terrain_r',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['saddlebrown',
                             'peru',
                             'darkorange',
                             'gold',
                             'white',
                             'lime',
                             'forestgreen',
                             'mediumspringgreen',
                             'aqua'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     relative_humidity_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Relative Humidity',
                     filename='RTMA Comparison Relative Humidity and Wind.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     relative_humidity_var_key='2m_relative_humidity',
                     wind_speed_var_key='10m_wind_speed',
                     u_var_key='10m_u_wind_component',
                     v_var_key='10m_v_wind_component',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_to='mph',
                     rh_value_loc='NW',
                     speed_value_loc='NE',
                     current_barb_length=4,
                     current_barb_width=0.5,
                     current_barb_color='gray',
                     current_barb_zorder=7,
                     comparison_barb_length=4,
                     comparison_barb_width=0.5,
                     comparison_barb_color='indigo',
                     comparison_barb_zorder=7,
                     barb_legend_fontsize=7,
                     barb_legend_x_position=0.825,
                     barb_legend_y_position=0,
                     barb_legend_zorder=10):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for relative humidity + wind.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'terrain_r' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Relative Humidity + Wind Analysis specified to the user's needs saved to {path}   

### plot_relative_humidity_and_gust()

***def plot_relative_humidity_and_gust(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA COMPARISON 2-METER RELATIVE HUMIDITY [Δ%] & 10-METER GUST [ΔMPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='terrain_r',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['saddlebrown',
                             'peru',
                             'darkorange',
                             'gold',
                             'white',
                             'lime',
                             'forestgreen',
                             'mediumspringgreen',
                             'aqua'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     relative_humidity_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Relative Humidity',
                     filename='RTMA Comparison Relative Humidity and Gust.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     relative_humidity_var_key='2m_relative_humidity',
                     wind_gust_var_key='10m_wind_gust',
                     wind_direction_var_key='10m_wind_direction',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_to='mph',
                     rh_value_loc='NW',
                     gust_value_loc='NE',
                     current_barb_length=4,
                     current_barb_width=0.5,
                     current_barb_color='gray',
                     current_barb_zorder=7,
                     comparison_barb_length=4,
                     comparison_barb_width=0.5,
                     comparison_barb_color='indigo',
                     comparison_barb_zorder=7,
                     barb_legend_fontsize=7,
                     barb_legend_x_position=0.825,
                     barb_legend_y_position=0,
                     barb_legend_zorder=10):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for relative_humidity + gust.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'terrain_r' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Relative Humidity + Gust Analysis specified to the user's needs saved to {path} 

### plot_dew_point_depression_and_wind()

***def plot_dew_point_depression_and_wind(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA COMPARISON 2-METER DEW POINT DEPRESSION [Δ°F] & 10-METER WIND [ΔMPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='terrain',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['aqua',
                             'mediumspringgreen',
                             'forestgreen',
                             'lime',
                             'chartreuse',
                             'olivedrab'
                             'olive',
                             'gold',
                             'darkorange',
                             'peru',
                             'saddlebrown'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     dew_point_depression_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Dew Point Depression',
                     filename='RTMA Comparison Dew Point Depression and Wind.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     dew_point_var_key='2m_dew_point',
                     wind_speed_var_key='10m_wind_speed',
                     temperature_var_key='2m_temperature',
                     u_var_key='10m_u_wind_component',
                     v_var_key='10m_v_wind_component',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_speed_to='mph',
                     convert_temperature=True,
                     convert_temp_to='fahrenheit',
                     dd_value_loc='NW',
                     speed_value_loc='NE',
                     current_barb_length=4,
                     current_barb_width=0.5,
                     current_barb_color='gray',
                     current_barb_zorder=7,
                     comparison_barb_length=4,
                     comparison_barb_width=0.5,
                     comparison_barb_color='indigo',
                     comparison_barb_zorder=7,
                     barb_legend_fontsize=7,
                     barb_legend_x_position=0.825,
                     barb_legend_y_position=0,
                     barb_legend_zorder=10):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for dew point depression + wind.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'terrain' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Dew Point Depression + Wind Analysis specified to the user's needs saved to {path} 

### plot_dew_point_depression_and_gust()

***def plot_dew_point_depression_and_gust(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA COMPARISON 2-METER DEW POINT DEPRESSION [Δ°F] & 10-METER GUST [ΔMPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='terrain',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['aqua',
                             'mediumspringgreen',
                             'forestgreen',
                             'lime',
                             'chartreuse',
                             'olivedrab'
                             'olive',
                             'gold',
                             'darkorange',
                             'peru',
                             'saddlebrown'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     dew_point_depression_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Dew Point Depression',
                     filename='RTMA Comparison Dew Point Depression and Gust.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     dew_point_var_key='2m_dew_point',
                     temperature_var_key='2m_temperature',
                     wind_gust_var_key='10m_wind_gust',
                     wind_direction_var_key='10m_wind_direction',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_speed_to='mph',
                     convert_temperature=True,
                     convert_temp_to='fahrenheit',
                     dd_value_loc='NW',
                     gust_value_loc='NE',
                     current_barb_length=4,
                     current_barb_width=0.5,
                     current_barb_color='gray',
                     current_barb_zorder=7,
                     comparison_barb_length=4,
                     comparison_barb_width=0.5,
                     comparison_barb_color='indigo',
                     comparison_barb_zorder=7,
                     barb_legend_fontsize=7,
                     barb_legend_x_position=0.825,
                     barb_legend_y_position=0,
                     barb_legend_zorder=10):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for dew point depression + gust.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'terrain' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Dew Point Depression + Gust Analysis specified to the user's needs saved to {path}   

### plot_dew_point_and_wind()

***def plot_dew_point_and_wind(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA COMPARISON 2-METER DEW POINT [Δ°F] & 10-METER WIND [ΔMPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='terrain_r',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['saddlebrown',
                             'peru',
                             'darkorange',
                             'gold',
                             'olive',
                             'olivedrab',
                             'chartreuse',
                             'lime',
                             'forestgreen',
                             'mediumspringgreen',
                             'aqua'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     dew_point_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Dew Point',
                     filename='RTMA Comparison Dew Point and Wind.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     dew_point_var_key='2m_dew_point',
                     wind_speed_var_key='10m_wind_speed',
                     u_var_key='10m_u_wind_component',
                     v_var_key='10m_v_wind_component',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_speed_to='mph',
                     convert_temperature=True,
                     convert_temp_to='fahrenheit',
                     dwpt_value_loc='NW',
                     speed_value_loc='NE',
                     current_barb_length=4,
                     current_barb_width=0.5,
                     current_barb_color='gray',
                     current_barb_zorder=7,
                     comparison_barb_length=4,
                     comparison_barb_width=0.5,
                     comparison_barb_color='indigo',
                     comparison_barb_zorder=7,
                     barb_legend_fontsize=7,
                     barb_legend_x_position=0.825,
                     barb_legend_y_position=0,
                     barb_legend_zorder=10):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for dew point + wind.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'terrain_r' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Dew Point + Wind Analysis specified to the user's needs saved to {path}    

### plot_dew_point_and_gust()

***def plot_dew_point_and_gust(region='hi',
                     hours=24,
                     show_states=True,
                     state_border_color='black',
                     state_border_linewidth=0.5,
                     state_border_zorder=3,
                     show_counties=True,
                     county_border_color='black',
                     county_border_linewidth=0.25,
                     county_border_zorder=3,
                     show_gacc_boundaries=False,
                     gacc_border_color='black',
                     gacc_border_linewidth=0.5,
                     gacc_border_zorder=3,
                     show_predictive_services_areas=False,
                     predictive_services_areas_color='black',
                     predictive_services_areas_linewidth=0.25,
                     predictive_services_areas_zorder=3,
                     show_nws_public_zones=False,
                     nws_public_zones_color='black',
                     nws_public_zones_linewidth=0.25,
                     nws_public_zones_zorder=3,
                     show_nws_fire_weather_zones=False,
                     nws_fire_weather_zones_color='black',
                     nws_fire_weather_zones_linewidth=0.25,
                     nws_fire_weather_zones_zorder=3,
                     show_nws_cwa=False,
                     nws_cwa_color='black',
                     nws_cwa_linewidth=0.5,
                     nws_cwa_zorder=3,
                     show_calfire_boundaries=False,
                     calfire_boundary_color='black',
                     calfire_boundary_linewidth=0.25,
                     calfire_boundary_zorder=3,
                     custom_shapefile_url=None,
                     custom_shapefile_folder_name='Custom Shapefile',
                     custom_shapefile_file_extension='.zip',
                     custom_shapefile_color='black',
                     custom_shapefile_linewidth=0.5,
                     custom_shapefile_zorder=3,
                     custom_geojson_url=None,
                     custom_geojson_filename=None,
                     custom_geojson_folder_name='Custom GeoJSON',
                     custom_geojson_color='black',
                     custom_geojson_linewidth=0.5,
                     custom_geojson_zorder=3,
                     custom_shapefile_local_path=None,
                     custom_shapefile_local_color='black',
                     custom_shapefile_local_linewidth=0.5,
                     custom_shapefile_local_zorder=3,
                     custom_geojson_local_path=None,
                     custom_geojson_local_color='black',
                     custom_geojson_local_linewidth=0.5,
                     custom_geojson_local_zorder=3,
                     convert_custom_shapefile_crs=False,
                     convert_local_custom_shapefile_crs=False,
                     refresh_cartographic_files=True,
                     reference_system='States & Counties',
                     show_rivers=False,
                     rivers_zorder=9,
                     rivers_color='lightcyan',
                     figure_x_length=12,
                     figure_y_length=12,
                     coastline_linewidth=0.75,
                     land_color='beige',
                     ocean_color='lightcyan',
                     lakes_color='lightcyan',
                     costline_zorder=9,
                     ocean_zorder=1,
                     lakes_zorder=1,
                     land_zorder=1,
                     decimate=10,
                     start=-10,
                     stop=10,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA COMPARISON 2-METER DEW POINT [Δ°F] & 10-METER GUST [ΔMPH]',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=8,
                     secondary_title_fontsize=7,
                     local_time=True,
                     signature_textbox_color='wheat',
                     signature_textbox_style='round',
                     signature_textbox_alpha=1,
                     signature_textbox_zorder=10,
                     signature_fontsize=8,
                     signature_textbox_x_position=0.01,
                     signature_textbox_y_position=-0.175,
                     signature_text_new_lines=False,
                     reference_system_textbox_color='wheat',
                     reference_system_textbox_style='round',
                     reference_system_textbox_alpha=1,
                     reference_system_textbox_zorder=10,
                     reference_system_fontsize=6,
                     reference_system_textbox_x_position=0.01,
                     reference_system_textbox_y_position=0,
                     colorbar_shrink=1,
                     colorbar_pad=0.01,
                     tick_label_fontsize=9,
                     colorbar_location='bottom',
                     colorbar_interval=1,
                     colorbar_aspect=50,
                     colormap='terrain_r',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['saddlebrown',
                             'peru',
                             'darkorange',
                             'gold',
                             'olive',
                             'olivedrab',
                             'chartreuse',
                             'lime',
                             'forestgreen',
                             'mediumspringgreen',
                             'aqua'],
                     ds1=None,
                     ds2=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=6,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     dew_point_pixel_query_value_fontcolor='darkred',
                     wind_speed_pixel_query_value_fontcolor='darkblue',
                     pixel_query_stroke_linewidth=1,
                     path='FireWxPy Graphics/RTMA Comparison/Dew Point',
                     filename='RTMA Comparison Dew Point and Gust.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     custom_data_directory=None,
                     mapcrs=_ccrs.PlateCarree(),
                     datacrs=_ccrs.PlateCarree(),
                     dew_point_var_key='2m_dew_point',
                     wind_gust_var_key='10m_wind_gust',
                     wind_direction_var_key='10m_wind_direction',
                     time_coord_key='time',
                     longitude_key='longitude',
                     latitude_key='latitude',
                     convert_wind_speed=True,
                     convert_speed_to='mph',
                     convert_temperature=True,
                     convert_temp_to='fahrenheit',
                     dwpt_value_loc='NW',
                     gust_value_loc='NE',
                     current_barb_length=4,
                     current_barb_width=0.5,
                     current_barb_color='gray',
                     current_barb_zorder=7,
                     comparison_barb_length=4,
                     comparison_barb_width=0.5,
                     comparison_barb_color='indigo',
                     comparison_barb_zorder=7,
                     barb_legend_fontsize=7,
                     barb_legend_x_position=0.825,
                     barb_legend_y_position=0,
                     barb_legend_zorder=10):***

    This function plots the latest Real Time Mesoscale Analysis (RTMA) for dew point + gust.
    
        Important things to note
        ------------------------
    
        1) Users can download, process and plot the data all within this function (recommended for users creating an image or two).
        
        2) Users can also use the WxData package or their own methods for downloading the data and passing the dataset into the function.
            (Recommended for users who are creating a large suite of graphics). The WxData package is the recommended data-access method - 
            especially for users on VPN/PROXY connections. The function will utilize the WxData package for the data-access method when 
            downloading and processing inside of the function. 
            
        3) Important default settings to note:
            i) Hawaii region.
            ii) 'terrain_r' Colormap from Matplotlib.
            iii) States & Counties cartographic reference system.
            iv) 12x12 figure size.
            v) Downloading/processing/plotting all done inside of the function.
            
    Returns
    -------
    
    An image of the RTMA Dew Point + Gust Analysis specified to the user's needs saved to {path}    
