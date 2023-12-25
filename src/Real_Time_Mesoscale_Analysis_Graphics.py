import pytz
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import metpy.calc as mpcalc
import numpy as np
import parsers
import data_access as da
import geometry
import calc
import colormaps

from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from NWS_Generic_Forecast_Graphics import standard


class Counties_Perspective:


    r'''

    THIS CLASS HOSTS PLOTTING FUNCTIONS TO PLOT THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA

    THE IMAGES IN THIS CLASS OVERLAY A STATE AND COUNTIES PERSPECTIVE AS THE REFERENCE FOR THE PLOTS

    (C) METEOROLOGIST ERIC J. DREWITZ 2023

    '''
    class CONUS:

        r'''
        THIS NESTED CLASS HOSTS THE IMAGES FOR CONUS AKA THE "LOWER-48"
        '''

        def plot_generic_real_time_mesoanalysis_no_METARs(parameter, plot_title, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            param = parameter

            if param == 'Wind_speed_gust_Analysis_height_above_ground' or param == 'Wind_speed_Analysis_height_above_ground' or param == 'Wind_speed_error_height_above_ground' or param == 'Wind_speed_gust_error_height_above_ground' or param == 'u-component_of_wind_Analysis_height_above_ground' or param == 'v-component_of_wind_Analysis_height_above_ground':

                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                data = data * 2.23694

            if param == 'Temperature_Analysis_height_above_ground' or param == 'Dewpoint_temperature_Analysis_height_above_ground' or param == 'Temperature_error_height_above_ground' or param == 'Dewpoint_temperature_error_height_above_ground':
                
                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(data)
                

            else:
                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                
            plot_proj = data.metpy.cartopy_crs
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)

            cs = ax.contourf(data.metpy.x, data.metpy.y, data, 
                             transform=data.metpy.cartopy_crs, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label=color_table_title, size=12, fontweight='bold')

            plt.title(plot_title + "\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.045, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_generic_real_time_mesoanalysis_with_METARs(parameter, plot_title, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, mask):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            param = parameter

            if param == 'Wind_speed_gust_Analysis_height_above_ground' or param == 'Wind_speed_Analysis_height_above_ground' or param == 'Wind_speed_error_height_above_ground' or param == 'Wind_speed_gust_error_height_above_ground' or param == 'u-component_of_wind_Analysis_height_above_ground' or param == 'v-component_of_wind_Analysis_height_above_ground':

               rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
               rtma_data = rtma_data * 2.23694

            if param == 'Temperature_Analysis_height_above_ground' or param == 'Dewpoint_temperature_Analysis_height_above_ground' or param == 'Temperature_error_height_above_ground' or param == 'Dewpoint_temperature_error_height_above_ground':
                
                rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
                rtma_data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
                

            else:
               rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
                
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label=color_table_title, size=12, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='blue',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title(plot_title + "\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\n\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') +"\n\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.045, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig



        def plot_relative_humidity_with_METARs(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, mask):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, mask)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            cmap = colormaps.relative_humidity_colormap()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=1)

            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", size=12, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='darkorange',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title("Real Time Mesoscale Analysis Relative Humidity\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\n\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') + "\n\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.045, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_relative_humidity_with_METARs(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, mask):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT FILTERS THE RELATIVE HUMIDITY DATASET TO ONLY PLOT WHERE THE RELATIVE HUMIDITY IS 15% OR LESS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, mask)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=1)

            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", size=12, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='darkorange',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title("Real Time Mesoscale Analysis Red-Flag Relative Humidity (RH <=15%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\n\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') + "\n\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.045, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_low_and_high_relative_humidity(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT FILTERS THE RELATIVE HUMIDITY DATASET TO ONLY PLOT WHERE THE RELATIVE HUMIDITY IS 15% OR LESS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)

            cs_low = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=1)

            cs_high = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(80, 101, 1), cmap='Greens', alpha=1)

            cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=0.03)
            cbar_low.set_label(label="Low Relative Humidity (RH <= 15%)", size=12, fontweight='bold')

            cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=0.03)
            cbar_high.set_label(label="High Relative Humidity (RH >= 80%)", size=12, fontweight='bold')


            plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_relative_humidity_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE RELATIVE HUMIDITY FROM THE CURRENT TIME AND THE RELATIVE HUMIDITY FROM 24 HOURS AGO AND PLOTS THE 24 HOUR RELATIVE HUMIDITY CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_relative_humidity_24_hour_difference_data(utc_time)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-60, 65, 5), cmap='BrBG', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity Change (%)", size=12, fontweight='bold')


            plt.title("24-Hour Relative Humidity Change (%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_temperature_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE TEMPERATURE FROM THE CURRENT TIME AND THE TEMPERATURE FROM 24 HOURS AGO AND PLOTS THE 24 HOUR TEMPERATURE CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Temperature_Analysis_height_above_ground')

            rtma_data = calc.unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(rtma_data)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-20, 21, 1), cmap='seismic', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Temperature Change (\N{DEGREE SIGN}F)", size=12, fontweight='bold')


            plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_wind_speed_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE WIND SPEED FROM THE CURRENT TIME AND THE WIND SPEED FROM 24 HOURS AGO AND PLOTS THE 24 HOUR WIND SPEED CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Wind_speed_Analysis_height_above_ground')

            rtma_data = rtma_data * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-30, 31, 1), cmap='PuOr_r', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Wind Speed Change (MPH)", size=12, fontweight='bold')


            plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig
            

        def plot_current_frost_freeze_areas(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT SHOWS THE CURRENT AREAS EXPERIENCING BELOW FREEZING TEMPERATURES SINCE FROST/FREEZE CAN TURN LIVE FUEL INTO DEAD FUEL WHICH CAN ULTIMATELY LEAD TO MORE SUCCEPTABLE FUELS FOR WILDFIRE.

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Temperature_Analysis_height_above_ground')

            rtma_data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-10, 33, 1), cmap='cool_r', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=12, fontweight='bold')


            plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_criteria_based_on_sustained_winds(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)

            rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Wind_speed_Analysis_height_above_ground')

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)

            cs_rh = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=0.5)

            cs_wind = ax.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 100, 5), cmap='BuPu', alpha=0.5)


            cbar_rh = fig.colorbar(cs_rh, location='left', shrink=color_table_shrink, pad=0.03)
            cbar_rh.set_label(label="Relative Humidity (%)", size=12, fontweight='bold')

            cbar_wind = fig.colorbar(cs_wind, location='right', shrink=color_table_shrink, pad=0.03)
            cbar_wind.set_label(label="Wind Speed (MPH)", size=12, fontweight='bold')


            plt.title("Red-Flag Warning Conditions (RH <= 15% and Wind Speed >= 25 MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_criteria_based_on_wind_gusts(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON WIND GUSTS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)

            rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Wind_speed_gust_Analysis_height_above_ground')

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax.add_feature(cfeature.STATES, linewidth=0.5)
            ax.add_feature(USCOUNTIES, linewidth=1.5)

            cs_rh = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=0.5)

            cs_wind = ax.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 100, 5), cmap='BuPu', alpha=0.5)


            cbar_rh = fig.colorbar(cs_rh, location='left', shrink=color_table_shrink, pad=0.03)
            cbar_rh.set_label(label="Relative Humidity (%)", size=12, fontweight='bold')

            cbar_wind = fig.colorbar(cs_wind, location='right', shrink=color_table_shrink, pad=0.03)
            cbar_wind.set_label(label="Wind Gust (MPH)", size=12, fontweight='bold')


            plt.title("Red-Flag Warning Conditions (RH <= 15% and Wind Gust >= 25 MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


class Predictive_Services_Areas_Perspective:


    r'''

    THIS CLASS HOSTS PLOTTING FUNCTIONS TO PLOT THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA

    THE IMAGES IN THIS CLASS OVERLAY A PREDICTIVE SERVICES AREAS PERSPECTIVE AS THE REFERENCE FOR THE PLOTS

    (C) METEOROLOGIST ERIC J. DREWITZ 2023

    '''
    class CONUS:

        r'''
        THIS NESTED CLASS HOSTS THE IMAGES FOR CONUS AKA THE "LOWER-48"
        '''


        def plot_generic_real_time_mesoanalysis_no_METARs(parameter, plot_title, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, PSA_Boundary_Color):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            param = parameter

            if param == 'Wind_speed_gust_Analysis_height_above_ground' or param == 'Wind_speed_Analysis_height_above_ground' or param == 'Wind_speed_error_height_above_ground' or param == 'Wind_speed_gust_error_height_above_ground' or param == 'u-component_of_wind_Analysis_height_above_ground' or param == 'v-component_of_wind_Analysis_height_above_ground':

                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                data = data * 2.23694

            if param == 'Temperature_Analysis_height_above_ground' or param == 'Dewpoint_temperature_Analysis_height_above_ground' or param == 'Temperature_error_height_above_ground' or param == 'Dewpoint_temperature_error_height_above_ground':
                
                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(data)
                

            else:
                data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, param)
                
            plot_proj = data.metpy.cartopy_crs
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs(PSA_Boundary_Color)

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs = ax.contourf(data.metpy.x, data.metpy.y, data, 
                             transform=data.metpy.cartopy_crs, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label=color_table_title, size=12, fontweight='bold')

            plt.title(plot_title + "\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + " | Image Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.045, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_generic_real_time_mesoanalysis_with_METARs(parameter, plot_title, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table, color_table_title, color_table_start, color_table_stop, color_table_step, color_table_shrink, mask, PSA_Boundary_Color):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()
            param = parameter

            if param == 'Wind_speed_gust_Analysis_height_above_ground' or param == 'Wind_speed_Analysis_height_above_ground' or param == 'Wind_speed_error_height_above_ground' or param == 'Wind_speed_gust_error_height_above_ground' or param == 'u-component_of_wind_Analysis_height_above_ground' or param == 'v-component_of_wind_Analysis_height_above_ground':

               rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
               rtma_data = rtma_data * 2.23694

            if param == 'Temperature_Analysis_height_above_ground' or param == 'Dewpoint_temperature_Analysis_height_above_ground' or param == 'Temperature_error_height_above_ground' or param == 'Dewpoint_temperature_error_height_above_ground':
                
                rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
                rtma_data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
                

            else:
               rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Synced_With_METAR(param, utc_time, mask)
                
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs(PSA_Boundary_Color)

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(color_table_start, color_table_stop, color_table_step), cmap=color_table, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label=color_table_title, size=12, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='blue',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title(plot_title + "\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\n\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') +"\n\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.045, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig



        def plot_relative_humidity_with_METARs(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, mask):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, mask)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')

            cmap = colormaps.relative_humidity_colormap()

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 105, 5), cmap=cmap, alpha=0.5)

            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", size=12, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='darkorange',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title("Real Time Mesoscale Analysis Relative Humidity\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\n\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') + "\n\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.045, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_relative_humidity_with_METARs(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink, mask):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT FILTERS THE RELATIVE HUMIDITY DATASET TO ONLY PLOT WHERE THE RELATIVE HUMIDITY IS 15% OR LESS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_proj = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.RTMA_Relative_Humidity_Synced_With_METAR(utc_time, mask)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=1)

            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity (%)", size=12, fontweight='bold')

            # Plots METAR
            stn = mpplots.StationPlot(ax, sfc_data['longitude'][sfc_data_mask].m, sfc_data['latitude'][sfc_data_mask].m,
                                     transform=ccrs.PlateCarree(), fontsize=11, zorder=10, clip_on=True)
            
            
            stn.plot_parameter('NW', sfc_data['air_temperature'].to('degF')[sfc_data_mask], color='red',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_parameter('SW', sfc_data['dew_point_temperature'].to('degF')[sfc_data_mask], color='darkorange',
                              path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_symbol('C', sfc_data['cloud_coverage'][sfc_data_mask], mpplots.sky_cover)
            
            stn.plot_parameter('E', sfc_data_rh.to('percent')[sfc_data_mask], color='lime',
                                path_effects=[withStroke(linewidth=1, foreground='black')])
            
            stn.plot_barb(sfc_data['u'][sfc_data_mask], sfc_data['v'][sfc_data_mask])

            plt.title("Real Time Mesoscale Analysis Red-Flag Relative Humidity (RH <=15%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\n\nMETAR Observations\nValid: " + metar_time_revised.strftime('%m/%d/%Y %HZ') + "\n\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.045, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_low_and_high_relative_humidity(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT FILTERS THE RELATIVE HUMIDITY DATASET TO ONLY PLOT WHERE THE RELATIVE HUMIDITY IS 15% OR LESS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs_low = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=1)

            cs_high = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(80, 101, 1), cmap='Greens', alpha=1)

            cbar_low = fig.colorbar(cs_low, location='left', shrink=color_table_shrink, pad=0.03)
            cbar_low.set_label(label="Low Relative Humidity (RH <= 15%)", size=12, fontweight='bold')

            cbar_high = fig.colorbar(cs_high, location='right', shrink=color_table_shrink, pad=0.03)
            cbar_high.set_label(label="High Relative Humidity (RH >= 80%)", size=12, fontweight='bold')


            plt.title("2.5km Real Time Mesoscale Analysis\nLow RH(<=15%) & High RH (RH >= 80%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_relative_humidity_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE RELATIVE HUMIDITY FROM THE CURRENT TIME AND THE RELATIVE HUMIDITY FROM 24 HOURS AGO AND PLOTS THE 24 HOUR RELATIVE HUMIDITY CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_relative_humidity_24_hour_difference_data(utc_time)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-60, 65, 5), cmap='BrBG', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Relative Humidity Change (%)", size=12, fontweight='bold')


            plt.title("24-Hour Relative Humidity Change (%)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_temperature_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE TEMPERATURE FROM THE CURRENT TIME AND THE TEMPERATURE FROM 24 HOURS AGO AND PLOTS THE 24 HOUR TEMPERATURE CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Temperature_Analysis_height_above_ground')

            rtma_data = calc.unit_conversion.Temperature_Or_Dewpoint_Change_to_Fahrenheit(rtma_data)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            plot_proj = rtma_data.metpy.cartopy_crs

            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-20, 21, 1), cmap='seismic', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Temperature Change (\N{DEGREE SIGN}F)", size=12, fontweight='bold')


            plt.title("24-Hour Temperature Change (\N{DEGREE SIGN}F)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_24_hour_wind_speed_change(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE WIND SPEED FROM THE CURRENT TIME AND THE WIND SPEED FROM 24 HOURS AGO AND PLOTS THE 24 HOUR WIND SPEED CHANGE

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(utc_time, 'Wind_speed_Analysis_height_above_ground')

            rtma_data = rtma_data * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-30, 31, 1), cmap='PuOr_r', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Wind Speed Change (MPH)", size=12, fontweight='bold')


            plt.title("24-Hour Wind Speed Change (MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig
            

        def plot_current_frost_freeze_areas(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT SHOWS THE CURRENT AREAS EXPERIENCING BELOW FREEZING TEMPERATURES SINCE FROST/FREEZE CAN TURN LIVE FUEL INTO DEAD FUEL WHICH CAN ULTIMATELY LEAD TO MORE SUCCEPTABLE FUELS FOR WILDFIRE.

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Temperature_Analysis_height_above_ground')

            rtma_data = calc.unit_conversion.RTMA_Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(rtma_data)
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(-10, 33, 1), cmap='cool_r', alpha=1)


            cbar = fig.colorbar(cs, shrink=color_table_shrink)
            cbar.set_label(label="Temperature (\N{DEGREE SIGN}F)", size=12, fontweight='bold')


            plt.title("Current Frost & Freeze Areas (T <= 32\N{DEGREE SIGN}F)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_criteria_based_on_sustained_winds(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON SUSTAINED WINDS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)

            rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Wind_speed_Analysis_height_above_ground')

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs_rh = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=0.5)

            cs_wind = ax.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 100, 5), cmap='BuPu', alpha=0.5)


            cbar_rh = fig.colorbar(cs_rh, location='left', shrink=color_table_shrink, pad=0.03)
            cbar_rh.set_label(label="Relative Humidity (%)", size=12, fontweight='bold')

            cbar_wind = fig.colorbar(cs_wind, location='right', shrink=color_table_shrink, pad=0.03)
            cbar_wind.set_label(label="Wind Speed (MPH)", size=12, fontweight='bold')


            plt.title("Red-Flag Warning Conditions (RH <= 15% and Wind Speed >= 25 MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_criteria_based_on_wind_gusts(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON WIND GUSTS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)

            rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Wind_speed_gust_Analysis_height_above_ground')

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Predictive_Services_Areas.get_PSAs('black')

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs_rh = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=0.5)

            cs_wind = ax.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 100, 5), cmap='BuPu', alpha=0.5)


            cbar_rh = fig.colorbar(cs_rh, location='left', shrink=color_table_shrink, pad=0.03)
            cbar_rh.set_label(label="Relative Humidity (%)", size=12, fontweight='bold')

            cbar_wind = fig.colorbar(cs_wind, location='right', shrink=color_table_shrink, pad=0.03)
            cbar_wind.set_label(label="Wind Gust (MPH)", size=12, fontweight='bold')


            plt.title("Red-Flag Warning Conditions (RH <= 15% and Wind Gust >= 25 MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig


        def plot_red_flag_criteria_based_on_wind_gusts_test(western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, fig_x_length, fig_y_length, color_table_shrink):

            r'''
            THIS FUNCTION CREATES A CUSTOMIZED PLOT OF THE 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA FOR ANY AREA INSIDE OF CONUS. THIS PLOT COMPARES THE AREAS OF RED-FLAG RELATIVE HUMIDITY CRITERIA WITH RED-FLAG WIND CRITERIA BASED ON WIND GUSTS. 

            (C) METEOROLOGIST ERIC J. DREWITZ 2023
            
            '''


            local_time, utc_time = standard.plot_creation_time()

            rtma_data, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(utc_time)

            rtma_wind, rtma_time = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(utc_time, 'Wind_speed_gust_Analysis_height_above_ground')

            rtma_wind = rtma_wind * 2.23694
            
            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
            datacrs = ccrs.PlateCarree()

            PSAs = geometry.Cal_Fire_Boundaries.get_Cal_Fire_Boundaries('black')

            plot_proj = rtma_data.metpy.cartopy_crs

            fig = plt.figure(figsize=(fig_x_length, fig_y_length))

            ax = fig.add_subplot(1, 1, 1, projection=plot_proj)
            ax.set_extent((western_bound, eastern_bound, southern_bound, northern_bound), crs=ccrs.PlateCarree())
            ax.add_feature(PSAs, linewidth=1.5)

            cs_rh = ax.contourf(rtma_data.metpy.x, rtma_data.metpy.y, rtma_data, 
                             transform=rtma_data.metpy.cartopy_crs, levels=np.arange(0, 16, 1), cmap='YlOrBr_r', alpha=0.5)

            cs_wind = ax.contourf(rtma_wind.metpy.x, rtma_wind.metpy.y, rtma_wind, 
                             transform=rtma_wind.metpy.cartopy_crs, levels=np.arange(25, 100, 5), cmap='BuPu', alpha=0.5)


            cbar_rh = fig.colorbar(cs_rh, location='left', shrink=color_table_shrink, pad=0.03)
            cbar_rh.set_label(label="Relative Humidity (%)", size=12, fontweight='bold')

            cbar_wind = fig.colorbar(cs_wind, location='right', shrink=color_table_shrink, pad=0.03)
            cbar_wind.set_label(label="Wind Gust (MPH)", size=12, fontweight='bold')


            plt.title("Red-Flag Warning Conditions (RH <= 15% and Wind Gust >= 25 MPH)\nValid: " + rtma_time.strftime('%m/%d/%Y %HZ') + "\nImage Created: " + utc_time.strftime('%m/%d/%Y %H:%MZ'), fontweight='bold')
            
            ax.text(0.5, -0.051, "Plot Created With FireWxPy (C) Eric J. Drewitz 2023\nData Source: thredds.ucar.edu", fontweight='bold', horizontalalignment='center',
           verticalalignment='bottom', transform=ax.transAxes)

            return fig
