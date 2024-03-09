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
import pandas as pd
import matplotlib.gridspec as gridspec

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from NWS_Generic_Forecast_Graphics import standard

class CONUS:

    r'''
    This class hosts the Counties Perspective and the Predictive Services Areas Perspective for the CONUS aka the "Lower-48" 

    '''
    
    class Counties_Perspective:

        r'''
        This class uses state and county borders as the geographic reference. 

        '''
    
        def short_term_forecast_dry_and_windy_areas_sustained_winds(directory_name, red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_speed_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, title_font_size, subplot_title_fontsize, fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size):

            r'''
            This function shows the National Weather Service Forecast for the next 18 hours filtered to focus on dry and windy conditions. This function shades areas in red where user defined dry and windy criteria are met. 

            Inputs:
                1) directory_name (String) - The directory name is the complete filepath on the National Weather Service FTP server. 
                                          The directory determines the domain the forecast data is valid for. 
                                          Here is the full directory list: 
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

                2) red_flag_warning_relative_humidity_threshold (Integer) - The low relative humidity threshold for a red flag warning. 

                3) red_flag_warning_wind_speed_threshold (Integer) - The wind speed threshold for a red flag warning. 

                4) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.

                5) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.

                6) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.

                7) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.

                8) central_longitude (Integer or Float) - The central longitude. Defaults to -96.

                9) central_latitude (Integer or Float) - The central latitude. Defaults to 39.

                10) first_standard_parallel (Integer or Float) - Southern standard parallel. 

                11) second_standard_parallel (Integer or Float) - Northern standard parallel. 

                12) title_font_size (Integer) - The fontsize of the title of the figure. 

                13) subplot_title_fontsize (Integer) - The fontsize of the title of the subplots. 

                14) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                15) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                16) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                17) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                18) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            '''

            directory_name = directory_name
            
            ds_ws = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data_to_xarray(directory_name, 'ds.wspd.bin')
            ds_rh = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data_to_xarray(directory_name, 'ds.rhm.bin')
            
            ds_mph = ds_ws['si10'] * 2.23694

            rh = ds_rh['r2']

            lon = ds_mph['longitude']
            lat = ds_mph['latitude']


            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold
            red_flag_warning_wind_speed_threshold = red_flag_warning_wind_speed_threshold
    
    
            mask = (rh <= red_flag_warning_relative_humidity_threshold) & (ds_mph >= red_flag_warning_wind_speed_threshold)


            times = []
            val_time = mask['valid_time']
            time = pd.to_datetime(val_time)
            
            for t in time:
                times.append(t)


            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    
            datacrs = ccrs.PlateCarree()
            cmap_rfw = colormaps.red_flag_warning_criteria_colormap()

            current_time = datetime.utcnow()
            
            hour = current_time.hour
            


            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            gs = gridspec.GridSpec(4, 3)
            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Sustained Wind Speed >= " + str(red_flag_warning_wind_speed_threshold) + " MPH", fontsize=title_font_size, fontweight='bold')
            plt.axis('off')
            
            ax1 = plt.subplot(gs[0:2, 0:1], projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            
            ax2 = plt.subplot(gs[0:2, 1:2], projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            
            ax3 = plt.subplot(gs[0:2, 2:3], projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            
            ax4 = plt.subplot(gs[2:4, 0:1], projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            
            ax5 = plt.subplot(gs[2:4, 1:2], projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax5.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax5.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            
            ax6 = plt.subplot(gs[2:4, 2:3], projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax6.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax6.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)


            ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy|(C) Eric J. Drewitz 2024|Data Source: NOAA/NWS\nPlot Creation Time: " + current_time.strftime('%m/%d/%Y %HZ'), fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)
            
            ax1.set_title("Valid: " + times[0].strftime('%m/%d %HZ') + " - " + times[1].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax2.set_title("Valid: " + times[1].strftime('%m/%d %HZ') + " - " + times[2].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax3.set_title("Valid: " + times[2].strftime('%m/%d %HZ') + " - " + times[3].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax4.set_title("Valid: " + times[3].strftime('%m/%d %HZ') + " - " + times[4].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax5.set_title("Valid: " + times[4].strftime('%m/%d %HZ') + " - " + times[5].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax6.set_title("Valid: " + times[5].strftime('%m/%d %HZ') + " - " + times[6].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')

        
            try:
                ax1.pcolormesh(lon,lat,mask[0, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax2.pcolormesh(lon,lat,mask[1, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax3.pcolormesh(lon,lat,mask[2, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax4.pcolormesh(lon,lat,mask[3, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax5.pcolormesh(lon,lat,mask[4, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax6.pcolormesh(lon,lat,mask[5, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
            except Exception as e:
                pass


            return fig


        def short_term_forecast_dry_and_windy_areas_wind_gusts(directory_name, red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_gust_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, title_font_size, subplot_title_fontsize, fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size):

            r'''
            This function shows the National Weather Service Forecast for the next 18 hours filtered to focus on dry and windy conditions. This function shades areas in red where user defined dry and windy criteria are met. 

            Inputs:
                1) directory_name (String) - The directory name is the complete filepath on the National Weather Service FTP server. 
                                          The directory determines the domain the forecast data is valid for. 
                                          Here is the full directory list: 
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

                2) red_flag_warning_relative_humidity_threshold (Integer) - The low relative humidity threshold for a red flag warning. 

                3) red_flag_warning_wind_gust_threshold (Integer) - The wind gust threshold for a red flag warning. 

                4) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.

                5) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.

                6) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.

                7) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.

                8) central_longitude (Integer or Float) - The central longitude. Defaults to -96.

                9) central_latitude (Integer or Float) - The central latitude. Defaults to 39.

                10) first_standard_parallel (Integer or Float) - Southern standard parallel. 

                11) second_standard_parallel (Integer or Float) - Northern standard parallel. 

                12) title_font_size (Integer) - The fontsize of the title of the figure. 

                13) subplot_title_fontsize (Integer) - The fontsize of the title of the subplots. 

                14) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                15) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                16) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                17) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                18) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            '''

            directory_name = directory_name
            
            ds_ws = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data_to_xarray(directory_name, 'ds.wgust.bin')
            ds_rh = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data_to_xarray(directory_name, 'ds.rhm.bin')
            
            ds_mph = ds_ws['i10fg'] * 2.23694

            rh = ds_rh['r2']

            lon = ds_mph['longitude']
            lat = ds_mph['latitude']


            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold
            red_flag_warning_wind_gust_threshold = red_flag_warning_wind_gust_threshold
    
    
            mask = (rh <= red_flag_warning_relative_humidity_threshold) & (ds_mph >= red_flag_warning_wind_gust_threshold)


            times = []
            val_time = mask['valid_time']
            time = pd.to_datetime(val_time)
            
            for t in time:
                times.append(t)


            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    
            datacrs = ccrs.PlateCarree()
            cmap_rfw = colormaps.red_flag_warning_criteria_colormap()

            current_time = datetime.utcnow()
            
            hour = current_time.hour
            


            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            gs = gridspec.GridSpec(4, 3)
            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Wind Gusts >= " + str(red_flag_warning_wind_gust_threshold) + " MPH", fontsize=title_font_size, fontweight='bold')
            plt.axis('off')
            
            ax1 = plt.subplot(gs[0:2, 0:1], projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax1.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            
            ax2 = plt.subplot(gs[0:2, 1:2], projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax2.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            
            ax3 = plt.subplot(gs[0:2, 2:3], projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax3.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            
            ax4 = plt.subplot(gs[2:4, 0:1], projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax4.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax4.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            
            ax5 = plt.subplot(gs[2:4, 1:2], projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax5.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax5.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)
            
            ax6 = plt.subplot(gs[2:4, 2:3], projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)
            ax6.add_feature(cfeature.STATES, linewidth=2, edgecolor='blue', zorder=3)
            ax6.add_feature(USCOUNTIES, linewidth=1.5, zorder=2)


            ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy|(C) Eric J. Drewitz 2024|Data Source: NOAA/NWS\nPlot Creation Time: " + current_time.strftime('%m/%d/%Y %HZ'), fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)
            
            ax1.set_title("Valid: " + times[0].strftime('%m/%d %HZ') + " - " + times[1].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax2.set_title("Valid: " + times[1].strftime('%m/%d %HZ') + " - " + times[2].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax3.set_title("Valid: " + times[2].strftime('%m/%d %HZ') + " - " + times[3].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax4.set_title("Valid: " + times[3].strftime('%m/%d %HZ') + " - " + times[4].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax5.set_title("Valid: " + times[4].strftime('%m/%d %HZ') + " - " + times[5].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax6.set_title("Valid: " + times[5].strftime('%m/%d %HZ') + " - " + times[6].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')

        
            try:
                ax1.pcolormesh(lon,lat,mask[0, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax2.pcolormesh(lon,lat,mask[1, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax3.pcolormesh(lon,lat,mask[2, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax4.pcolormesh(lon,lat,mask[3, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax5.pcolormesh(lon,lat,mask[4, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax6.pcolormesh(lon,lat,mask[5, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
            except Exception as e:
                pass


            return fig
    
    
    class Predictive_Services_Areas_Perspective:

        r'''
        This class uses Geographic Area Coordination Center (GACC) and Predictive Services Areas (PSA) borders as the geographic reference. 

        '''
    
        def short_term_forecast_dry_and_windy_areas_sustained_winds(directory_name, red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_speed_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, title_font_size, subplot_title_fontsize, fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size):

            r'''
            This function shows the National Weather Service Forecast for the next 18 hours filtered to focus on dry and windy conditions. This function shades areas in red where user defined dry and windy criteria are met. 

            Inputs:
                1) directory_name (String) - The directory name is the complete filepath on the National Weather Service FTP server. 
                                          The directory determines the domain the forecast data is valid for. 
                                          Here is the full directory list: 
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

                2) red_flag_warning_relative_humidity_threshold (Integer) - The low relative humidity threshold for a red flag warning. 

                3) red_flag_warning_wind_speed_threshold (Integer) - The wind speed threshold for a red flag warning. 

                4) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.

                5) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.

                6) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.

                7) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.

                8) central_longitude (Integer or Float) - The central longitude. Defaults to -96.

                9) central_latitude (Integer or Float) - The central latitude. Defaults to 39.

                10) first_standard_parallel (Integer or Float) - Southern standard parallel. 

                11) second_standard_parallel (Integer or Float) - Northern standard parallel. 

                12) title_font_size (Integer) - The fontsize of the title of the figure. 

                13) subplot_title_fontsize (Integer) - The fontsize of the title of the subplots. 

                14) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                15) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                16) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                17) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                18) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            '''

            directory_name = directory_name
            
            ds_ws = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data_to_xarray(directory_name, 'ds.wspd.bin')
            ds_rh = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data_to_xarray(directory_name, 'ds.rhm.bin')
            
            ds_mph = ds_ws['si10'] * 2.23694

            rh = ds_rh['r2']

            lon = ds_mph['longitude']
            lat = ds_mph['latitude']

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')


            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold
            red_flag_warning_wind_speed_threshold = red_flag_warning_wind_speed_threshold
    
    
            mask = (rh <= red_flag_warning_relative_humidity_threshold) & (ds_mph >= red_flag_warning_wind_speed_threshold)


            times = []
            val_time = mask['valid_time']
            time = pd.to_datetime(val_time)
            
            for t in time:
                times.append(t)


            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    
            datacrs = ccrs.PlateCarree()
            cmap_rfw = colormaps.red_flag_warning_criteria_colormap()

            current_time = datetime.utcnow()
            
            hour = current_time.hour
            


            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            gs = gridspec.GridSpec(4, 3)
            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Sustained Wind Speed >= " + str(red_flag_warning_wind_speed_threshold) + " MPH", fontsize=title_font_size, fontweight='bold')
            plt.axis('off')
            
            ax1 = plt.subplot(gs[0:2, 0:1], projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            
            ax2 = plt.subplot(gs[0:2, 1:2], projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            
            ax3 = plt.subplot(gs[0:2, 2:3], projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            
            ax4 = plt.subplot(gs[2:4, 0:1], projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
            
            ax5 = plt.subplot(gs[2:4, 1:2], projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax5.add_feature(PSAs, linewidth=1.5, zorder=2)
            
            ax6 = plt.subplot(gs[2:4, 2:3], projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax6.add_feature(PSAs, linewidth=1.5, zorder=2)


            ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy|(C) Eric J. Drewitz 2024|Data Source: NOAA/NWS\nPlot Creation Time: " + current_time.strftime('%m/%d/%Y %HZ'), fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)
            
            ax1.set_title("Valid: " + times[0].strftime('%m/%d %HZ') + " - " + times[1].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax2.set_title("Valid: " + times[1].strftime('%m/%d %HZ') + " - " + times[2].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax3.set_title("Valid: " + times[2].strftime('%m/%d %HZ') + " - " + times[3].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax4.set_title("Valid: " + times[3].strftime('%m/%d %HZ') + " - " + times[4].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax5.set_title("Valid: " + times[4].strftime('%m/%d %HZ') + " - " + times[5].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax6.set_title("Valid: " + times[5].strftime('%m/%d %HZ') + " - " + times[6].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')

        
            try:
                ax1.pcolormesh(lon,lat,mask[0, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax2.pcolormesh(lon,lat,mask[1, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax3.pcolormesh(lon,lat,mask[2, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax4.pcolormesh(lon,lat,mask[3, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax5.pcolormesh(lon,lat,mask[4, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax6.pcolormesh(lon,lat,mask[5, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
            except Exception as e:
                pass


            return fig    


        def short_term_forecast_dry_and_windy_areas_wind_gusts(directory_name, red_flag_warning_relative_humidity_threshold, red_flag_warning_wind_gust_threshold, western_bound, eastern_bound, southern_bound, northern_bound, central_longitude, central_latitude, first_standard_parallel, second_standard_parallel, title_font_size, subplot_title_fontsize, fig_x_length, fig_y_length, signature_x_position, signature_y_position, signature_font_size):

            r'''
            This function shows the National Weather Service Forecast for the next 18 hours filtered to focus on dry and windy conditions. This function shades areas in red where user defined dry and windy criteria are met. 

            Inputs:
                1) directory_name (String) - The directory name is the complete filepath on the National Weather Service FTP server. 
                                          The directory determines the domain the forecast data is valid for. 
                                          Here is the full directory list: 
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

                2) red_flag_warning_relative_humidity_threshold (Integer) - The low relative humidity threshold for a red flag warning. 

                3) red_flag_warning_wind_gust_threshold (Integer) - The wind gust threshold for a red flag warning. 

                4) western_bound (Integer or Float) - Western extent of the plot in decimal degrees.

                5) eastern_bound (Integer or Float) - Eastern extent of the plot in decimal degrees.

                6) southern_bound (Integer or Float) - Southern extent of the plot in decimal degrees.

                7) northern_bound (Integer or Float) - Northern extent of the plot in decimal degrees.

                8) central_longitude (Integer or Float) - The central longitude. Defaults to -96.

                9) central_latitude (Integer or Float) - The central latitude. Defaults to 39.

                10) first_standard_parallel (Integer or Float) - Southern standard parallel. 

                11) second_standard_parallel (Integer or Float) - Northern standard parallel. 

                12) title_font_size (Integer) - The fontsize of the title of the figure. 

                13) subplot_title_fontsize (Integer) - The fontsize of the title of the subplots. 

                14) fig_x_length (Integer) - The horizontal (x-direction) length of the entire figure. 

                15) fig_y_length (Integer) - The vertical (y-direction) length of the entire figure. 

                16) signature_x_position (Integer or Float) - The x-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure. 

                17) signature_y_position (Integer or Float) - The y-position of the signature (The signature is where the credit is given to FireWxPy and the data source on the graphic) with respect to the axis of the subplot of the figure.

                18) signature_font_size (Integer) - The fontsize of the signature of the figure. 

            '''

            directory_name = directory_name
            
            ds_ws = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data_to_xarray(directory_name, 'ds.wgust.bin')
            ds_rh = da.FTP_Downloads.get_NWS_NDFD_short_term_grid_data_to_xarray(directory_name, 'ds.rhm.bin')
            
            ds_mph = ds_ws['i10fg'] * 2.23694

            rh = ds_rh['r2']

            lon = ds_mph['longitude']
            lat = ds_mph['latitude']

            PSAs = geometry.Predictive_Services_Areas.get_PSAs_custom_file_path(f"PSA Shapefiles/National_PSA_Current.shp", 'black')
            GACC = geometry.Predictive_Services_Areas.get_GACC_Boundaries_custom_file_path(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'blue')


            red_flag_warning_relative_humidity_threshold = red_flag_warning_relative_humidity_threshold
            red_flag_warning_wind_gust_threshold = red_flag_warning_wind_gust_threshold
    
    
            mask = (rh <= red_flag_warning_relative_humidity_threshold) & (ds_mph >= red_flag_warning_wind_gust_threshold)


            times = []
            val_time = mask['valid_time']
            time = pd.to_datetime(val_time)
            
            for t in time:
                times.append(t)


            mapcrs = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude, standard_parallels=(first_standard_parallel,second_standard_parallel))
    
            datacrs = ccrs.PlateCarree()
            cmap_rfw = colormaps.red_flag_warning_criteria_colormap()

            current_time = datetime.utcnow()
            
            hour = current_time.hour
            


            fig = plt.figure(figsize=(fig_x_length, fig_y_length))
            gs = gridspec.GridSpec(4, 3)
            plt.title("Exceptionally Dry & Windy Areas (Shaded)\nRH <= " + str(red_flag_warning_relative_humidity_threshold) + "% & Wind Gusts >= " + str(red_flag_warning_wind_gust_threshold) + " MPH", fontsize=title_font_size, fontweight='bold')
            plt.axis('off')
            
            ax1 = plt.subplot(gs[0:2, 0:1], projection=mapcrs)
            ax1.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax1.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax1.add_feature(PSAs, linewidth=1.5, zorder=2)
            
            ax2 = plt.subplot(gs[0:2, 1:2], projection=mapcrs)
            ax2.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax2.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax2.add_feature(PSAs, linewidth=1.5, zorder=2)
            
            ax3 = plt.subplot(gs[0:2, 2:3], projection=mapcrs)
            ax3.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax3.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax3.add_feature(PSAs, linewidth=1.5, zorder=2)
            
            ax4 = plt.subplot(gs[2:4, 0:1], projection=mapcrs)
            ax4.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax4.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax4.add_feature(PSAs, linewidth=1.5, zorder=2)
            
            ax5 = plt.subplot(gs[2:4, 1:2], projection=mapcrs)
            ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax5.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax5.add_feature(PSAs, linewidth=1.5, zorder=2)
            
            ax6 = plt.subplot(gs[2:4, 2:3], projection=mapcrs)
            ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
            ax6.add_feature(GACC, linewidth=2, edgecolor='blue', zorder=3)
            ax6.add_feature(PSAs, linewidth=1.5, zorder=2)


            ax5.text(signature_x_position, signature_y_position, "Plot Created With FireWxPy|(C) Eric J. Drewitz 2024|Data Source: NOAA/NWS\nPlot Creation Time: " + current_time.strftime('%m/%d/%Y %HZ'), fontsize=signature_font_size, fontweight='bold', horizontalalignment='center',
       verticalalignment='bottom', transform=ax5.transAxes)
            
            ax1.set_title("Valid: " + times[0].strftime('%m/%d %HZ') + " - " + times[1].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax2.set_title("Valid: " + times[1].strftime('%m/%d %HZ') + " - " + times[2].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax3.set_title("Valid: " + times[2].strftime('%m/%d %HZ') + " - " + times[3].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax4.set_title("Valid: " + times[3].strftime('%m/%d %HZ') + " - " + times[4].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax5.set_title("Valid: " + times[4].strftime('%m/%d %HZ') + " - " + times[5].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')
            ax6.set_title("Valid: " + times[5].strftime('%m/%d %HZ') + " - " + times[6].strftime('%m/%d %HZ'), fontsize=subplot_title_fontsize, fontweight='bold')

        
            try:
                ax1.pcolormesh(lon,lat,mask[0, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax2.pcolormesh(lon,lat,mask[1, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax3.pcolormesh(lon,lat,mask[2, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax4.pcolormesh(lon,lat,mask[3, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax5.pcolormesh(lon,lat,mask[4, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
                ax6.pcolormesh(lon,lat,mask[5, :, :], transform=ccrs.PlateCarree(),cmap=cmap_rfw)
            except Exception as e:
                pass


            return fig    
    


        
